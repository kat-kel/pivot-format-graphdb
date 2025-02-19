from pydantic import Field
from app.models.base import BaseDataModel

from typing import Optional, List

from app.models.part import PartModel
from app.models.text import TextModel
from app.models.document import DocumentModel
from app.models.term import TermModel
from app.models.scripta import ScriptaModel
from app.models.person import PersonModel
from app.database import DBConn

# Recursive fields
USED_TO_FOLLOW_FRAGMENT = "used_to_follow_fragment H-ID"
USED_TO_FOLLOW_WITNESS = "used_to_follow_witness H-ID"

# Table name
TABLE_NAME = "Witness"


class WitnessModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    is_manifestation_of: Optional[TextModel] = Field(
        default=None,
        validation_alias="is_manifestation_of H-ID",
        json_schema_extra={
            "model": TextModel,
            "table": "TextTable",
        },
    )
    observed_on_pages: List[Optional[PartModel]] = Field(
        default=[],
        validation_alias="observed_on_pages H-ID",
        json_schema_extra={
            "model": PartModel,
            "table": "Part",
        },
    )
    last_observed_in_doc: Optional[DocumentModel] = Field(
        default=None,
        validation_alias="last_observed_in_doc H-ID",
        json_schema_extra={
            "model": DocumentModel,
            "table": "DocumentTable",
        },
    )
    is_unobserved: Optional[TermModel] = Field(
        default=None,
        validation_alias="is_unobserved TRM-ID",
    )
    used_to_follow_fragment: Optional[int] = Field(
        default=None,
        validation_alias="used_to_follow_fragment H-ID",
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    used_to_follow_witness: Optional[int] = Field(
        default=None,
        validation_alias="used_to_follow_witness H-ID",
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    preferred_siglum: Optional[str] = Field(default=None)
    alternative_sigla: Optional[List[str]] = Field(default=None)
    status_witness: Optional[TermModel] = Field(
        default=None,
        validation_alias="status_witness TRM-ID",
    )
    is_excerpt: Optional[TermModel] = Field(
        default=None,
        validation_alias="is_excerpt TRM-ID",
    )
    regional_writing_style: Optional[ScriptaModel] = Field(
        default=None,
        validation_alias="regional_writing_style H-ID",
        json_schema_extra={
            "model": ScriptaModel,
            "table": "Scripta",
        },
    )
    date_of_creation: Optional[dict | str] = Field(
        validation_alias="date_of_creation_TEMPORAL",
        default=None,
    )
    date_of_creation_certainty: Optional[TermModel] = Field(
        default=None,
        validation_alias="date_of_creation_certainty TRM-ID",
    )
    date_freetext: Optional[str] = Field(default=None)
    scribe: List[Optional[PersonModel]] = Field(
        default=[],
        validation_alias="scribe H-ID",
        json_schema_extra={"model": PersonModel, "table": "Person"},
    )
    number_of_hands: Optional[int] = Field(default=None)
    scribe_note: Optional[str] = Field(default=None)
    # place_of_creation <-- add later
    described_at_URL: List[Optional[str]] = Field(default=[])

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
