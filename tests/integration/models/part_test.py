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

    def test_pages(self):
        row = self.db.get_by_id(table="Part", hid=45053)
        nested_dict = PartModel.build_nested_dict(row_dict=row, db=self.db)
        model = PartModel(**nested_dict)
        actual = model.page_ranges[0].images
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
