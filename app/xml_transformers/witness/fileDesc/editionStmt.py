import xml.etree.ElementTree as ET


class EditionStmt:
    def __init__(self):
        self.root = ET.Element("editionStmt")

        edition = ET.SubElement(self.root, "edition", attrib={"n": "P1"})
        edition.text = "First draft"
