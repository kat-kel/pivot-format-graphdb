from pydantic import BaseModel, Field, computed_field

from typing import Optional


class TermModel(BaseModel):
    id: int = Field(
        alias="trm_ID",
    )
    label: str = Field(
        alias="trm_Label",
    )
    description: Optional[str] = Field(
        alias="trm_Description",
        default=None,
    )
    code: Optional[str] = Field(
        alias="trm_Code",
        default=None,
    )
    semantic_reference: Optional[str] = Field(
        alias="trm_SemanticReferenceURL",
        default=None,
    )

    @computed_field
    @property
    def xml_id(self) -> str:
        return f"term_{self.id}"
