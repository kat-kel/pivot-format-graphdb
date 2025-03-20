from pydantic import Field, computed_field
from typing import Optional, List

from app.data_models.term import TermModel
from app.data_models.base import BaseDataModel


class PhysDescModel(BaseDataModel):
    id: int = Field(
        alias="H-ID",
    )
    material: Optional[TermModel] = Field(
        default=None,
        alias="material TRM-ID",
    )
    form: Optional[TermModel] = Field(
        default=None,
        alias="form TRM-ID",
    )
    folio_size_width: Optional[str] = Field(default=None)
    folio_size_height: Optional[str] = Field(default=None)
    estimated_folio_size_height: Optional[str] = Field(default=None)
    estimated_folio_size_width: Optional[str] = Field(default=None)
    has_decorations: List[Optional[TermModel]] = Field(
        default=[],
        alias="has_decorations TRM-ID",
    )
    amount_of_illustrations: Optional[TermModel] = Field(
        default=None,
        alias="amount_of_illustrations TRM-ID",
    )
    writing_surface_area_height: Optional[str] = Field(default=None)
    writing_surface_area_width: Optional[str] = Field(default=None)
    number_of_columns: Optional[str] = Field(default=None)
    above_top_line: Optional[TermModel] = Field(
        default=None,
        alias="above_top_line TRM-ID",
    )
    script_type: Optional[TermModel] = Field(
        default=None,
        alias="script_type TRM-ID",
    )
    subscript_type: Optional[TermModel] = Field(
        default=None,
        alias="subscript_type TRM-ID",
    )

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"physDesc_{self.id}"
