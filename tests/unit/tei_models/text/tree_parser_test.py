import unittest

from app.tei_models.text.base_tree import TextTree


class Test(unittest.TestCase):
    def setUp(self):
        self.tree = TextTree()
        return super().setUp()

    def test_titleStmt(self):
        branch = self.tree.titleStmt
        # test finding the title node
        self.assertIsNotNone(branch.title)
        # test finding the respStmt node
        self.assertIsNotNone(branch.respStmt)

    def test_publicationStmt(self):
        branch = self.tree.publicationStmt
        # test finding the date node
        self.assertIsNotNone(branch.date)


if __name__ == "__main__":
    unittest.main()
