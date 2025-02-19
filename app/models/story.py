from pydantic import Field
from typing import Optional, List

from .storyverse import StoryverseModel
from .term import TermModel
from .base import BaseDataModel
from app.database import DBConn

# Recursive fields
IS_MODELED_ON = "is_modeled_on H-ID"

# Table name
TABLE_NAME = "Story"


class StoryModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    is_part_of_storyverse: List[Optional[StoryverseModel]] = Field(
        default=[],
        validation_alias="is_part_of_storyverse H-ID",
        json_schema_extra={
            "model": StoryverseModel,
            "table": "Storyverse",
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    matter: Optional[TermModel] = Field(
        default=None,
        validation_alias="matter TRM-ID",
    )
    is_modeled_on: List[Optional[int]] = Field(
        default=[],
        validation_alias=IS_MODELED_ON,
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    described_at_URL: List[Optional[str]] = Field(default=[])

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn):
        array_of_nested_dicts = []
        for fk in row_dict[IS_MODELED_ON]:
            row = db.get_by_id(table=TABLE_NAME, hid=fk)
            nested_dict = cls.build_nested_dict(row_dict=row, db=db)
            array_of_nested_dicts.append(nested_dict)

        row_dict.update({IS_MODELED_ON: array_of_nested_dicts})

        return super().build_nested_dict(row_dict=row_dict, db=db)
