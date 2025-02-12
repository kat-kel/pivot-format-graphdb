import unittest

from app.database import DBConn
from app.models.place import PlaceModel


class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Place"):
            id = row["H-ID"]
            nested_dict = PlaceModel.build_nested_dict(row_dict=row, db=self.db)
            model = PlaceModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
