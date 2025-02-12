import unittest

from app.database import DBConn
from app.models.digitization import DigitizationModel


class DigigizationTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for dig in self.db.select_all("SELECT * FROM Digitization"):
            dig_id = dig["H-ID"]
            nested_dict = DigitizationModel.build_nested_dict(row_dict=dig, db=self.db)
            model = DigitizationModel(**nested_dict)
            self.assertEqual(dig_id, model.id)


if __name__ == "__main__":
    unittest.main()
