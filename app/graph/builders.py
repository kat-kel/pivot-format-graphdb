from kuzu import Connection
from duckdb import DuckDBPyConnection

# ============ BUILDER ============ #
from app.graph.edges import EdgeBuilder
from app.graph.nodes import NodeBuilder

# ============= EDGES ============= #
from app.graph.edges import is_modeled_on
from app.graph.edges import is_part_of_storyverse
from app.graph.edges import has_language
from app.graph.edges import is_expression_of
from app.graph.edges import has_parent_genre
from app.graph.edges import has_genre
from app.graph.edges import is_manifestation_of


# ============= NODES ============= #
from app.graph.nodes.story import Story
from app.graph.nodes.storyverse import Storyverse
from app.graph.nodes.text import Text
from app.graph.nodes.term import Language
from app.graph.nodes.genre import Genre
from app.graph.nodes.witness import Witness

ALL_EDGES = [
    is_modeled_on.IsModeledOn,
    is_part_of_storyverse.StoryIsPartOfStoryverse,
    is_part_of_storyverse.StoryverseIsPartOfStoryverse,
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
        builder(edge=edge)


def create_all_nodes(
    kconn: Connection, dconn: DuckDBPyConnection, nodes=ALL_NODES
) -> None:
    builder = NodeBuilder(kconn=kconn, dconn=dconn)
    for node in nodes:
        builder(node=node)
