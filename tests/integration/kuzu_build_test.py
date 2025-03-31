import unittest

import duckdb

import kuzu
from app import HEURIST_DB
from app.graph.builders import ALL_NODES, create_all_edges, create_all_nodes
from app.graph.nodes import NodeBuilder
from app.graph.nodes.story import Story
from app.graph.nodes.storyverse import Storyverse


class BuildTest(unittest.TestCase):
    """Test the builder functions and methods for the Kuzu nodes and edges."""

    def setUp(self):
        db = kuzu.Database()
        self.kconn = kuzu.Connection(db)
        self.dconn = duckdb.connect(HEURIST_DB)
        return super().setUp()

    def test_full_build(self):
        """Test that the integrated build-all methods work."""
        create_all_nodes(kconn=self.kconn, dconn=self.dconn)
        create_all_edges(kconn=self.kconn, dconn=self.dconn)

        for node in ALL_NODES:
            # Count the number of rows selected from the DuckDB database.
            result = self.dconn.sql(node.duckdb_query).count("*").fetchone()
            expected = result[0]
            # Count the number of nodes created in the Kuzu database.
            query = f"MATCH (n:{node.table_name}) RETURN n"
            actual = self.kconn.execute(query).get_as_df().shape[0]
            # Assert that all the rows from the DuckDB database were inserted
            # as nodes in the Kuzu database.
            self.assertEqual(expected, actual)

    def test_nodes(self):
        """Test that the node builder works."""

        builder = NodeBuilder(kconn=self.kconn, dconn=self.dconn)

        # Story node
        res1 = builder(node=Story)
        count1 = res1.get_as_df().shape[0]

        # Storyverse node
        res2 = builder(node=Storyverse)
        count2 = res2.get_as_df().shape[0]

        # Sum of the created nodes
        expected = count1 + count2

        # Sum of all nodes in the graph
        res = self.kconn.execute("MATCH (n) RETURN n")
        actual = res.get_as_df().shape[0]

        # Assert that the sum of the created nodes equals the
        # sum of all nodes found in the graph
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
