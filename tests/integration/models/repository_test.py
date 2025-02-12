import unittest

from app.database import DBConn
from app.models.repository import RepositoryModel


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Repository"):
            id = row["H-ID"]
            nested_dict = RepositoryModel.build_nested_dict(row_dict=row, db=self.db)
            model = RepositoryModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
