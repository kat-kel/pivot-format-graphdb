from lxml import etree

from app.tei.text import TextXMLParser
from app.tei.text.branches.titleStmt import TitleStmt

# from app.tei.text.encodingDesc import EncodingDesc
# from app.tei.text.profileDesc import ProfileDesc


class TextTreeBuilder:
    def __init__(self, text_data_model) -> None:
        self.tree = TextXMLParser()

        # build the titleStmt
        TitleStmt.insert_data(text=text_data_model, tree=self.tree)

        # build the publicationStmt
        # -- built automatically with TextTree() instantiation --

        # build the encodingDesc
        # EncodingDesc.insert_data(text=text_data_model, tree=self.tree)

        # build the profileDesc
        # ProfileDesc.insert_data(text=text_data_model, tree=self.tree)

    def write(self, outfile: str) -> None:
        etree.indent(self.tree.tree)
        s = etree.tostring(
            self.tree.tree, encoding="utf-8", xml_declaration=True, pretty_print=True
        )
        with open(outfile, "wb") as f:
            f.write(s)
