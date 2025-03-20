from pydantic import BaseModel, Field
from typing import Optional


class DateRange(BaseModel):
    earliest: Optional[float | int] = Field(default=None)
    latest: Optional[float | int] = Field(default=None)


class Timestamp(BaseModel):
    time: str = Field(validation_alias="in")


class DateObject(BaseModel):
    start: Optional[DateRange] = Field(default=None)
    end: Optional[DateRange] = Field(default=None)
    timestamp: Optional[Timestamp] = Field(default=None)
    estMinDate: float | int
    estMaxDate: float
    profile: Optional[str] = Field(default=None)
    determination: Optional[str] = Field(default=None)


class ProfileConverter:
    map = {"0": "flat", "1": "central", "2": "slowStart", "3": "slowFinish"}

    @classmethod
    def convert(cls, value: str) -> str:
        if cls.map.get(value):
            return cls.map[value]
        else:
            return ""


class DeterminationConverter:
    map = {"0": "unknown", "1": "attested", "2": "conjecture", "3": "measurement"}

    @classmethod
    def convert(cls, value: str) -> str:
        if cls.map.get(value):
            return cls.map[value]
        else:
            return ""
