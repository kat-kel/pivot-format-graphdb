from pydantic import BaseModel, Field


class Story(BaseModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    matter: str
    review_status: str
    review_note: str | None = Field(default=None)
