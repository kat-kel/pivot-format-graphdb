from pydantic import Field
from app.models.base import BaseDataModel

from typing import Optional, List

from app.models.part import PartModel
from app.models.text import TextModel
from app.models.document import DocumentModel
from app.models.term import TermModel
from app.models.scripta import ScriptaModel
from app.models.person import PersonModel


class WitnessModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    is_manifestation_of: Optional[TextModel] = Field(
        validation_alias="is_manifestation_of H-ID",
        default=None,
        description="TextTable",
    )
    observed_on_pages: Optional[List[PartModel]] = Field(
        validation_alias="observed_on_pages H-ID", default=[], description="Part"
    )
    last_observed_in_doc: Optional[DocumentModel] = Field(
        validation_alias="last_observed_in_doc H-ID",
        default=None,
        description="DocumentTable",
    )
    is_unobserved: Optional[TermModel] = Field(
        validation_alias="is_unobserved TRM-ID",
        default=None,
    )
    used_to_follow_fragment: Optional["WitnessModel"] = Field(
        validation_alias="used_to_follow_fragment H-ID",
        default=None,
        description="Witness",
    )
    used_to_follow_witness: Optional["WitnessModel"] = Field(
        validation_alias="used_to_follow_witness H-ID",
        default=None,
        description="Witness",
    )
    preferred_siglum: Optional[str] = Field(default=None)
    alternative_sigla: Optional[List[str]] = Field(default=None)
    status_witness: Optional[TermModel] = Field(
        validation_alias="status_witness TRM-ID",
        default=None,
    )
    is_excerpt: Optional[TermModel] = Field(
        validation_alias="is_excerpt TRM-ID",
        default=None,
    )
    regional_writing_style: Optional[ScriptaModel] = Field(
        validation_alias="regional_writing_style H-ID",
        default=None,
        description="Scripta",
    )
    date_of_creation: Optional[dict | str] = Field(
        validation_alias="date_of_creation_TEMPORAL",
        default=None,
    )
    date_of_creation_certainty: Optional[TermModel] = Field(
        validation_alias="date_of_creation_certainty TRM-ID",
        default=None,
    )
    date_freetext: Optional[str] = Field(default=None)
    scribe: Optional[List[PersonModel]] = Field(
        validation_alias="scribe H-ID",
        default=None,
        description="Person",
    )
    number_of_hands: Optional[int] = Field(default=None)
    scribe_note: Optional[str] = Field(default=None)
    # place_of_creation <-- add later
    described_at_URL: Optional[List[str]] = Field(default=None)
