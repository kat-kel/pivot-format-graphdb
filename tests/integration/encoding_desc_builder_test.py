import unittest

import duckdb

import kuzu
from app import HEURIST_DB
from app.graph.builders import create_all_edges, create_all_nodes
from app.graph.edges.has_genre import TextHasGenre
from app.graph.edges.has_parent_genre import GenreHasParent
from app.tei.text_builder import TextTEIBuilder


class TextBuilderGMHTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        db = kuzu.Database()
        self.kconn = kuzu.Connection(db)
        self.dconn = duckdb.connect(HEURIST_DB)
        create_all_nodes(kconn=self.kconn, dconn=self.dconn)
        create_all_edges(kconn=self.kconn, dconn=self.dconn)

        self.builder = TextTEIBuilder(conn=self.kconn)
        return super().setUp()

    def test_genre_parentage(self):
        # Build a TEI document for a text with a nested genre
        iterate_texts = f"""
        MATCH path=(g:Genre)
    <-[r:{TextHasGenre.table_name}|{GenreHasParent.table_name} *1..]
    -(t:Text)
        WHERE LENGTH(r) > 1
        RETURN t.id
        """
        response = self.kconn.execute(iterate_texts)
        while response.has_next():
            text_id = response.get_next()[0]
            break
        self.builder(text_id=text_id)
        # Read the created genre nodes


if __name__ == "__main__":
    unittest.main()
