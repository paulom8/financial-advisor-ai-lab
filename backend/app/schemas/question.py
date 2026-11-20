"""Request and response schemas for a single model question."""

from pydantic import BaseModel, ConfigDict, Field


class QuestionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=1, max_length=4_000)


class QuestionResponse(BaseModel):
    answer: str
