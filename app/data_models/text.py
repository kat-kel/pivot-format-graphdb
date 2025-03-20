from pydantic import Field, BeforeValidator, computed_field

from typing import Optional, List, Annotated
import ast

from app.data_models.base import BaseDataModel
from app.data_models.term import TermModel
from app.data_models.story import StoryModel
from app.data_models.genre import GenreModel
from app.data_models.scripta import ScriptaModel
from app.data_models.person import PersonModel
from app.data_models.date import DateObject
from app.database import DBConn

# Recusrive fields
IS_DERIVED_FROM = "is_derived_from H-ID"

# Table name
TABLE_NAME = "TextTable"


def value_to_dict(value: str | None | dict) -> dict | None:
    if value and isinstance(value, dict):
        return value
    elif value:
        return ast.literal_eval(value)


class TextModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    preferred_name: str
    language: Optional[TermModel] = Field(
        default=None,
        alias="language_COLUMN TRM-ID",
    )
    literary_form: Optional[TermModel] = Field(
        default=None,
        alias="literary_form TRM-ID",
    )
    is_hypothetical: Optional[TermModel] = Field(
        default=None,
        alias="is_hypothetical TRM-ID",
    )
    alternative_names: List[Optional[str]] = Field(
        default=[],
    )
    is_expression_of: Optional[StoryModel] = Field(
        default=None,
        alias="is_expression_of H-ID",
        json_schema_extra={
            "model": StoryModel,
            "table": "Story",
        },
    )
    peripheral: Optional[TermModel] = Field(
        default=None,
        alias="peripheral TRM-ID",
    )
    genre: Optional[GenreModel] = Field(
        default=None,
        alias="specific_genre H-ID",
        json_schema_extra={
            "model": GenreModel,
            "table": "Genre",
        },
    )
    length: Optional[int] = Field(default=None)
    length_note: Optional[str] = Field(
        default=None,
        alias="length_freetext",
    )
    verse_type: List[Optional[TermModel]] = Field(
        default=[],
        alias="verse_type TRM-ID",
    )
    rhyme_type: List[Optional[TermModel]] = Field(
        default=[],
        alias="rhyme_type TRM-ID",
    )
    is_derived_from: List[Optional["TextModel"]] = Field(
        default=[],
        alias="is_derived_from H-ID",
        json_schema_extra={
            "model": None,
            "table": TABLE_NAME,
        },
    )
    derivation_note: Optional[str] = Field(
        default=None,
        alias="nature_of_derivations",
    )
    tradition_status: Optional[TermModel] = Field(
        default=None,
        alias="tradition_status TRM-ID",
    )
    status_notes: Optional[str] = Field(default=None)
    # in_stemma <-- add later
    has_lost_older_version: Optional[TermModel] = Field(
        default=None,
        alias="has_lost_older_version TRM-ID",
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
        default=None,
        alias="date_of_creation_TEMPORAL",
    )
    date_of_creation_certainty: Optional[TermModel] = Field(
        default=None,
        alias="date_of_creation_certainty TRM-ID",
    )
    date_freetext: Optional[str] = Field(default=None)
    is_written_by: List[Optional[PersonModel]] = Field(
        default=[],
        alias="is_written_by H-ID",
        json_schema_extra={
            "model": PersonModel,
            "table": "Person",
        },
    )
    is_adapted_by: List[Optional[PersonModel]] = Field(
        default=[],
        alias="is_adapted_by H-ID",
        json_schema_extra={
            "model": PersonModel,
            "table": "Person",
        },
    )
    # place_of_creation <-- add later
    described_at_URL: List[Optional[str]] = Field(default=[])

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"text_{self.id}"

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn):
        array_of_nested_dicts = []
        for fk in row_dict[IS_DERIVED_FROM]:
            row = db.get_by_id(table=TABLE_NAME, hid=fk)
            nested_dict = cls.build_nested_dict(row_dict=row, db=db)
            array_of_nested_dicts.append(nested_dict)

        row_dict.update({IS_DERIVED_FROM: array_of_nested_dicts})

        return super().build_nested_dict(row_dict=row_dict, db=db)
