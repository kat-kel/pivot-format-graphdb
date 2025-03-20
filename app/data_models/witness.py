from pydantic import Field, BeforeValidator, computed_field
from app.data_models.base import BaseDataModel

from typing import Optional, List, Annotated
import ast

from app.data_models.part import PartModel
from app.data_models.text import TextModel
from app.data_models.document import DocumentModel
from app.data_models.term import TermModel
from app.data_models.scripta import ScriptaModel
from app.data_models.person import PersonModel
from app.data_models.date import DateObject
from app.database import DBConn

# Recursive fields
USED_TO_FOLLOW_FRAGMENT = "used_to_follow_fragment H-ID"
USED_TO_FOLLOW_WITNESS = "used_to_follow_witness H-ID"

# Table name
TABLE_NAME = "Witness"


def value_to_dict(value: str | None | dict) -> dict | None:
    if value and isinstance(value, dict):
        return value
    elif value:
        return ast.literal_eval(value)


class WitnessModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    is_manifestation_of: Optional[TextModel] = Field(
        default=None,
        alias="is_manifestation_of H-ID",
        json_schema_extra={
            "model": TextModel,
            "table": "TextTable",
        },
    )
    observed_on_pages: List[Optional[PartModel]] = Field(
        default=[],
        alias="observed_on_pages H-ID",
        json_schema_extra={
            "model": PartModel,
            "table": "Part",
        },
    )
    last_observed_in_doc: Optional[DocumentModel] = Field(
        default=None,
        alias="last_observed_in_doc H-ID",
        json_schema_extra={
            "model": DocumentModel,
            "table": "DocumentTable",
        },
    )
    is_unobserved: Optional[TermModel] = Field(
        default=None,
        alias="is_unobserved TRM-ID",
    )
    used_to_follow_fragment: Optional[int] = Field(
        default=None,
        alias="used_to_follow_fragment H-ID",
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    used_to_follow_witness: Optional[int] = Field(
        default=None,
        alias="used_to_follow_witness H-ID",
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    preferred_siglum: Optional[str] = Field(default=None)
    alternative_sigla: Optional[List[str]] = Field(default=None)
    status_witness: Optional[TermModel] = Field(
        default=None,
        alias="status_witness TRM-ID",
    )
    is_excerpt: Optional[TermModel] = Field(
        default=None,
        alias="is_excerpt TRM-ID",
    )
    regional_writing_style: Optional[ScriptaModel] = Field(
        default=None,
        alias="regional_writing_style H-ID",
        json_schema_extra={
            "model": ScriptaModel,
            "table": "Scripta",
        },
    )
    date_of_creation: Annotated[
        Optional[DateObject], BeforeValidator(value_to_dict)
    ] = Field(
        alias="date_of_creation_TEMPORAL",
        default=None,
    )
    date_of_creation_certainty: Optional[TermModel] = Field(
        default=None,
        alias="date_of_creation_certainty TRM-ID",
    )
    date_freetext: Optional[str] = Field(default=None)
    scribe: List[Optional[PersonModel]] = Field(
        default=[],
        alias="scribe H-ID",
        json_schema_extra={"model": PersonModel, "table": "Person"},
    )
    number_of_hands: Optional[int] = Field(default=None)
    scribe_note: Optional[str] = Field(default=None)
    # place_of_creation <-- add later
    described_at_URL: List[Optional[str]] = Field(default=[])

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"witness_{self.id}"

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn):
        if row_dict[USED_TO_FOLLOW_FRAGMENT]:
            row = db.get_by_id(table=TABLE_NAME, hid=row_dict[USED_TO_FOLLOW_FRAGMENT])
            nested_dict = cls.build_nested_dict(row_dict=row, db=db)
            row_dict.update({USED_TO_FOLLOW_FRAGMENT: nested_dict})
        if row_dict[USED_TO_FOLLOW_WITNESS]:
            row = db.get_by_id(table=TABLE_NAME, hid=row_dict[USED_TO_FOLLOW_WITNESS])
            nested_dict = cls.build_nested_dict(row_dict=row, db=db)
            row_dict.update({USED_TO_FOLLOW_WITNESS: nested_dict})
        return super().build_nested_dict(row_dict=row_dict, db=db)
