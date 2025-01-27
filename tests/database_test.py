# Tests for the DBConn class in etl/database.py

import unittest

import duckdb

from src.etl.database import DBConn


class TestDBConnMethods(unittest.TestCase):
    def setUp(self):
        self.db = DBConn(fp=":memory:")
        self.db._execute("CREATE TABLE TestTable (id INT, color TEXT, fruit TEXT)")
        self.db._execute(
            "INSERT INTO TestTable VALUES (1, 'red', 'apple'), (2, 'blue', 'berry'), (3, 'yellow', 'banana'), (4, 'green', 'pepper')"
        )

    def test_select_all(self):
        expected = [
            {"id": 1, "color": "red", "fruit": "apple"},
            {"id": 2, "color": "blue", "fruit": "berry"},
            {"id": 3, "color": "yellow", "fruit": "banana"},
            {"id": 4, "color": "green", "fruit": "pepper"},
        ]
        actual = self.db.select_all("SELECT * FROM TestTable")
        self.assertListEqual(expected, actual)

    def test_select_one_a(self):
        expected = {"id": 1, "color": "red", "fruit": "apple"}
        actual = self.db.select_one("SELECT * FROM TestTable WHERE id=1")
        self.assertDictEqual(expected, actual)

    def test_select_one_b(self):
        expected = {"id": 1, "color": "red", "fruit": "apple"}
        actual = self.db.select_one("SELECT * FROM TestTable WHERE id=1 LIMIT 1;")
        self.assertDictEqual(expected, actual)

    def test_get_row(self):
        exepcted = {"id": 1, "color": "red", "fruit": "apple"}
        actual = self.db.get_by_id(table="TestTable", col="id", id=1)
        self.assertDictEqual(exepcted, actual)

        exepcted = None
        actual = self.db.get_by_id(table="TestTable", col="id", id=5)
        self.assertEqual(exepcted, actual)

        try:
            self.db.get_by_id(table="MissingTable", col="id", id=1)
        except duckdb.CatalogException:
            pass


if __name__ == "__main__":
    unittest.main()
