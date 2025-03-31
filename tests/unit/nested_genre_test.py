import unittest

import duckdb

import kuzu
from app.graph.edges import EdgeBuilder
from app.graph.edges.has_genre import TextHasGenre
from app.graph.edges.has_parent_genre import GenreHasParent
from app.graph.nodes.genre import Genre


class Test(unittest.TestCase):

    def setUp(self):
        # Connect to an in-memory Kuzu database
        db = kuzu.Database()
        self.conn = kuzu.Connection(db)

        # Create and insert a node for Text
        create_stmt = """
        CREATE NODE TABLE Text (id INT, name STRING, PRIMARY KEY (id))
        """
        self.conn.execute(create_stmt)
        df = duckdb.sql("VALUES (1, 'text')").pl()
        self.conn.execute("COPY Text FROM df")

        # Create a node table for Genre
        self.conn.execute(Genre.create_statement)

        # Insert genre nodes
        query = """
VALUES
    (5, 'child', [], Null, []),
    (4, 'parent', [], Null, []),
    (3, 'grandparent', [], Null, []),
    (2, 'cousin', [], Null, []),
    (1, 'aunt', [], Null, [])
"""
        df = duckdb.sql(query).pl()
        self.conn.execute(f"COPY {Genre.table_name} FROM df")

        # Create edge table
        create_stmt = EdgeBuilder.compose_create_statement(edge=GenreHasParent)
        self.conn.execute(create_stmt)

        # Insert edge data
        query = """
VALUES
    (5, 4),
    (4, 3),
    (2, 1)
"""
        df = duckdb.sql(query).pl()
        self.conn.execute(f"COPY {GenreHasParent.table_name} FROM df")

        # Create and insert a genre-text edge
        create_stmt = EdgeBuilder.compose_create_statement(edge=TextHasGenre)
        self.conn.execute(create_stmt)
        df = duckdb.sql("VALUES (1, 5)").pl()
        self.conn.execute(f"COPY {TextHasGenre.table_name} FROM df")
        del df

        return super().setUp()

    def test_result_ordering(self):
        query = f"""
        MATCH (child:Genre)-[r:{GenreHasParent.table_name}]->(parent:Genre)
        RETURN child, parent
        """
        rows = []
        result = self.conn.execute(query)
        while result.has_next():
            rows.append(result.get_next()[0])

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["id"], 5)
        self.assertEqual(rows[1]["id"], 4)

    def test_build_tree(self):
        id = 1
        ordered_genres = []

        query = f"""
MATCH (g:Genre)
    <-[r:{TextHasGenre.table_name}|{GenreHasParent.table_name} *1..]
    -(t:Text)
WHERE t.id = {id}
RETURN g """
        result = self.conn.execute(query)
        while result.has_next():
            ordered_genres.append(result.get_next()[0])

        from pprint import pprint

        pprint(ordered_genres)

    def tearDown(self):
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
