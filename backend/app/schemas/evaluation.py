"""Request and results for the three preset evaluation cases."""

from typing import Literal

from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    run: Literal[True]


class EvaluationCaseResult(BaseModel):
    id: str
    title: str
    question: str
    expected_answer: str
    expected_database_function_used: bool
    status: Literal["passed", "failed", "error"]
    answer: str | None = None
    database_function_used: bool | None = None
    answer_matched: bool | None = None
    error: str | None = None


class EvaluationResponse(BaseModel):
    model: str
    cases: list[EvaluationCaseResult]
