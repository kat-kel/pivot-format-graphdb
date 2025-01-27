from typing import List

from pydantic import BaseModel, Field


class Part(BaseModel):
    id: int = Field(validation_alias="H-ID")
    is_inscribed_on: int = Field(validation_alias="is_inscribed_on H-ID")
    div_order: int
    number_of_verses: float | None = Field(default=None)
    part_of_text: str | None = Field(default=None)
    volume_number: str | None = Field(default=None)
    physical_description: int | None = Field(
        validation_alias="physical_description H-ID", default=None
    )
    number_of_lines: int | None = Field(default=None)
    verses_per_line: str | None = Field(default=None)
    lines_are_incomplete: str
    page_ranges: str | List[str]
    review_status: str
    review_note: str | None = Field(default=None)
