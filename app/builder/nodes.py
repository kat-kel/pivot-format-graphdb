from duckdb import DuckDBPyConnection
from kuzu import Connection

from app.models.nodes import Builder as NodeBuilder, story, storyverse


ALL_NODES = [
    story.Story,
    storyverse.Storyverse,
]


def build_all_nodes(kconn: Connection, dconn: DuckDBPyConnection) -> None:
    builder = NodeBuilder(kconn=kconn, dconn=dconn)
    for node_type in ALL_NODES:
        builder(node=node_type)
