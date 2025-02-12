import unittest

from app.database import DBConn
from app.models.story import StoryModel


class StoryTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Story"):
            id = row["H-ID"]
            nested_dict = StoryModel.build_nested_dict(row_dict=row, db=self.db)
            model = StoryModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
