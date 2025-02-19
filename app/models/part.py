from pydantic import Field
from typing import Optional, List

from .physdesc import PhysDescModel
from .document import DocumentModel
from .term import TermModel
from .base import BaseDataModel
from .pages import PageRange


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
    page_ranges: Optional[List[PageRange]] = Field(default=None)

    @classmethod
    def build_nested_dict(cls, row_dict, db):
        modeled_pages = []
        for pr in row_dict["page_ranges"]:
            pages = PageRange.validate(
                page_str=pr,
                part_id=row_dict["H-ID"],
                db=db,
            )
            modeled_pages.append(pages)
        row_dict["page_ranges"] = modeled_pages
        return super().build_nested_dict(row_dict=row_dict, db=db)
