import unittest

from lxml import etree
from app.tei_models.text.base_tree import TextTree
from app.tei_models.text.titleStmt import RespPerson, TitleStmt

# Set up mock data for Text data model
from tests.mock_data.text import DATA_MODEL


class TitleStmtTest(unittest.TestCase):
    def setUp(self):
        self.tree = TextTree()
        self.data_model = DATA_MODEL

        # Confirm that the mock data we're using is a Middle Ductch text
        lang_code = TitleStmt.get_language_code(text=self.data_model)
        self.assertEqual(lang_code, "dum")

        return super().setUp()

    def test_person_metadata(self):
        # Set up the metadata
        data = RespPerson(name="NAME", role="ROLE")

        # Use the RespPerson class method to insert nodes
        respStmt_node = etree.Element("respStmt")
        data.insert_nodes(parent=respStmt_node)

        # Affirm that 'respStmt' has the new nodes embedded
        expected = b"<respStmt><name>NAME</name><resp>ROLE</resp></respStmt>"
        actual = etree.tostring(respStmt_node)
        self.assertEqual(actual, expected)

    def test_responsibility_config(self):
        # Test yaml parsing for default language
        people = TitleStmt.load_responsibility_config(language_code=None)

        # Test that 3 roles were parsed:
        # (1) data entry, (2) metadata encoding, (3) text encoding
        from collections import Counter

        counter = Counter([p.role for p in people])
        expected = 3
        actual = counter.total()
        self.assertEqual(actual, expected)

    def test_load_data_model(self):
        # Assert that the mock Middle Dutch text has 4 contributors
        dataclass = TitleStmt.load_data_model(text=self.data_model)
        corpus_experts = [p for p in dataclass.respStmt if "proof correction" in p.role]
        expected = 4
        actual = len(corpus_experts)
        self.assertEqual(actual, expected)

    def test_insert_data(self):
        # Try to insert the parsed mock data
        TitleStmt.insert_data(text=self.data_model, tree=self.tree)

        # Assert the text's title is in the TEI document title
        expected = self.data_model.preferred_name
        title_node = self.tree.titleStmt.title
        actual = title_node.text  # 'Encoded metadata of "{title}"'
        self.assertRegex(actual, expected)


if __name__ == "__main__":
    unittest.main()
