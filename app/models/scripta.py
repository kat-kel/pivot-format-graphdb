from pydantic import Field

from typing import Optional, List
from .term import TermModel
from .place import PlaceModel
from .base import BaseDataModel


class ScriptaModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    description: Optional[str] = Field(default=None)
    language: Optional[TermModel] = Field(
        default=None,
        validation_alias="language_COLUMN TRM-ID",
    )
    region: Optional[PlaceModel] = Field(
        default=None,
        validation_alias="region H-ID",
        json_schema_extra={
            "model": PlaceModel,
            "table": "Place",
        },
    )
    region_note: Optional[str] = Field(default=None)
    described_at_URL: List[Optional[str]] = Field(default=[])
