from pydantic import Field, computed_field
from typing import Optional, List

from app.data_models.storyverse import StoryverseModel
from app.data_models.term import TermModel
from app.data_models.base import BaseDataModel
from app.database import DBConn

# Recursive fields
IS_MODELED_ON = "is_modeled_on H-ID"

# Table name
TABLE_NAME = "Story"


class StoryModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    preferred_name: str
    is_part_of_storyverse: List[Optional[StoryverseModel]] = Field(
        default=[],
        alias="is_part_of_storyverse H-ID",
        json_schema_extra={
            "model": StoryverseModel,
            "table": "Storyverse",
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    matter: Optional[TermModel] = Field(
        default=None,
        alias="matter TRM-ID",
    )
    is_modeled_on: List[Optional[int]] = Field(
        default=[],
        alias=IS_MODELED_ON,
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    described_at_URL: List[Optional[str]] = Field(default=[])

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"story_{self.id}"

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn):
        array_of_nested_dicts = []
        for fk in row_dict[IS_MODELED_ON]:
            row = db.get_by_id(table=TABLE_NAME, hid=fk)
            nested_dict = cls.build_nested_dict(row_dict=row, db=db)
            array_of_nested_dicts.append(nested_dict)

        row_dict.update({IS_MODELED_ON: array_of_nested_dicts})

        return super().build_nested_dict(row_dict=row_dict, db=db)
