from kuzu import Connection
from duckdb import DuckDBPyConnection

# ============ BUILDER ============ #
from app.models.edges import EdgeBuilder
from app.models.nodes import NodeBuilder

# ============= EDGES ============= #
from app.models.edges import is_modeled_on
from app.models.edges import is_part_of_storyverse
from app.models.edges import has_language
from app.models.edges import is_expression_of


# ============= NODES ============= #
from app.models.nodes.story import Story
from app.models.nodes.storyverse import Storyverse
from app.models.nodes.text import Text
from app.models.nodes.term import Language

ALL_EDGES = [
    is_modeled_on.IsModeledOn,
    is_part_of_storyverse.StoryIsPartOfStoryverse,
    is_part_of_storyverse.StoryverseIsPartOfStoryverse,
    has_language.TextHasLanguage,
    is_expression_of.TextIsExpressionOf,
]

ALL_NODES = [
    Story,
    Storyverse,
    Text,
    Language,
]


def create_all_edges(
    kconn: Connection, dconn: DuckDBPyConnection, edges=ALL_EDGES
) -> None:
    builder = EdgeBuilder(kconn=kconn, dconn=dconn)
    for edge in edges:
        builder(edge=edge)


def create_all_nodes(
    kconn: Connection, dconn: DuckDBPyConnection, nodes=ALL_NODES
) -> None:
    builder = NodeBuilder(kconn=kconn, dconn=dconn)
    for node in nodes:
        builder(node=node)
