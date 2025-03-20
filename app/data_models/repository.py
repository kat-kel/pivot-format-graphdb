from pydantic import Field, computed_field

from typing import List, Optional
from app.data_models.place import PlaceModel
from app.data_models.base import BaseDataModel


class RepositoryModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    preferred_name: Optional[str] = Field(default=None)
    label_name: Optional[str] = Field(default=None)
    city: Optional[PlaceModel] = Field(
        default=None,
        alias="city H-ID",
        json_schema_extra={
            "model": PlaceModel,
            "table": "Place",
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    viaf: Optional[float] = Field(
        default=None,
        alias="VIAF",
    )
    isni: Optional[str] = Field(
        default=None,
        alias="ISNI",
    )
    biblissima_identifier: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"repository_{self.id}"
