from pydantic import BaseModel, Field


class DateEndpoint(BaseModel):
    earliest: str | None = Field(default=None)
    latest: str | None = Field(default=None)


class TemporalObject(BaseModel):
    comment: str | None = Field(default=None)
    start: DateEndpoint
    end: DateEndpoint
    estMinDate: float | None = Field(default=None)
    estMaxDate: float | None = Field(default=None)
