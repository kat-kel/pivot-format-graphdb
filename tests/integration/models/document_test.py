import unittest

from app.database import DBConn
from app.models.document import DocumentModel


class DocumentTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM DocumentTable"):
            id = row["H-ID"]
            nested_dict = DocumentModel.build_nested_dict(row_dict=row, db=self.db)
            model = DocumentModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
