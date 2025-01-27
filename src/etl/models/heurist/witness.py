from typing import List, Optional

from pydantic import BaseModel, Field

from src.etl.models.heurist.utils import TemporalObject


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
    date_of_creation_temporal: TemporalObject | None = Field(default=None)
    date_of_creation_certainty: Optional[str] = Field(default=None)
    date_of_creation_source: Optional[str] = Field(default=None)
    date_of_creation: Optional[list] = Field(default=[])
    date_freetext: Optional[str] = Field(default=None)
    review_status: str
    review_note: str | None = Field(default=None)
    described_at_url: str | None = Field(default=None)
