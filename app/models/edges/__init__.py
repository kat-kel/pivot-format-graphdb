from dataclasses import dataclass
from kuzu import Connection, QueryResult
from duckdb import DuckDBPyConnection
from polars import DataFrame


@dataclass
class Edge:
    name: str
    from_node: str
    to_node: str
    metadata: list[str]
    duckdb_query: str


class EdgeBuilder:
    def __init__(self, kconn: Connection, dconn: DuckDBPyConnection):
        self.kconn = kconn
        self.dconn = dconn

    @classmethod
    def create_statement(cls, edge: Edge) -> str:
        return f"""
CREATE REL TABLE IF NOT EXISTS {edge.name} (
    FROM {edge.from_node}
    TO {edge.to_node},
    {', '.join(edge.metadata)}
)
"""

    @classmethod
    def insert_statement(cls, edge: Edge) -> str:
        return f"COPY {edge.name} FROM df"

    def __call__(
        self, edge: Edge, drop: bool = False, fill_null: bool = True
    ) -> QueryResult:
        # Build the edge table in the connected Kuzu database
        self.build_edge_table(edge=edge, drop=drop)

        # Select data from the connected DuckDB database
        df = self.select_data_from_duckdb(edge=edge)
        if fill_null:
            df = df.fill_null("")

        # Insert the node's data into the connected Kuzu database
        self.insert_data(edge=edge)

        query = f"MATCH ()-[r:{edge.name}]->() RETURN r"
        return self.kconn.execute(query)

    def build_edge_table(self, edge: Edge, drop: bool) -> QueryResult:
        creation_stmt = self.create_statement(edge=edge)
        if drop:
            self.kconn.execute(f"DROP TABLE IF EXISTS {edge.name}")
        r = self.kconn.execute(creation_stmt)
        return r

    def select_data_from_duckdb(self, edge: Edge) -> DataFrame:
        return self.dconn.sql(edge.duckdb_query).pl()

    def insert_data(self, edge: Edge) -> None:
        query = self.insert_statement(edge=edge)
        try:
            self.kconn.execute(query)
        except Exception as e:
            print(query)
            raise e
