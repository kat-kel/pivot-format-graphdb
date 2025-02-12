import unittest

from app.database import DBConn
from app.models.witness import WitnessModel


class WitnessTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Witness"):
            id = row["H-ID"]
            nested_dict = WitnessModel.build_nested_dict(row_dict=row, db=self.db)
            model = WitnessModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
