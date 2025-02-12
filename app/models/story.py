from pydantic import Field

from .storyverse import StoryverseModel
from .term import TermModel
from typing import Optional, List
from .base import BaseDataModel


class StoryModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    is_part_of_storyverse: Optional[List[StoryverseModel]] = Field(
        default=None,
        validation_alias="is_part_of_storyverse H-ID",
        json_schema_extra={
            "model": StoryverseModel,
            "table": "Storyverse",
        },
    )
    alternative_names: Optional[List[str]] = Field(default=None)
    matter: Optional[TermModel] = Field(
        default=None,
        validation_alias="matter TRM-ID",
    )
    is_modeled_on: Optional[List[int]] = Field(
        default=None,
        validation_alias="is_modeled_on H-ID",
    )
    described_at_URL: Optional[str] = Field(default=None)
