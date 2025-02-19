import unittest

from app.xml_transformers.witness.tree import WitnessTree
from app.models.witness import WitnessModel
from app.database import DBConn


TEST_IMAGES = 45040
TEST_DIG = 46368


class WitnessTreeTest(unittest.TestCase):
    def setUp(self):
        self.db = DBConn()
        item = self.db.get_by_id(table="Witness", hid=TEST_IMAGES)
        nested_row = WitnessModel.build_nested_dict(item, self.db)
        self.model = WitnessModel.model_validate(nested_row)

    def test(self):
        WitnessTree(data_model=self.model)


if __name__ == "__main__":
    unittest.main()
