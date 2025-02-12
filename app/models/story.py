from pydantic import Field
from typing import Optional, List

from .storyverse import StoryverseModel
from .term import TermModel
from .base import BaseDataModel


class StoryModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    is_part_of_storyverse: List[Optional[StoryverseModel]] = Field(
        default=[],
        validation_alias="is_part_of_storyverse H-ID",
        json_schema_extra={
            "model": StoryverseModel,
            "table": "Storyverse",
        },
    )
    alternative_names: List[Optional[str]] = Field(default=[])
    matter: Optional[TermModel] = Field(
        default=None,
        validation_alias="matter TRM-ID",
    )
    is_modeled_on: List[Optional[int]] = Field(
        default=[],
        validation_alias="is_modeled_on H-ID",
        json_schema_extra={
            "model": None,  # Do not make recursive nest
            "table": None,  # Do not make recursive nest
        },
    )
    described_at_URL: List[Optional[str]] = Field(default=[])
