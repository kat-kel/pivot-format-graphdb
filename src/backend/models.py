from typing import List

from pydantic import BaseModel, Field


class Story(BaseModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    matter: str
    review_status: str
    review_note: str | None = Field(default=None)


class Text(BaseModel):
    id: int = Field(validation_alias="H-ID")
    language: str | None = Field(default=None)
    literary_form: str
    claim_freetext: str | None = Field(default=None)
    is_expression_of: int | None = Field(
        default=None, validation_alias="is_expression_of H-Id"
    )
    peripheral: str | None = Field(default=None)
    specific_genre: int | None = Field(
        default=None, validation_alias="specific_genre H-ID"
    )
    tradition_status: str
    status_notes: str | None = Field(default=None)
    is_derived_from: int | None = Field(
        default=None, validation_alias="is_derived_from H-ID"
    )
    nature_of_derivations: str | None = Field(default=None)
    has_lost_older_version: str | None = Field(default=None)
    regional_writing_style: int | None = Field(
        default=None, validation_alias="regional_writing_style H-ID"
    )
    scripta_freetext: str | None = Field(default=None)
    date_of_creation_temporal: dict | str | None = Field(default=None)
    date_of_creation_certainty: str | None = Field(default=None)
    date_of_creation_source: str | None = Field(default=None)
    review_status: str
    review_note: str | None = Field(default=None)


class Witness(BaseModel):
    id: int = Field(validation_alias="H-ID")
    is_manifestation_of: int = Field(validation_alias="is_manifestation_of H-ID")
    observed_on_pages: int | List[int] | None = Field(
        default=[], validation_alias="observed_on_pages H-ID"
    )
    is_unobserved: str
    preferred_siglum: str
    alternative_sigla: str | List[str] | None
    status_witness: str
    is_excerpt: str
    date_of_creation_temporal: dict | str | None = Field(default=None)
    date_of_creation_certainty: str | None = Field(default=None)
    date_of_creation_source: str | None = Field(default=None)
    date_freetext: str | None = Field(default=None)
    review_status: str
    review_note: str | None = Field(default=None)
    described_at_url: str | None = Field(default=None)


class Part(BaseModel):
    is_inscribed_on: int = Field(validation_alias="is_inscribed_on H-ID")
    div_order: int
    number_of_verses: float | None = Field(default=None)
    part_of_text: str | None = Field(default=None)
    volume_number: str | None = Field(default=None)
    physical_description: int | None = Field(
        validation_alias="physical_description H-ID", default=None
    )
    number_of_lines: int | None = Field(default=None)
    verses_per_line: str | None = Field(default=None)
    lines_are_incomplete: str
    page_ranges: str | List[str]
    review_status: str
    review_note: str | None = Field(default=None)
