import unittest

from app.database import DBConn
from app.models.storyverse import StoryverseModel


class StoryverseTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()

    def test(self):
        for row in self.db.select_all("SELECT * FROM Storyverse"):
            id = row["H-ID"]
            nested_dict = StoryverseModel.build_nested_dict(row_dict=row, db=self.db)
            model = StoryverseModel(**nested_dict)
            self.assertEqual(id, model.id)


if __name__ == "__main__":
    unittest.main()
