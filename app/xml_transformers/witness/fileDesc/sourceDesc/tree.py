from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET

from .msDesc import MsDesc


class SourceDesc:
    def __init__(self, data: WitnessModel):
        self.data = data
        self.root = ET.Element("sourceDesc")

        for doc in self.group_parts_by_document(
            data=self.data.observed_on_pages
        ).values():
            manuscript, parts = doc["doc"], doc["parts"]
            elem = MsDesc(doc=manuscript, parts=parts).root
            self.root.append(elem)

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
