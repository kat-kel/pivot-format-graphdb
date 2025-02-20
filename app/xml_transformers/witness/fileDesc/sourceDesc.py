from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from app.models.part import PartModel
from app.models.document import DocumentModel
from app.constants import XML_ID


class SourceDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("sourceDesc")

        for doc in self.group_parts_by_document(
            data=self.data.observed_on_pages
        ).values():
            manuscript, parts = doc["doc"], doc["parts"]
            msDesc = self.make_msDesc(doc=manuscript, parts=parts)
            self.root.append(msDesc)

    @staticmethod
    def group_parts_by_document(data) -> dict:
        """All of the witness's parts need to be grouped by their document and under a
        <msDesc>. For instance, if two or more of the witness's parts are from the same
        document, they need to be under the same <msDesc>.

        Returns:
            dict: index of document IDs with arrays of their parts
        """
        doc_ids = set(p.is_inscribed_on.id for p in data)
        index = {id: {"doc": None, "parts": []} for id in doc_ids}
        for part in data:
            doc_id = part.is_inscribed_on.id
            if not index[doc_id]["doc"]:
                index[doc_id]["doc"] = part.is_inscribed_on
            index[doc_id]["parts"].append(part)
        return index

    def make_msDesc(self, doc: DocumentModel, parts: list[PartModel]) -> ET.Element:
        # Create the msDesc
        ms_attrib = {XML_ID: f"doc-{doc.id}"}
        if doc.collection_of_fragments == "Yes":
            ms_attrib.update({"type": "composite"})
        root = ET.Element("msDesc", attrib=ms_attrib)

        root.append(self.make_msIdentifier(doc=doc))
        root.append(self.make_additional(doc=doc))
        root.append(self.make_msContents(parts=parts))

        return root

    def make_msContents(self, parts: list[PartModel]) -> ET.Element:
        # For each part of the manuscript, create a msItem
        root = ET.Element("msContents")
        for part in parts:
            item = self.make_msItem(part=part)
            root.append(item)
        return root

    def make_additional(self, doc: DocumentModel) -> ET.Element:
        root = ET.Element("additional")

        # Add digitization
        surrogates = ET.SubElement(root, "surrogates")
        for dig in doc.digitization:
            dig_xml_id = f"dig-{dig.id}"
            bibl = ET.SubElement(surrogates, "bibl", attrib={XML_ID: dig_xml_id})
            _ = ET.SubElement(bibl, "ptr", attrib={"target": dig.uri})
            idno = ET.SubElement(bibl, "idno", attrib={"type": "ark"})
            idno.text = dig.ark

            # If digitization has IIIF manifest, add another bibl
            iiif_xml_id = f"{dig_xml_id}-iiif"
            bibl = ET.SubElement(
                surrogates,
                "bibl",
                attrib={XML_ID: iiif_xml_id, "corresp": f"#{dig_xml_id}"},
            )
            _ = ET.SubElement(bibl, "ptr", attrib={"target": dig.iiif})

        # Add bibliographic info
        if len(doc.described_at_URL):
            listBibl = ET.SubElement(root, "listBibl")
            for url in doc.described_at_URL:
                bibl = ET.SubElement(listBibl, "bibl")
                _ = ET.SubElement(bibl, "ptr", attrib={"target": url})

        return root

    def make_msItem(self, part: PartModel) -> ET.Element:
        root = ET.Element(
            "msItem",
            attrib={
                XML_ID: f"part-{part.id}",
                "n": str(part.div_order),
            },
        )
        # Add locus for manuscript item (part)
        locusGrp = ET.SubElement(root, "locusGrp")
        for pr in part.page_ranges:
            locus = ET.SubElement(locusGrp, "locus")
            if pr.start and pr.end:
                locus.set("from", pr.start)
                locus.set("to", pr.end)
            locus.text = pr.text

        # Add note describing what part of the text this item contains
        note = ET.SubElement(root, "note")
        note.text = part.part_of_text
        return root

    def make_msIdentifier(self, doc: DocumentModel) -> ET.Element:
        root = ET.Element("msIdentifier")
        if doc.location:
            country_code = doc.location.city.country.code
            settlement = ET.SubElement(root, "settlement")
            ET.SubElement(settlement, "country", attrib={"key": country_code})
            settlement_inner = ET.SubElement(settlement, "settlement")
            settlement_inner.text = doc.location.city.place_name
            repository = ET.SubElement(root, "repository")
            repository.text = doc.location.preferred_name
        idno = ET.SubElement(root, "idno", attrib={"type": "shelfmark"})
        idno.text = doc.current_shelfmark
        for alt_idno in doc.old_shelfmark:
            altIdentifier = ET.SubElement(
                root, "altIdentifier", attrib={"type": "former"}
            )
            idno = ET.SubElement(altIdentifier, "idno", attrib={"type": "shelfmark"})
            idno.text = alt_idno
        if doc.ARK:
            altIdentifier = ET.SubElement(root, "altIdentifier")
            idno = ET.SubElement(altIdentifier, "idno", attrib={"type": "ark"})
            idno.text = doc.ARK

        return root
