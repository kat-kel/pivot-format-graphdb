from pydantic import Field, computed_field

from typing import Optional
from app.data_models.term import TermModel
from app.data_models.base import BaseDataModel


class PlaceModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    place_name: Optional[str] = Field(default=None)
    administrative_region: Optional[str] = Field(default=None)
    country: Optional[TermModel] = Field(
        default=None,
        alias="country TRM-ID",
    )
    place_type: Optional[str] = Field(default=None)
    location_mappable: Optional[str] = Field(default=None)

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"place_{self.id}"
