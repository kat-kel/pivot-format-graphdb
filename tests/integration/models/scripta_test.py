import unittest

from app.database import DBConn
from app.models.scripta import ScriptaModel


class ScriptaTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Scripta"):
            id = row["H-ID"]
            nested_dict = ScriptaModel.build_nested_dict(row_dict=row, db=self.db)
            model = ScriptaModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
