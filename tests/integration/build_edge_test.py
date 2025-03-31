import unittest

import duckdb

import kuzu
from app import HEURIST_DB
from app.graph.edges import EdgeBuilder
from app.graph.edges.is_part_of_storyverse import IsPartOfStoryverse
from app.graph.nodes import NodeBuilder
from app.graph.nodes.story import Story
from app.graph.nodes.storyverse import Storyverse


class EdgesTest(unittest.TestCase):
    def setUp(self):
        db = kuzu.Database()
        self.kconn = kuzu.Connection(db)
        self.dconn = duckdb.connect(HEURIST_DB)
        return super().setUp()

    def test_multiple_from_to_pairs(self):
        # Build the nodes for the edges
        builder = NodeBuilder(kconn=self.kconn, dconn=self.dconn)
        builder(node=Story)
        builder(node=Storyverse)
        # Build the edges
        builder = EdgeBuilder(kconn=self.kconn, dconn=self.dconn)
        # Assert that the edges are built without any errors
        with self.assertNoLogs():
            builder(edge=IsPartOfStoryverse)


if __name__ == "__main__":
    unittest.main()
