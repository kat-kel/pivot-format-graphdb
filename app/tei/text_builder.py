from lxml import etree
from datetime import datetime

from app.tei.branches import build_titleStmt
from app.tei.text_xml_parser import TextXMLParser
from kuzu import Connection


class TextTEIBuilder:
    def __init__(self, conn: Connection):
        self.parser = TextXMLParser()
        self.conn = conn

    def __call__(self, text_id: int):
        build_titleStmt(
            conn=self.conn,
            text_id=text_id,
            root=self.parser.titleStmt,
        )
        # build the publicationStmt
        node = self.parser.publicationStmt.date
        node.text = datetime.today().strftime("%Y-%m-%d")

    def write(self, outfile: str) -> None:
        etree.indent(self.parser.tree)
        s = etree.tostring(
            self.parser.tree,
            encoding="utf-8",
            xml_declaration=True,
            pretty_print=True,
        )
        with open(outfile, "wb") as f:
            f.write(s)
