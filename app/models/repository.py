from pydantic import Field

from typing import List, Optional
from .place import PlaceModel
from .base import BaseDataModel


class RepositoryModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: Optional[str] = Field(default=None)
    label_name: Optional[str] = Field(default=None)
    city: Optional[PlaceModel] = Field(
        default=None,
        validation_alias="city H-ID",
        json_schema_extra={
            "model": PlaceModel,
            "table": "Place",
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    viaf: Optional[float] = Field(default=None, validation_alias="VIAF")
    isni: Optional[str] = Field(default=None, validation_alias="ISNI")
    biblissima_identifier: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
