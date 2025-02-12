from pydantic import Field

from typing import Optional, List
from .base import BaseDataModel


class StoryverseModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    preferred_name: str
    member_of_cycle: List[Optional[int]] = Field(
        default=[],
        validation_alias="member_of_cycle H-ID",
        json_schema_extra={
            "model": None,  # Do not make recursive nest
            "table": None,  # Do not make recursive nest
        },
    )
    alternative_names: Optional[str] = Field(default=None)
    described_at_URL: List[Optional[str]] = Field(default=[])
