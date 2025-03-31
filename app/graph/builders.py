from duckdb import DuckDBPyConnection

# ============= EDGES ============= #
from app.graph.edges import (
    EdgeBuilder,
    has_genre,
    has_language,
    has_parent_genre,
    is_expression_of,
    is_manifestation_of,
    is_modeled_on,
    is_part_of_storyverse,
)

# ============= NODES ============= #
from app.graph.nodes import NodeBuilder
from app.graph.nodes.genre import Genre
from app.graph.nodes.story import Story
from app.graph.nodes.storyverse import Storyverse
from app.graph.nodes.term import Language
from app.graph.nodes.text import Text
from app.graph.nodes.witness import Witness
from kuzu import Connection

ALL_EDGES = [
    is_modeled_on.IsModeledOn,
    is_part_of_storyverse.IsPartOfStoryverse,
    has_language.TextHasLanguage,
    is_expression_of.TextIsExpressionOf,
    has_parent_genre.GenreHasParent,
    has_genre.TextHasGenre,
    is_manifestation_of.WitnessIsManifestationOf,
]

ALL_NODES = [
    Story,
    Storyverse,
    Text,
    Language,
    Genre,
    Witness,
]


def create_all_edges(
    kconn: Connection, dconn: DuckDBPyConnection, edges=ALL_EDGES
) -> None:
    builder = EdgeBuilder(kconn=kconn, dconn=dconn)
    for edge in edges:
        try:
            builder(edge=edge)
        except RuntimeError as e:
            print(edge)
            raise e


def create_all_nodes(
    kconn: Connection, dconn: DuckDBPyConnection, nodes=ALL_NODES
) -> None:
    builder = NodeBuilder(kconn=kconn, dconn=dconn)
    for node in nodes:
        try:
            builder(node=node)
        except RuntimeError as e:
            print(node)
            raise e
