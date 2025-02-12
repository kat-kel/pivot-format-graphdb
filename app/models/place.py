from pydantic import Field

from typing import Optional
from .term import TermModel
from .base import BaseDataModel


class PlaceModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    place_name: Optional[str] = Field(default=None)
    administrative_region: Optional[str] = Field(default=None)
    country: Optional[TermModel] = Field(
        default=None,
        validation_alias="country TRM-ID",
    )
    place_type: Optional[str] = Field(default=None)
    location_mappable: Optional[str] = Field(default=None)
