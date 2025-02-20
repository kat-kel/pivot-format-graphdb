from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from pathlib import Path
from app.constants import XML_ID
from app.xml_transformers.witness.fileDesc.tree import WitnessFileDesc
from app.xml_transformers.witness.profileDesc.tree import ProfileDesc

# from app.xml_transformers.witness.sourceDoc.tree import SourceDoc


class WitnessTree:
    def __init__(self, data_model: WitnessModel, ns: dict | None = None):
        # Load the witness's modeled data
        self.data = data_model

        # If a namespace has been given for the TEI root, update the attrib
        attrib = {XML_ID: f"witness-{data_model.id}"}
        if ns:
            attrib.update(ns)

        # Build the tree's main branches
        self.root = ET.Element("TEI", attrib=attrib)
        self.root.append(self.teiHeader)
        # self.root.append(self.sourceDoc)

    def write(self, fp: str | Path):
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="\t", level=0)
        tree.write(fp, encoding="utf-8")

    # @property
    # def sourceDoc(self) -> ET.Element:
    #     witness_parts = self.data.observed_on_pages
    #     return SourceDoc(parts=witness_parts).root

    @property
    def text(self) -> ET.Element:
        root = ET.Element("text")
        body = ET.SubElement(root, "body")
        _ = ET.SubElement(body, "div")
        return root

    @property
    def teiHeader(self) -> ET.Element:
        root = ET.Element("teiHeader")

        # Add the <fileDesc> to the <teiHeader>
        fileDesc = WitnessFileDesc(data=self.data).root
        root.append(fileDesc)

        # Replace with encodingDesc class
        encodingDesc = ET.SubElement(root, "encodingDesc")
        ET.SubElement(encodingDesc, "p")

        # Add the <profileDesc> to the <teiHeader>
        profileDesc = ProfileDesc(data=self.data).root
        root.append(profileDesc)

        return root
