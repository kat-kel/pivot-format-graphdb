from pydantic import Field

from typing import Optional, List
from .base import BaseDataModel


class StoryverseModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    member_of_cycle: Optional[List[int]] = Field(
        default=None,
        validation_alias="member_of_cycle H-ID",
    )
    alternative_names: Optional[str] = Field(default=None)
    described_at_URL: Optional[List[str]] = Field(default=None)
