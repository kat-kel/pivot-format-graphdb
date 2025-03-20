from pydantic import Field, computed_field

from typing import Optional, List
from app.data_models.repository import RepositoryModel
from app.data_models.digitization import DigitizationModel
from app.data_models.base import BaseDataModel


class DocumentModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    current_shelfmark: Optional[str] = Field(default=None)
    location: Optional[RepositoryModel] = Field(
        default=None,
        alias="location H-ID",
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
        alias="digitization H-ID",
        json_schema_extra={
            "model": DigitizationModel,
            "table": "Digitization",
        },
    )
    described_at_URL: Optional[List[str]] = Field(default=None)
    online_catalogue_URL: Optional[str] = Field(default=None)
    ARK: Optional[str] = Field(default=None)

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"document_{self.id}"
