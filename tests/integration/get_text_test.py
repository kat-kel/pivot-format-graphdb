import unittest

import duckdb
from lxml import etree

import kuzu
from app import HEURIST_DB
from app.tei.text_builder import TextTEIBuilder
from app.graph.builders import create_all_edges, create_all_nodes


class TextParserTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        db = kuzu.Database()
        self.kconn = kuzu.Connection(db)
        self.dconn = duckdb.connect(HEURIST_DB)
        create_all_nodes(kconn=self.kconn, dconn=self.dconn)
        create_all_edges(kconn=self.kconn, dconn=self.dconn)
        return super().setUp()

    def test_gmh_respStmt(self):
        iterate_texts = """
        MATCH (t:Text)-[r:HAS_LANGAUGE]-(l:Language)
        WHERE l.code = 'gmh'
        RETURN t.id
        """
        response = self.kconn.execute(iterate_texts)
        while response.has_next():
            # Get the text ID
            text_id = response.get_next()[0]
            break

        # Build a TEI document for a text
        builder = TextTEIBuilder(conn=self.kconn)
        builder(text_id=text_id)

        # Read the created respStmt branch
        node = builder.parser.titleStmt.respStmt
        etree.indent(node)
        actual = etree.tostring(node, encoding="utf-8").decode().strip()

        # Affirm the created branch is what is expected
        expected = """\
<respStmt xmlns="http://www.tei-c.org/ns/1.0">
  <name>Mike Kestemont</name>
  <resp>data entry and proof correction</resp>
  <name>Kelly Christensen</name>
  <resp>conversion of metadata to TEI markup</resp>
  <name>Théo Moins</name>
  <resp>conversion of text to TEI markup</resp>
</respStmt>"""
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
