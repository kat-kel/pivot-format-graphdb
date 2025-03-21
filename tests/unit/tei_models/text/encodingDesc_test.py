from lxml import etree
import unittest
from app.data_models.genre import GenreModel
from app.tei_models.text.encodingDesc import EncodingDesc, GenreTaxonomy
from app.tei_models.text import TextTree
from tests.mock_data.text import DATA_MODEL

NESTED_GENRE = GenreModel(
    **{
        "H-ID": 1,
        "preferred_name": "CHILD",
        "parent_genre H-ID": GenreModel(
            **{
                "H-ID": 2,
                "preferred_name": "PARENT",
                "parent_genre H-ID": GenreModel(
                    **{
                        "H-ID": 3,
                        "preferred_name": "GRANDPARENT",
                        "description": "",
                    }
                ),
                "description": "",
            }
        ),
        "description": "",
    }
)


class Test(unittest.TestCase):
    def setUp(self):
        self.tree = TextTree()
        return super().setUp()

    def test_sort_recursive_genres(self):
        # Unnest the genres and sort them by seniority
        sorted_genres = GenreTaxonomy.sort_genres(genre=NESTED_GENRE)

        # Affirm the first item is the inner-most parent
        actual = sorted_genres[0].preferred_name
        self.assertEqual(actual, "GRANDPARENT")

        # Affirm the second item is the first parent
        actual = sorted_genres[1].preferred_name
        self.assertEqual(actual, "PARENT")

        # Affirm the last item is the child
        actual = sorted_genres[2].preferred_name
        self.assertEqual(actual, "CHILD")

    def test_build_nested_category_nodes(self):
        # Create nodes for genre genealogy
        node = GenreTaxonomy.build_category_tree(genre=NESTED_GENRE)

        # Affirm that the genres nested correctly in the XML
        etree.indent(node)
        actual = etree.tostring(node).decode()
        expected = """\
<category xml:id="genre_3">
  <catDesc>GRANDPARENT</catDesc>
  <category xml:id="genre_2">
    <catDesc>PARENT</catDesc>
    <category xml:id="genre_1">
      <catDesc>CHILD</catDesc>
    </category>
  </category>
</category>\
"""
        self.assertEqual(actual, expected)

    def test_insert_data(self):
        # Try to insert the genre taxonomy nodes
        EncodingDesc.insert_data(text=DATA_MODEL, tree=self.tree)

        # Assert that there is 1 category node nested in the mock text's genre category
        category_node = self.tree.encodingDesc.genre_taxonomy
        matches = category_node.findall(".//category")
        actual = len(matches)
        expected = 1
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
