from kuzu import Connection
from typing import Optional

from pydantic import BaseModel, Field


class LanguageTerm(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)


def fetch_language(conn: Connection, id: int) -> LanguageTerm:
    query = f"""
MATCH (t:Text)-[r:HAS_LANGAUGE]-(l:Language) WHERE t.id = {id} RETURN l
"""
    response = conn.execute(query)
    while response.has_next():
        match = response.get_next()
        if len(match) == 1:
            return LanguageTerm.model_validate(match[0])
