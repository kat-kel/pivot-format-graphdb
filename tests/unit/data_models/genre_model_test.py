import unittest

from app.data_models.genre import GenreModel
from app.database import DBConn


class GenreRecursionTest(unittest.TestCase):

    CHILD = {
        "H-ID": 2,
        "preferred_name": "riddarasögur indigenous",
        "parent_genre H-ID": 1,
        "alternative_names": [],
        "description": "Icelandic indigenous creations in a style of riddarasögur",
    }

    PARENT = {
        "H-ID": 1,
        "preferred_name": "riddarasögur",
        "parent_genre H-ID": None,
        "alternative_names": ["chivalric sagas"],
        "description": "The riddarasögur are Norse prose sagas of the romance genre. \
            Starting in the thirteenth century with Norse translations of French \
            chansons de geste and Latin romances and histories, the genre expanded in \
            Iceland to indigenous creations in a similar style.",
    }

    def setUp(self):
        self.db = DBConn(fp=":memory:")
        self.db._execute(
            """
CREATE TABLE Genre (
                         "H-ID" INT,
                         preferred_name VARCHAR,
                         "parent_genre H-ID" INT,
                         alternative_names VARCHAR[],
                         description TEXT)
"""
        )
        self.db._execute(
            """INSERT INTO Genre VALUES (?, ?, ?, ?, ?)""",
            parameters=self.CHILD.values(),
        )
        self.db._execute(
            """INSERT INTO Genre VALUES (?, ?, ?, ?, ?)""",
            parameters=self.PARENT.values(),
        )

    def test_nested_dict(self):
        row_dict = self.CHILD.copy()
        nested_dicts = GenreModel.build_nested_dict(row_dict=row_dict, db=self.db)
        expected = self.PARENT
        actual = nested_dicts["parent_genre H-ID"]
        self.assertDictEqual(expected, actual)

    def test_validation(self):
        row_dict = self.CHILD.copy()
        nested_dicts = GenreModel.build_nested_dict(row_dict=row_dict, db=self.db)
        model = GenreModel.model_validate(nested_dicts)
        expected = self.PARENT["preferred_name"]
        actual = model.parent_genre.preferred_name
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
