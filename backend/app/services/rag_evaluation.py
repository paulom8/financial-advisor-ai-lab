"""Run a small, labelled evaluation of retrieval and grounded answers."""

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal

from fastapi import HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel

from app.services.document_embeddings import SemanticPassage
from app.services.document_rag import GeneratedAnswer, generate, load_sections, retrieve
from app.services.openai_service import OpenAIServiceError


@dataclass(frozen=True)
class Case:
    question: str
    expected: str
    passage_id: str | None


CASES = (
    Case("How many employees does the company have?", "18 employees", "company-profile:2"),
    Case("How many people work here?", "18 employees", "company-profile:2"),
    Case("Do you charge a cancellation fee?", "The documents don't cover this question.", None),
)


class SearchResult(BaseModel):
    method: Literal["keyword", "vector"]
    passages: list[str]
    retrieval_passed: bool | None = None
    answer: str | None = None
    citations: list[str]
    answer_passed: bool | None = None
    error: str | None = None


class CaseResult(BaseModel):
    question: str
    expected_answer: str
    expected_passage: str | None
    results: list[SearchResult]


class RagEvaluationReport(BaseModel):
    cases: list[CaseResult]


def answer_matches(case: Case, answer: GeneratedAnswer) -> bool:
    if case.passage_id is None:
        return answer.status == "not_covered" and not answer.citations
    return (
        answer.status == "answered"
        and case.passage_id in answer.citations
        and re.search(r"\b(?:18|eighteen)\b", answer.answer, flags=re.IGNORECASE) is not None
    )


async def evaluate_rag(
    client: AsyncOpenAI | None,
    retrieve_vector: Callable[[str], Awaitable[list[SemanticPassage]]],
) -> RagEvaluationReport:
    sections = load_sections()
    labels = {p.id: f"{p.document} / {p.section}" for p in sections}
    cases = []
    for case in CASES:
        results = []
        for method in ("keyword", "vector"):
            result = SearchResult(method=method, passages=[], citations=[])
            results.append(result)
            try:
                passages = (
                    retrieve(case.question, sections)
                    if method == "keyword"
                    else await retrieve_vector(case.question)
                )
            except HTTPException as exc:
                result.error = str(exc.detail)
                continue

            passage_labels = {p.id: f"{p.document} / {p.section}" for p in passages}
            result.passages = list(passage_labels.values())
            if case.passage_id is not None:
                result.retrieval_passed = case.passage_id in passage_labels
            try:
                answer, _ = await generate(case.question, passages, client)
            except OpenAIServiceError as exc:
                result.error = str(exc)
                continue
            result.answer = answer.answer
            result.citations = [passage_labels[pid] for pid in answer.citations]
            result.answer_passed = answer_matches(case, answer)

        cases.append(CaseResult(
            question=case.question,
            expected_answer=case.expected,
            expected_passage=labels.get(case.passage_id, case.passage_id),
            results=results,
        ))
    return RagEvaluationReport(cases=cases)
