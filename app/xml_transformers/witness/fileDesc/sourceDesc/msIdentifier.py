import xml.etree.ElementTree as ET

from app.models.document import DocumentModel


class MsIdentifier:
    def __init__(self, doc: DocumentModel):
        self.root = ET.Element("msIdentifier")
        if doc.location:
            settlement = ET.SubElement(self.root, "settlement")
            country_code = doc.location.city.country.code
            attrib = {}
            if country_code:
                attrib = {"key": country_code}
            country = ET.SubElement(settlement, "country", attrib=attrib)
            country.text = doc.location.city.country.label
            settlement_inner = ET.SubElement(settlement, "settlement")
            settlement_inner.text = doc.location.city.place_name
            repository = ET.SubElement(self.root, "repository")
            repository.text = doc.location.preferred_name
        idno = ET.SubElement(self.root, "idno", attrib={"type": "shelfmark"})
        idno.text = doc.current_shelfmark
        for alt_idno in doc.old_shelfmark:
            altIdentifier = ET.SubElement(
                self.root, "altIdentifier", attrib={"type": "former"}
            )
            idno = ET.SubElement(altIdentifier, "idno", attrib={"type": "shelfmark"})
            idno.text = alt_idno
        if doc.ARK:
            altIdentifier = ET.SubElement(self.root, "altIdentifier")
            idno = ET.SubElement(altIdentifier, "idno", attrib={"type": "ark"})
            idno.text = doc.ARK
