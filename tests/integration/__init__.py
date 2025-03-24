import unittest
import kuzu
import shutil
from pathlib import Path
from app import HEURIST_DB
import duckdb


TEST_KUZU_DB = Path.cwd().joinpath("tmp")


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        db = kuzu.Database(TEST_KUZU_DB)
        self.kconn = kuzu.Connection(db)

        self.dconn = duckdb.connect(HEURIST_DB)

        return super().setUp()

    def tearDown(self):
        self.kconn.close()
        shutil.rmtree(TEST_KUZU_DB, ignore_errors=True)
        return super().tearDown()
