import xml.etree.ElementTree as ET
from app.models.witness import WitnessModel


def datestr(value: float) -> str:
    s = str(value)
    if s.endswith(".0"):
        s = s[:-2]
    return s


class ProfileDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("profileDesc")
        self.root.append(self.creation)
        self.root.append(self.handDesc)

    @property
    def handDesc(self) -> ET.Element:
        # Make root <handDesc>
        attrib = {}
        if self.data.number_of_hands:
            attrib.update({"hands": str(self.data.number_of_hands)})
        root = ET.Element("handDesc", attrib=attrib)

        # If the scripta is available, create a handNote for the scripta
        scripta = self.data.regional_writing_style
        if scripta:
            scripta_id = f"scripta-#{scripta.id}"
            handNote = ET.SubElement(root, "handNote")
            handNote.text = "Written in "
            term = ET.SubElement(handNote, "term", attrib={"corresp": scripta_id})
            term.text = scripta.preferred_name

        return root

    @property
    def creation(self) -> ET.Element:
        root = ET.Element("creation")
        date_obj = self.data.date_of_creation
        if date_obj:
            if date_obj.timestamp:
                attrib = {"when": date_obj.timestamp.time}
            else:
                attrib = {
                    "notBefore": datestr(date_obj.start.earliest),
                    "notAfter": datestr(date_obj.end.latest),
                }
                if date_obj.start.latest:
                    attrib.update({"from": datestr(date_obj.start.latest)})
                if date_obj.end.earliest:
                    attrib.update({"to": datestr(date_obj.end.earliest)})
                if date_obj.determination:
                    attrib.update({"cert": date_obj.determination})
                elif self.data.date_of_creation_certainty:
                    attrib.update({"cert": self.data.date_of_creation_certainty.label})

            date = ET.SubElement(root, "date", attrib=attrib)
            date.text = self.data.date_freetext
        return root
