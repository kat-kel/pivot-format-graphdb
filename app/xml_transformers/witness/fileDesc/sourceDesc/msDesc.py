import xml.etree.ElementTree as ET

from app.models.part import PartModel
from app.models.document import DocumentModel
from app.constants import XML_ID

from .physDesc import PhysDesc
from .msItem import MsItem
from .msIdentifier import MsIdentifier
from .additional import Additional


class MsDesc:
    def __init__(self, doc: DocumentModel, parts: list[PartModel]):
        self.doc = doc
        self.parts = parts

        # Create the msDesc
        ms_attrib = {XML_ID: f"doc-{doc.id}"}
        if doc.collection_of_fragments == "Yes":
            ms_attrib.update({"type": "composite"})
        self.root = ET.Element("msDesc", attrib=ms_attrib)

        # Add identifier
        self.root.append(self.msIdentifier)

        # Add additional (surrogates / digitizations)
        self.root.append(self.additional)

        # Add content item for each part
        msContents = ET.SubElement(self.root, "msContents")
        for part in self.parts:
            item = MsItem(part=part).root
            msContents.append(item)

        # Add physical description
        self.root.append(self.physDesc)

    @property
    def physDesc(self) -> ET.Element:
        return PhysDesc(parts=self.parts).root

    @property
    def msIdentifier(self) -> ET.Element:
        return MsIdentifier(doc=self.doc).root

    @property
    def additional(self) -> ET.Element:
        return Additional(doc=self.doc).root
