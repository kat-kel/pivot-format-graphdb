from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated


def profile_validator(value) -> str:
    if value == "0":
        return "flat"
    elif value == "1":
        return "central"
    elif value == "2":
        return "slowStart"
    elif value == "3":
        return "slowFinish"
    else:
        return "INVALID"


def determination_validator(value) -> str:
    if value == "0":
        return "unknown"
    elif value == "1":
        return "attested"
    elif value == "2":
        return "conjecture"
    elif value == "3":
        return "measurement"
    else:
        return "INVALID"


def timestamp_type_validator(value) -> str:
    if value == "s":
        return "exact"
    else:
        return value


class DateRange(BaseModel):
    earliest: Optional[float] = Field(default=None)
    latest: Optional[float] = Field(default=None)


class Timestamp(BaseModel):
    time: str = Field(validation_alias="in")
    type: Annotated[Optional[str], BeforeValidator(timestamp_type_validator)] = Field(
        default=None
    )


class DateObject(BaseModel):
    start: Optional[DateRange] = Field(default=None)
    end: Optional[DateRange] = Field(default=None)
    timestamp: Optional[Timestamp] = Field(default=None)
    estMinDate: float
    estMaxDate: float
    profile: Annotated[Optional[str], BeforeValidator(profile_validator)] = Field(
        default=None
    )
    determination: Annotated[
        Optional[str], BeforeValidator(determination_validator)
    ] = Field(default=None)
