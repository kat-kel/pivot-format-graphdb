import duckdb
import kuzu
import unittest

from app.graph.nodes import Node, Metadata, NodeBuilder


class Test(unittest.TestCase):
    def setUp(self):
        db = kuzu.Database()
        self.kconn = kuzu.Connection(db)
        self.dconn = duckdb.connect("")
        return super().setUp()

    def test_manual(self):
        # Create the node table with the date properties
        n = Node(
            label="Text",
            pk="id",
            metadata=[
                Metadata(
                    label="id",
                    col="H-ID",
                    type="INT",
                ),
                Metadata(
                    label="name",
                    col="preferred_name",
                    type="STRING",
                ),
                Metadata(
                    label="date",
                    col="date_of_creation_TEMPORAL",
                    temporal=True,
                ),
            ],
            table="TextTable",
        )

        result_query = self.kconn.execute("MATCH (n) RETURN n").get_next()
        result = result_query[0]
        print(result)


if __name__ == "__main__":
    unittest.main()
