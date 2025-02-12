from pydantic import Field
from typing import Optional, List

from .physdesc import PhysDescModel
from .document import DocumentModel
from .term import TermModel
from .base import BaseDataModel


class PartModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    is_inscribed_on: Optional[DocumentModel] = Field(
        default=None,
        validation_alias="is_inscribed_on H-ID",
        json_schema_extra={
            "model": DocumentModel,
            "table": "DocumentTable",
        },
    )
    div_order: int
    number_of_verses: Optional[int] = Field(default=None)
    part_of_text: Optional[str] = Field(default=None)
    volume_number: Optional[str] = Field(default=None)
    physical_description: Optional[PhysDescModel] = Field(
        default=None,
        validation_alias="physical_description H-ID",
        json_schema_extra={
            "model": PhysDescModel,
            "table": "PhysDesc",
        },
    )
    verses_per_line: Optional[TermModel] = Field(
        default=None,
        validation_alias="verses_per_line TRM-ID",
    )
    number_of_lines: Optional[int] = Field(default=None)
    lines_are_incomplete: Optional[TermModel] = Field(
        default=None,
        validation_alias="lines_are_incomplete TRM-ID",
    )
    page_ranges: Optional[List[str]] = Field(default=None)
