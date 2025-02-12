from pydantic import BaseModel, Field

from typing import Optional


class TermModel(BaseModel):
    id: int = Field(validation_alias="trm_ID")
    label: str = Field(validation_alias="trm_Label")
    description: Optional[str] = Field(
        validation_alias="trm_Description",
        default=None,
    )
    code: Optional[str] = Field(
        validation_alias="trm_Code",
        default=None,
    )
    semantic_reference: Optional[str] = Field(
        validation_alias="trm_SemanticReferenceURL",
        default=None,
    )
