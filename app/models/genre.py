from pydantic import Field

from .base import BaseDataModel


class GenreModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
