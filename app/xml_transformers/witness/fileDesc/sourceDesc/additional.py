import xml.etree.ElementTree as ET

from app.models.document import DocumentModel
from app.constants import XML_ID


class Additional:
    def __init__(self, doc: DocumentModel):
        self.root = ET.Element("additional")

        # Add digitization
        surrogates = ET.SubElement(self.root, "surrogates")
        for dig in doc.digitization:
            dig_xml_id = f"dig-{dig.id}"
            bibl = ET.SubElement(surrogates, "bibl", attrib={XML_ID: dig_xml_id})
            _ = ET.SubElement(bibl, "ptr", attrib={"target": dig.uri})
            idno = ET.SubElement(bibl, "idno", attrib={"type": "ark"})
            idno.text = dig.ark

            # If digitization has IIIF manifest, add another bibl
            if dig.iiif:
                iiif_xml_id = f"{dig_xml_id}-iiif"
                bibl = ET.SubElement(
                    surrogates,
                    "bibl",
                    attrib={XML_ID: iiif_xml_id, "corresp": f"#{dig_xml_id}"},
                )
                _ = ET.SubElement(bibl, "ptr", attrib={"target": dig.iiif})

        # Add bibliographic info
        if len(doc.described_at_URL):
            listBibl = ET.SubElement(self.root, "listBibl")
            for url in doc.described_at_URL:
                bibl = ET.SubElement(listBibl, "bibl")
                _ = ET.SubElement(bibl, "ptr", attrib={"target": url})
