from pydantic import Field
from typing import Optional

from .base import BaseDataModel


class DigitizationModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    uri: Optional[str] = Field(validation_alias="URI")
    iiif: Optional[str] = Field(validation_alias="IIIF")
    ark: Optional[str] = Field(validation_alias="ARK")
