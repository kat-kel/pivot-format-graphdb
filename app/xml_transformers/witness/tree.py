from app.models.witness import WitnessModel
import xml.etree.ElementTree as ET
from app.xml_transformers.witness.fileDesc.tree import WitnessFileDesc
from app.xml_transformers.witness.profileDesc.tree import ProfileDesc


class WitnessTree:
    def __init__(self, data_model: WitnessModel):
        # Load the witness's modeled data
        self.data = data_model

        # Build the tree's main branches
        self.root = ET.Element("TEI", attrib={"xmlns": "http://www.tei-c.org/ns/1.0"})
        self.root.append(self.teiHeader)

        # Write the tree to file
        self.write()

    def write(self):
        tree = ET.ElementTree(self.root)
        ET.indent(tree, space="\t", level=0)
        tree.write("witness-tei-new.xml", encoding="utf-8")

    @property
    def teiHeader(self) -> ET.Element:
        root = ET.Element("teiHeader")

        # Add the <fileDesc> to the <teiHeader>
        fileDesc = WitnessFileDesc(data=self.data).root
        root.append(fileDesc)

        # Add the <profileDesc> to the <teiHeader>
        profileDesc = ProfileDesc(data=self.data).root
        root.append(profileDesc)

        return root
