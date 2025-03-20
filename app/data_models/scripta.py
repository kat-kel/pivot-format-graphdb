from pydantic import Field, computed_field

from typing import Optional, List
from app.data_models.term import TermModel
from app.data_models.place import PlaceModel
from app.data_models.base import BaseDataModel


class ScriptaModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    preferred_name: str
    description: Optional[str] = Field(default=None)
    language: Optional[TermModel] = Field(
        default=None,
        alias="language_COLUMN TRM-ID",
    )
    region: Optional[PlaceModel] = Field(
        default=None,
        alias="region H-ID",
        json_schema_extra={
            "model": PlaceModel,
            "table": "Place",
        },
    )
    region_note: Optional[str] = Field(default=None)
    described_at_URL: List[Optional[str]] = Field(default=[])

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"scripta_{self.id}"
