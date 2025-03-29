import unittest

from tests.integration import IntegrationTest
from app.graph.builders import create_all_edges, create_all_nodes

# from app.tei.text.builder import TextTreeBuilder


class TextParserTest(IntegrationTest):

    def test(self):
        create_all_nodes(self.kconn, self.dconn)
        create_all_edges(self.kconn, self.dconn)


if __name__ == "__main__":
    unittest.main()
