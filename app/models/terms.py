from dataclasses import dataclass


@dataclass
class LanguageDataModel:
    id: int
    name: str
    code: str
    url: str | None
    description: str
