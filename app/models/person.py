from pydantic import Field

from .base import BaseDataModel


class PersonModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
