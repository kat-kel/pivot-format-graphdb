from kuzu import Connection, QueryResult
from duckdb import DuckDBPyConnection

from app.models.nodes import Node, create_statement as create_node
from app.models.edges import Edge, create_statement as create_edge


class Builder:
    """Class for building node and edge tables in Kuzu database connection from data
    stored in DuckDB database connection."""

    def __init__(self, kconn: Connection, dconn: DuckDBPyConnection) -> None:
        self.kconn = kconn
        self.dconn = dconn

    def build_node(self, data: Node) -> None:
        """"""
        creation_stmt = create_node(data=data)
        self._rebuild_table(name=data.name, creation_stmt=creation_stmt)
        self._insert_data(data=data)

    def build_edge(self, data: Edge) -> None:
        creation_stmt = create_edge(data=data)
        self._rebuild_table(name=data.name, creation_stmt=creation_stmt, drop=True)
        self._insert_data(data=data)

    def _rebuild_table(
        self, name: str, creation_stmt: str, drop: bool = False
    ) -> QueryResult:
        # Drop table if exists
        if drop:
            self.kconn.execute(f"DROP TABLE IF EXISTS {name}")
        r = self.kconn.execute(creation_stmt)
        return r

    def _insert_data(self, data: Edge | Node) -> None:
        # Select the edge data from the DuckDB database
        df = self.dconn.sql(data.duckdb_query).pl()
        df = df.fill_null("")
        print(df)
        # Ingest the polars dataframe in the Kuzu DB table
        try:
            query = f"COPY {data.name} FROM df"
            self.kconn.execute(query)
        except Exception as e:
            print(query)
            raise e
