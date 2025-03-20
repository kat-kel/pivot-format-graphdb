from pydantic import Field

from app.data_models.base import BaseDataModel


class PersonModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
