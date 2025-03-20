from pydantic import Field, computed_field
from typing import Optional, List

from app.data_models.physdesc import PhysDescModel
from app.data_models.document import DocumentModel
from app.data_models.term import TermModel
from app.data_models.base import BaseDataModel
from app.data_models.pages import PageRange


class PartModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    is_inscribed_on: Optional[DocumentModel] = Field(
        default=None,
        alias="is_inscribed_on H-ID",
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
        alias="physical_description H-ID",
        json_schema_extra={
            "model": PhysDescModel,
            "table": "PhysDesc",
        },
    )
    verses_per_line: Optional[TermModel] = Field(
        default=None,
        alias="verses_per_line TRM-ID",
    )
    number_of_lines: Optional[int] = Field(default=None)
    lines_are_incomplete: Optional[TermModel] = Field(
        default=None,
        alias="lines_are_incomplete TRM-ID",
    )
    page_ranges: Optional[List[PageRange]] = Field(default=None)

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"part_{self.id}"

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
