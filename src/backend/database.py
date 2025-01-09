from pathlib import Path

import duckdb

from src.backend.constants import DB_PATH


class DB:
    def __init__(self, fp: str | Path = DB_PATH):
        if isinstance(fp, Path):
            fp = str(fp)
        self.conn = duckdb.connect(fp)

    def _query(self, query: str) -> duckdb.DuckDBPyRelation:
        try:
            return self.conn.sql(query)
        except Exception as e:
            print(query)
            raise e

    def select(self, query: str) -> list[dict]:
        rel = self._query(query)
        keys = rel.columns
        values = rel.fetchall()
        return [{k: v for k, v in zip(keys, val)} for val in values]
