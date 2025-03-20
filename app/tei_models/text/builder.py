from lxml import etree
from app.tei_models.text.base_tree import TextTree
from app.data_models.text import TextModel

from app.tei_models.text.encodingDesc import EncodingDesc
from app.tei_models.text.titleStmt import TitleStmt
from app.tei_models.text.profileDesc import ProfileDesc


class TextTreeBuilder:
    def __init__(self, text_data_model: TextModel) -> None:
        self.tree = TextTree()

        # build the titleStmt
        TitleStmt.insert_data(text=text_data_model, tree=self.tree)

        # build the publicationStmt
        # -- built automatically with TextTree() instantiation --

        # build the encodingDesc
        EncodingDesc.insert_data(text=text_data_model, tree=self.tree)

        # build the profileDesc
        ProfileDesc.insert_data(text=text_data_model, tree=self.tree)

    def write(self, outfile: str) -> None:
        etree.indent(self.tree.tree)
        s = etree.tostring(
            self.tree.tree, encoding="utf-8", xml_declaration=True, pretty_print=True
        )
        with open(outfile, "wb") as f:
            f.write(s)
