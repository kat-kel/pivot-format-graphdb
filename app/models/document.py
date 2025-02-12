from pydantic import Field

from typing import Optional, List
from .repository import RepositoryModel
from .digitization import DigitizationModel
from .base import BaseDataModel


class DocumentModel(BaseDataModel):
    id: int = Field(
        validation_alias="H-ID",
    )
    current_shelfmark: Optional[str] = Field(default=None)
    location: Optional[RepositoryModel] = Field(
        default=None,
        validation_alias="location H-ID",
        json_schema_extra={
            "model": RepositoryModel,
            "table": "Repository",
        },
    )
    collection: Optional[str] = Field(default=None)
    invented_label: Optional[str] = Field(default=None)
    is_hypothetical: Optional[str] = Field(default=None)
    claim_freetext: Optional[str] = Field(default=None)
    collection_of_fragments: Optional[str] = Field(default=None)
    old_shelfmark: List[Optional[str]] = Field(default=[])
    digitization: List[Optional[DigitizationModel]] = Field(
        default=[],
        validation_alias="digitization H-ID",
        json_schema_extra={
            "model": DigitizationModel,
            "table": "Digitization",
        },
    )
    described_at_URL: Optional[List[str]] = Field(default=None)
    online_catalogue_URL: Optional[str] = Field(default=None)
    ARK: Optional[str] = Field(default=None)
