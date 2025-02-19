from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from app.models.part import PartModel
from app.constants import XML_ID


class SourceDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("sourceDesc")
        self.root.append(self.msDesc)

    @property
    def msDesc(self) -> ET.Element:
        root = ET.Element("msDesc")
        for part in self.data.observed_on_pages:
            elem = self.make_ms_part(part=part)
            root.append(elem)
        return root

    @classmethod
    def make_ms_part(cls, part: PartModel) -> ET.Element:
        root = ET.Element(
            "msPart",
            attrib={XML_ID: f"part-{part.id}"},
        )
        msIdentifier = ET.SubElement(
            root,
            "msIdentifier",
            attrib={XML_ID: f"doc-{part.is_inscribed_on.id}"},
        )

        doc = part.is_inscribed_on
        if doc.location:
            settlement = ET.SubElement(msIdentifier, "settlement")
            settlement.text = doc.location.city.place_name
            repository = ET.SubElement(msIdentifier, "repository")
            repository.text = doc.location.preferred_name
            idno = ET.SubElement(msIdentifier, "idno", attrib={"type": "shelfmark"})
            idno.text = doc.current_shelfmark
            for alt_idno in doc.old_shelfmark:
                altIdentifier = ET.SubElement(
                    msIdentifier, "altIdentifier", attrib={"type": "former"}
                )
                idno = ET.SubElement(
                    altIdentifier, "idno", attrib={"type": "shelfmark"}
                )
                idno.text = alt_idno

        return root
