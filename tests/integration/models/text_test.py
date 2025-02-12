import unittest

from app.database import DBConn
from app.models.text import TextModel


class TextTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM TextTable"):
            id = row["H-ID"]
            try:
                nested_dict = TextModel.build_nested_dict(row_dict=row, db=self.db)
                model = TextModel(**nested_dict)
            except Exception as e:
                from pprint import pprint

                pprint(row)
                raise e
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
