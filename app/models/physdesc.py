from pydantic import Field
from typing import Optional, List

from .term import TermModel
from .base import BaseDataModel


class PhysDescModel(BaseDataModel):
    id: int = Field(validation_alias="H-ID")
    material: Optional[TermModel] = Field(
        default=None,
        validation_alias="material TRM-ID",
    )
    form: Optional[TermModel] = Field(
        default=None,
        validation_alias="form TRM-ID",
    )
    folio_size_width: Optional[str] = Field(default=None)
    folio_size_height: Optional[str] = Field(default=None)
    estimated_folio_size_height: Optional[str] = Field(default=None)
    estimated_folio_size_width: Optional[str] = Field(default=None)
    has_decorations: List[Optional[TermModel]] = Field(
        default=[],
        validation_alias="has_decorations TRM-ID",
    )
    amount_of_illustrations: Optional[TermModel] = Field(
        default=None,
        validation_alias="amount_of_illustrations TRM-ID",
    )
    writing_surface_area_height: Optional[str] = Field(default=None)
    writing_surface_area_width: Optional[str] = Field(default=None)
    number_of_columns: Optional[str] = Field(default=None)
    above_top_line: Optional[TermModel] = Field(
        default=None,
        validation_alias="above_top_line TRM-ID",
    )
    script_type: Optional[TermModel] = Field(
        default=None,
        validation_alias="script_type TRM-ID",
    )
    subscript_type: Optional[TermModel] = Field(
        default=None,
        validation_alias="subscript_type TRM-ID",
    )
