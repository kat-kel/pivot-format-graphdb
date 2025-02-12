import unittest

from app.database import DBConn
from app.models.part import PartModel


class PartTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Part"):
            id = row["H-ID"]
            nested_dict = PartModel.build_nested_dict(row_dict=row, db=self.db)
            model = PartModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
