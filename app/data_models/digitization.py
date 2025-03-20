from pydantic import Field, computed_field
from typing import Optional

from app.data_models.base import BaseDataModel


class DigitizationModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    uri: Optional[str] = Field(
        alias="URI",
    )
    iiif: Optional[str] = Field(
        alias="IIIF",
    )
    ark: Optional[str] = Field(
        alias="ARK",
    )

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"digitization_{self.id}"
