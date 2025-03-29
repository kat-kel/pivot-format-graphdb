from kuzu import Connection, QueryResult
from duckdb import DuckDBPyConnection
from typing import Literal


CypherTypes = Literal[
    "BOOLEAN",
    "DATE",
    "DATE[]",
    "DURATION",
    "FLOAT",
    "FLOAT[]",
    "INT",
    "INT[]",
    "MAP",
    "POINT",
    "STRING",
    "STRING[]",
    "STRUCT",
]


class Metadata:
    def __init__(
        self,
        label: str,
        col: str | None = None,
        type: CypherTypes | None = None,
        temporal: bool = False,
    ):
        self.label = label
        if not col:
            self.duckdb_col = label
        else:
            self.duckdb_col = col
        self.temporal = temporal
        # If the metadata is a Heurist temporal object,
        # create a flat structured data type
        if temporal:
            self.type = """STRUCT(
start_earliest TIMESTAMP,
start_latest TIMESTAMP,
start_prob STRING,
start_cert STRING,
end_earliest TIMESTAMP,
end_latest TIMESTAMP,
end_prob STRING,
end_cert STRING,
timestamp_year TIMESTAMP,
timestamp_type STRING,
timestamp_circa BOOL,
est_min TIMESTAMP,
est_max TIMESTAMP,
est_prob STRING,
est_cert STRING
)"""
        else:
            self.type = type

    @property
    def cypher_alias(self) -> str:
        return f"{self.label} {self.type}"

    @property
    def sql_alias(self) -> str:
        if self.temporal:
            s = f"""
'start_earliest': CAST({self.duckdb_col}.start.earliest AS TIMESTAMP),
'start_latest': CAST({self.duckdb_col}.start.latest AS TIMESTAMP),
'start_prob': CAST({self.duckdb_col}.start.estProfile AS VARCHAR),
'start_cert': CAST({self.duckdb_col}.start.estDetermination AS VARCHAR),
'end_earliest': CAST({self.duckdb_col}.end.earliest AS TIMESTAMP),
'end_latest': CAST({self.duckdb_col}.end.latest AS TIMESTAMP),
'end_prob': CAST({self.duckdb_col}.end.estProfile AS VARCHAR),
'end_cert': CAST({self.duckdb_col}.end.estDetermination AS VARCHAR),
'timestamp_year': CAST({self.duckdb_col}.timestamp.in AS TIMESTAMP),
'timestamp_type': CAST({self.duckdb_col}.timestamp.type AS VARCHAR),
'timestamp_circa': CAST({self.duckdb_col}.timestamp.circa AS BOOL),
'est_min': CAST({self.duckdb_col}.estMinDate AS TIMESTAMP),
'est_max': CAST({self.duckdb_col}.estMaxDate AS TIMESTAMP),
'est_prob': CAST({self.duckdb_col}.estProfile AS VARCHAR),
'est_cert': CAST({self.duckdb_col}.estDetermination AS VARCHAR)
"""
            return f"""
            CASE WHEN "{self.duckdb_col}" IS NULL THEN NULL ELSE {{{s}}}
            END AS {self.label}"""
        elif self.type == "BOOLEAN":
            return f"""
CASE WHEN "{self.duckdb_col}" LIKE 'Yes' THEN True ELSE False
END AS {self.label}
"""
        else:
            return f'"{self.duckdb_col}" AS {self.label}'


class Node:
    def __init__(
        self,
        table_name: str,
        pk: str,
        metadata: list[Metadata],
        duckdb_query: str | None = None,
        table: str | None = None,
    ):
        self.table_name = table_name
        self.pk = pk
        self.metadata = metadata
        self.table = table
        self.duckdb_query = duckdb_query
        if not duckdb_query:
            self.duckdb_query = self.make_duckdb_query()

    def list_cypher_props(self) -> list[str]:
        return [m.cypher_alias for m in self.metadata]

    @property
    def create_statement(self) -> str:
        params = self.list_cypher_props() + [f"PRIMARY KEY ({self.pk})"]
        return f"""
    CREATE NODE TABLE {self.table_name}
    (
        {', '.join(params)}
    )"""

    def make_duckdb_query(self) -> str:
        aliases = ", ".join([m.sql_alias for m in self.metadata])
        return f"SELECT {aliases} FROM {self.table}"


class NodeBuilder:
    def __init__(self, kconn: Connection, dconn: DuckDBPyConnection) -> None:
        self.kconn = kconn
        self.dconn = dconn

    def __call__(
        self, node: Node, drop: bool = True, fill_null: bool = True
    ) -> QueryResult:
        # Build the node table in the connected Kuzu database
        if drop:
            self.kconn.execute(f"DROP TABLE IF EXISTS {node.table_name}")
        self.kconn.execute(node.create_statement)

        # Select data from the connected DuckDB database
        try:
            rel = self.dconn.sql(node.duckdb_query)
            df = rel.pl()
        except Exception as e:
            print(node.duckdb_query)
            raise e
        if fill_null:
            df = df.fill_null("")

        # Insert the DuckDB data into the Kuzu database
        query = f"COPY {node.table_name} FROM df"
        try:
            self.kconn.execute(query)
        except Exception as e:
            print(node.table_name)
            print(df)
            print(rel.select("creation_date"))
            raise e

        # Fetch the nodes createdin in the Kuzu database
        query = f"MATCH (n:{node.table_name}) return n"
        return self.kconn.execute(query)
