import unittest

from app.graph.builders import ALL_NODES, create_all_edges, create_all_nodes
from app.graph.edges.is_part_of_storyverse import (
    StoryIsPartOfStoryverse,
    StoryverseIsPartOfStoryverse,
)
from app.graph.nodes import NodeBuilder
from app.graph.nodes.story import Story
from app.graph.nodes.storyverse import Storyverse
from tests.integration import IntegrationTest


class BuildTest(IntegrationTest):
    """Test the builder functions and methods for the Kuzu nodes and edges."""

    def test_edge_integration_builder(self):
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

    def test_edges(self):
        """Test that the edge builder works."""
        # Build the nodes for the testd edge (Story & Storyverse).
        create_all_nodes(
            kconn=self.kconn,
            dconn=self.dconn,
            nodes=[
                Story,
                Storyverse,
            ],
        )

        # Build edges between Story & Storyverse and between Storyverses.
        create_all_edges(
            kconn=self.kconn,
            dconn=self.dconn,
            edges=[StoryIsPartOfStoryverse, StoryverseIsPartOfStoryverse],
        )

        # Count the edges from Story to Storyverse.
        query = "MATCH ()-[r:STORY_IS_PART_OF]-() RETURN r"
        edges1 = self.kconn.execute(query).get_num_tuples()

        # Count the edges from Storyverse to Storyverse.
        query = "MATCH ()-[r:STORYVERSE_IS_PART_OF]-() RETURN r"
        edges2 = self.kconn.execute(query).get_num_tuples()

        # Sum each edge type.
        summed_count = edges1 + edges2

        # Count all the edges created in the graph.
        query = """
        MATCH ()-[r]-() RETURN r
        """
        returned_count = self.kconn.execute(query).get_num_tuples()

        # Assert that the sum of the created edges equals the
        # sum of all edges found in the graph
        self.assertEqual(summed_count, returned_count)

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
