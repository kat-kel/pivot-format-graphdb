import unittest

from lxml import etree
from app.tei_models.text.profileDesc import Date, ProfileDesc, Language
from app.data_models.date import DateObject
from app.data_models import TermModel
from app.tei_models.text.base_tree import TextTree

# Set up mock data for Text data model
from tests.mock_data import DATA_MODEL_TEXT


class ProfileDescTest(unittest.TestCase):
    def setUp(self):
        self.data_model = DATA_MODEL_TEXT
        self.tree = TextTree()
        # Update the tree's 'profileDesc' with the language and creation date.
        ProfileDesc.insert_data(text=self.data_model, tree=self.tree)
        return super().setUp()

    def test_build_creation(self):
        # Get a trimmed, string representation of the creation node's XML
        node = self.tree.profileDesc.creation
        etree.indent(node)
        actual = etree.tostring(node).decode().strip()

        # Affirm the XML is what's exepcted
        expected = """\
<creation xmlns="http://www.tei-c.org/ns/1.0">
  <date notBefore="1201-01-01" notAfter="1325-12-31" cert="conjecture">\
'Medio en tweede helft dertiende eeuw'</date>
</creation>\
"""
        self.assertEqual(actual, expected)

    def test_build_language(self):
        # Get a trimmed, string representation of the langUsage node's XML
        node = self.tree.profileDesc.languUsage
        etree.indent(node)
        actual = etree.tostring(node).decode().strip()

        # Affirm the XML is what's expected
        expected = """\
<langUsage xmlns="http://www.tei-c.org/ns/1.0">
  <language ident="dum" ref="https://iso639-3.sil.org/code/dum">Middle Dutch</language>
</langUsage>\
"""
        self.assertEqual(actual, expected)


class LanguageTest(unittest.TestCase):
    def setUp(self):
        self.lang_term = TermModel(
            trm_ID=1,
            trm_Label="dum (Middle Dutch)",
            trm_Description="Middle Dutch",
            trm_Code="dum",
            trm_SemanticReferenceURL="https://iso639-3.sil.org/code/dum",
        )
        return super().setUp()

    def test_language_term_parsing(self):
        # Test parsing with data
        actual = Language.load_term(language=self.lang_term)
        expected = Language(
            ident="dum",
            text="Middle Dutch",
            ref="https://iso639-3.sil.org/code/dum",
        )
        self.assertEqual(actual, expected)

        # Test parsing with missing data
        actual = Language.load_term(language=None)
        expected = Language(ident="", text="", ref="")
        self.assertEqual(actual, expected)

    def test_language_node(self):
        # Set up what's expected
        expected = """\
<language ident="dum" ref="https://iso639-3.sil.org/code/dum">Middle Dutch</language>\
"""

        # Transform the data into XML
        node = Language.build_node(term=self.lang_term)
        actual = etree.tostring(node).decode()

        # Assert that the transformed XML is what's expected
        self.assertEqual(actual, expected)


class DateObjectTest(unittest.TestCase):
    def setUp(self):
        self.date_obj = DateObject(
            estMinDate=1200,  # Should become ISO string of 1 Jan. 1200
            estMaxDate=1230.1231,  # Should become ISO string of 31 Dec. 1230
            determination="2",  # Should become 'conjecture'
        )
        return super().setUp()

    def test_date_object_parsing(self):
        # Test parsing with data
        actual = Date.load_date(date_obj=self.date_obj)
        expected = Date(
            notBefore="1200-01-01",
            notAfter="1230-12-31",
            cert="conjecture",
        )
        self.assertEqual(actual, expected)

        # Test parsing with missing data
        actual = Date.load_date(date_obj=None)
        expected = Date(notBefore="", notAfter="", cert="")
        self.assertEqual(actual, expected)

    def test_date_node(self):
        # Set up what's expected
        freetext = "Between 1200 and 1230"
        attribs = {
            "notBefore": "1200-01-01",
            "notAfter": "1230-12-31",
            "cert": "conjecture",
        }
        expected = etree.Element("date", attribs)
        expected.text = freetext

        # Transform the data into the XML node
        actual = Date.build_node(date_obj=self.date_obj, freetext=freetext)

        # Assert that the transformed XML is what is expected
        self.assertEqual(etree.tostring(actual), etree.tostring(expected))


if __name__ == "__main__":
    unittest.main()
