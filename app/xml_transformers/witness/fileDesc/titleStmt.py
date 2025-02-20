from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from app.constants import ENCODER_RESP, DATA_ENTRY_RESP


class TitleStmt:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("titleStmt")

        # Add title
        self.root.append(self.build_title())

        # Add funder
        self.root.append(self.build_funder())

        # Add principal
        self.root.append(self.build_principal())

        # Add data entry respStmt
        lang_code = self.data.is_manifestation_of.language.code
        data_entry_names = DATA_ENTRY_RESP.get(lang_code)
        if not data_entry_names:
            data_entry_names = DATA_ENTRY_RESP["default"]
        for name in data_entry_names:
            self.root.append(self.build_respStmt(name=name))

        # Add encoding respStmt
        for name in ENCODER_RESP:
            self.root.append(
                self.build_respStmt(
                    name=name,
                    text="conversion to TEI markup",
                )
            )

    @property
    def text_title(self) -> str:
        return self.data.is_manifestation_of.preferred_name

    @property
    def text_key(self) -> int:
        return f"text-{self.data.is_manifestation_of.id}"

    def build_title(self) -> ET.Element:
        root = ET.Element("title", attrib={"type": "full"})
        main = ET.SubElement(
            root, "title", attrib={"type": "main", "ref": f"#{self.text_key}"}
        )
        main.text = self.text_title
        sub = ET.SubElement(root, "title", attrib={"type": "sub"})
        subtitle_text = "Electronic transcription of witness"
        if self.data.preferred_siglum:
            subtitle_text += " "
            abbr = ET.SubElement(sub, "abbr", attrib={"type": "siglum"})
            abbr.text = self.data.preferred_siglum
        sub.text = subtitle_text

        return root

    def build_respStmt(
        self, name: str, text: str = "data entry and proof correction"
    ) -> ET.Element:
        root = ET.Element("respStmt")
        name_elem = ET.SubElement(root, "name")
        name_elem.text = name
        resp = ET.SubElement(root, "resp")
        resp.text = text
        return root

    def build_funder(self) -> ET.Element:
        root = ET.Element("funder")
        root.text = "European Research Council"
        return root

    def build_principal(self) -> ET.Element:
        root = ET.Element("principal")
        root.text = "Jean-Baptiste Camps"
        return root
