import unittest
import kuzu
import shutil
from pathlib import Path
from app import DB_PATH
import duckdb


TEST_KUZU_DB = Path.cwd().joinpath("tmp")


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        db = kuzu.Database(TEST_KUZU_DB)
        self.kconn = kuzu.Connection(db)

        self.dconn = duckdb.connect(DB_PATH)

        return super().setUp()

    def tearDown(self):
        self.kconn.close()
        shutil.rmtree(TEST_KUZU_DB, ignore_errors=True)
        return super().tearDown()
