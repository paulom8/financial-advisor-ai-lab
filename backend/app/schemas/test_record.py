"""API representation of a Test record."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TestRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str = Field(max_length=255)
    date_inserted: datetime
