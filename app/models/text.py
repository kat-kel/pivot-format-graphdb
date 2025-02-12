from pydantic import Field

from typing import Optional, List

from .base import BaseDataModel
from .term import TermModel
from .story import StoryModel
from .genre import GenreModel
from .scripta import ScriptaModel
from .person import PersonModel


class TextModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    language: Optional[TermModel] = Field(
        default=None,
        validation_alias="language_COLUMN TRM-ID",
    )
    literary_form: Optional[TermModel] = Field(
        default=None,
        validation_alias="literary_form TRM-ID",
    )
    is_hypothetical: Optional[TermModel] = Field(
        default=None,
        validation_alias="is_hypothetical TRM-ID",
    )
    alternative_names: List[Optional[str]] = Field(
        default=[],
    )
    is_expression_of: Optional[StoryModel] = Field(
        default=None,
        validation_alias="is_expression_of H-ID",
        json_schema_extra={
            "model": StoryModel,
            "table": "Story",
        },
    )
    peripheral: Optional[TermModel] = Field(
        default=None,
        validation_alias="peripheral TRM-ID",
    )
    genre: Optional[GenreModel] = Field(
        default=None,
        validation_alias="specific_genre H-ID",
        json_schema_extra={
            "model": GenreModel,
            "table": "Genre",
        },
    )
    length: Optional[int] = Field(default=None)
    length_note: Optional[str] = Field(
        default=None,
        validation_alias="length_freetext",
    )
    verse_type: List[Optional[TermModel]] = Field(
        default=[],
        validation_alias="verse_type TRM-ID",
    )
    rhyme_type: List[Optional[TermModel]] = Field(
        default=[],
        validation_alias="rhyme_type TRM-ID",
    )
    is_derived_from: List[Optional[int]] = Field(
        default=[],
        validation_alias="is_derived_from H-ID",
        json_schema_extra={
            "model": None,  # Do not make recursive nest
            "table": None,  # Do not make recursive nest
        },
    )
    derivation_note: Optional[str] = Field(
        default=None,
        validation_alias="nature_of_derivations",
    )
    tradition_status: Optional[TermModel] = Field(
        default=None,
        validation_alias="tradition_status TRM-ID",
    )
    status_notes: Optional[str] = Field(default=None)
    # in_stemma <-- add later
    has_lost_older_version: Optional[TermModel] = Field(
        default=None,
        validation_alias="has_lost_older_version TRM-ID",
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
        default=None,
        validation_alias="date_of_creation_TEMPORAL",
    )
    date_of_creation_certainty: Optional[TermModel] = Field(
        default=None,
        validation_alias="date_of_creation_certainty TRM-ID",
    )
    date_freetext: Optional[str] = Field(default=None)
    is_written_by: List[Optional[PersonModel]] = Field(
        default=[],
        validation_alias="is_written_by H-ID",
        json_schema_extra={
            "model": PersonModel,
            "table": "Person",
        },
    )
    is_adapted_by: List[Optional[PersonModel]] = Field(
        default=[],
        validation_alias="is_adapted_by H-ID",
        json_schema_extra={
            "model": PersonModel,
            "table": "Person",
        },
    )
    # place_of_creation <-- add later
    described_at_URL: List[Optional[str]] = Field(default=[])
