import unittest

from app.database import DBConn
from app.models.physdesc import PhysDescModel


class PhysDescTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM PhysDesc"):
            id = row["H-ID"]
            nested_dict = PhysDescModel.build_nested_dict(row_dict=row, db=self.db)
            model = PhysDescModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
