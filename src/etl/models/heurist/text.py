from typing import List, Optional

from pydantic import BaseModel, Field

from src.etl.models.heurist.utils import TemporalObject


class Text(BaseModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    language: Optional[str] = Field(default=None, validation_alias="language column")
    literary_form: Optional[str] = Field(default=None)
    claim_freetext: Optional[str] = Field(default=None)
    is_expression_of: Optional[int] = Field(
        default=None, validation_alias="is_expression_of H-Id"
    )
    peripheral: Optional[str] = Field(default=None)
    specific_genre: int | None = Field(
        default=None, validation_alias="specific_genre H-ID"
    )
    tradition_status: Optional[str] = Field(default=None)
    status_notes: Optional[str] = Field(default=None)
    is_derived_from: Optional[int] = Field(
        default=None, validation_alias="is_derived_from H-ID"
    )
    nature_of_derivations: Optional[str] = Field(default=None)
    has_lost_older_version: Optional[str] = Field(default=None)
    regional_writing_style: Optional[int] = Field(
        default=None, validation_alias="regional_writing_style H-ID"
    )
    scripta_freetext: Optional[str] = Field(default=None)
    date_of_creation_temporal: TemporalObject | None = Field(default=None)
    date_of_creation_certainty: Optional[str] = Field(default=None)
    date_of_creation_source: Optional[str] = Field(default=None)
    date_of_creation: Optional[list] = Field(default=[])
    date_freetext: Optional[str] = Field(default=None)
    review_status: Optional[str] = Field()
    review_note: Optional[str] = Field(default=None)
