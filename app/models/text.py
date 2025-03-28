from dataclasses import dataclass
from kuzu import Connection
from typing import Iterator

from app.graph.nodes.text import Text as TextNode
from app.graph.nodes.term import Language as LanguageNode
from app.graph.nodes.genre import Genre as GenreNode
from app.graph.data.terms import LanguageDataModel
from app.graph.data.date import TemporalDataModel


def iterate_texts(conn: Connection) -> Iterator[dict]:
    text_query = f"""
    MATCH (text:{TextNode.name})
    RETURN text
        """
    query_result = conn.execute(query=text_query)
    while query_result.has_next():
        row = query_result.get_next()
        if row:
            yield row[0]


class TextNodeParser:

    def __init__(self, conn: Connection, text: dict):
        self.conn = conn
        self._data = text

    def _load_data_model(cls, data: dict, model: dataclass) -> dataclass:
        i = {k: data.get(k) for k in model.__annotations__}
        return model(**i)

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def title(self) -> str:
        return self._data["name"]

    @property
    def language(self) -> LanguageDataModel:
        query = f"""
MATCH (t:{TextNode.name})-[]->(l:{LanguageNode.name}) WHERE t.id = {id}
RETURN l
        """
        result = self.conn.execute(query=query)
        if result.has_next():
            match = result.get_next()[0]
            return self._load_data_model(data=match, model=LanguageDataModel)

    @property
    def creation_date(self) -> TemporalDataModel:
        temporal = self._data["creation_date_temporal"]
        return TemporalDataModel.load(dict_str=temporal)

    @property
    def genre_genealogy(self) -> list[dict]:
        genre_id =

    def _get_genre_tree(self, id: int):
        query = f"""
MATCH (t:{Text.name})-[]->(g:{Genre.name}) WHERE t.id = {id}
RETURN g
"""
        result = self.conn.execute(query=query)
        print(result.get_as_df())
        if result.has_next():
            match = result.get_next()[0]
            return match
