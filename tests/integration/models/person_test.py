import unittest

from app.database import DBConn
from app.models.person import PersonModel


class PersonTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Person"):
            id = row["H-ID"]
            nested_dict = PersonModel.build_nested_dict(row_dict=row, db=self.db)
            model = PersonModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
