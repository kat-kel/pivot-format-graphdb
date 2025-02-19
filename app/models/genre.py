from pydantic import Field
from typing import List, Optional
from .base import BaseDataModel
from app.database import DBConn

# Recusrive fields
PARENT_GENRE = "parent_genre H-ID"

# Table name
TABLE_NAME = "Genre"


class GenreModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    parent_genre: Optional["GenreModel"] = Field(
        default=None,
        validation_alias=PARENT_GENRE,
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    description: str
    archetype: List[Optional[str]] = Field(default=[])
    described_at_URL: List[Optional[str]] = Field(default=[])

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn):
        if row_dict[PARENT_GENRE]:
            parent_genre = db.get_by_id(table=TABLE_NAME, hid=row_dict[PARENT_GENRE])
            row_dict.update({PARENT_GENRE: parent_genre})
        return super().build_nested_dict(row_dict=row_dict, db=db)
