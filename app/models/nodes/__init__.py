from dataclasses import dataclass
from kuzu import Connection, QueryResult
from duckdb import DuckDBPyConnection
from polars import DataFrame


@dataclass
class Node:
    name: str
    duckdb_query: str
    pk: str
    metadata: list[str]


class Builder:
    def __init__(self, kconn: Connection, dconn: DuckDBPyConnection) -> None:
        self.kconn = kconn
        self.dconn = dconn

    @classmethod
    def create_statement(cls, node: Node) -> str:
        params = node.metadata + [f"PRIMARY KEY({node.pk})"]
        return f"""
    CREATE NODE TABLE {node.name}
    (
        {', '.join(params)}
    )
            """

    @classmethod
    def insert_statement(cls, node: Node) -> str:
        return f"COPY {node.name} FROM df"

    def __call__(
        self, node: Node, drop: bool = True, fill_null: bool = True
    ) -> QueryResult:
        # Build the node table in the connected Kuzu database
        self.build_node_table(node=node, drop=drop)

        # Select data from the connected DuckDB database
        df = self.select_data_from_duckdb(node=node)
        if fill_null:
            df = df.fill_null("")

        # Insert the node's data into the connected Kuzu database
        self.insert_data(node=node)

        query = f"MATCH (n:{node.name}) return n"
        return self.kconn.execute(query)

    def build_node_table(self, node: Node, drop: bool) -> QueryResult:
        creation_stmt = self.create_statement(node=node)
        if drop:
            self.kconn.execute(f"DROP TABLE IF EXISTS {node.name}")
        r = self.kconn.execute(creation_stmt)
        return r

    def select_data_from_duckdb(self, node: Node) -> DataFrame:
        return self.dconn.sql(node.duckdb_query).pl()

    def insert_data(self, node: Node) -> None:
        query = self.insert_statement(node=node)
        try:
            self.kconn.execute(query)
        except Exception as e:
            print(query)
            raise e
