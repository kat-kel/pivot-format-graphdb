from duckdb import DuckDBPyConnection
from kuzu import Connection

from app.models.edges import (
    Builder as EdgeBuilder,
    is_part_of_storyverse,
    is_modeled_on,
)

ALL_EDGES = [
    is_part_of_storyverse.StoryIsPartOfStoryverse,
    is_part_of_storyverse.StoryverseIsPartOfStoryverse,
    is_modeled_on.IsModeledOn,
]


def build_all_edges(kconn: Connection, dconn: DuckDBPyConnection) -> None:
    builder = EdgeBuilder(kconn=kconn, dconn=dconn)
    for edge_type in ALL_EDGES:
        builder(edge=edge_type)
