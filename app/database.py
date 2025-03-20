from pathlib import Path

import duckdb

from config import DB_PATH


class DBConn:
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

    def _execute(self, query: str, parameters: list | None = None) -> None:
        try:
            self.conn.execute(query=query, parameters=parameters)
        except Exception as e:
            print(query)
            print(parameters)
            raise e

    def select_all(self, query: str) -> list[dict] | list:
        rel = self._query(query)
        if not rel:
            return []
        keys = rel.columns
        values = rel.fetchall()
        return [{k: v for k, v in zip(keys, val)} for val in values]

    def select_one(self, query: str) -> dict:
        if not query.lower().endswith("limit 1") and not query.lower().endswith(
            "limit 1;"
        ):
            query += " LIMIT 1"
        rel = self._query(query)
        if not rel:
            return
        keys = rel.columns
        values = rel.fetchone()
        return {k: v for k, v in zip(keys, values)}

    def get_by_id(self, table: str, hid: int) -> dict:
        q = f"""
SELECT * FROM {table}
WHERE "H-ID" = {hid}
"""
        return self.select_one(q)
