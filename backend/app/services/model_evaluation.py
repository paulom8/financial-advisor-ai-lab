"""Run three independent questions and compare their answers with preset rules."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal

from openai import AsyncOpenAI

from app.core.config import OPENAI_MODEL
from app.schemas.evaluation import EvaluationCaseResult, EvaluationResponse
from app.services.openai_service import OpenAIServiceError, answer_question
from app.services.test_record_service import SYNTHETIC_RECORD_PREFIXES
from app.services.test_record_tool import TestRecordToolResult

AUD_AMOUNT = r"(?:AUD\s*)?\$?\s*([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{1,2})?)"
WINNER_LINE = re.compile(
    rf"(?:[-•]\s+)?(Demo\s+Client\s+[A-E])\s*[:\-–—]\s*{AUD_AMOUNT}\.?", re.IGNORECASE
)
BALANCE_LINE = re.compile(rf"{AUD_AMOUNT}\.?", re.IGNORECASE)


class EvaluationDataError(Exception):
    """The saved examples cannot provide a reliable expected answer."""


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    title: str
    question: str
    expected_answer: str
    expects_database_function: bool
    matches_answer: Callable[[str], bool]


def _amount(text: str) -> Decimal:
    return Decimal(text.replace(",", ""))


def _plain_text(answer: str) -> str:
    return answer.replace("*", "").replace("`", "").strip()


def _matches_balance(answer: str) -> bool:
    match = BALANCE_LINE.fullmatch(_plain_text(answer))
    return match is not None and _amount(match[1]) == Decimal(121)


def _demo_targets(snapshot: TestRecordToolResult) -> dict[str, Decimal]:
    targets = {}
    expected_clients = {prefix.split(" — ")[1] for prefix in SYNTHETIC_RECORD_PREFIXES}
    for description in snapshot["records"]:
        client = description.split(" — ")[1]
        amount = description.rpartition("$")[2]
        targets[client] = _amount(amount)

    if (
        snapshot["truncated"]
        or targets.keys() != expected_clients
        or len(snapshot["records"]) != len(expected_clients)
    ):
        raise EvaluationDataError(
            "Evaluation needs one valid row for each of the five fictional demo clients. "
            "Check the Test table for missing or duplicate examples."
        )
    return targets


def _evaluation_cases(snapshot: TestRecordToolResult) -> tuple[EvaluationCase, ...]:
    targets = _demo_targets(snapshot)
    largest = max(targets.values())
    winners = sorted(client for client, amount in targets.items() if amount == largest)
    amount = f"{largest:,.0f}" if largest == largest.to_integral_value() else f"{largest:,.2f}"
    expected_pairs = {(client.casefold(), largest) for client in winners}

    def matches_winner(answer: str) -> bool:
        pairs = []
        for line in _plain_text(answer).splitlines():
            if not line.strip():
                continue
            match = WINNER_LINE.fullmatch(line.strip())
            if match is None:
                return False
            client = " ".join(match[1].casefold().split())
            pairs.append((client, _amount(match[2])))
        return len(pairs) == len(expected_pairs) and set(pairs) == expected_pairs

    return (
        EvaluationCase(
            "largest-target",
            "Largest savings target",
            'Which demo client has the largest savings target? Use the format "Demo Client X: AUD $amount". '
            "Give only that line. If there is a tie, give one line per tied client.",
            f"{', '.join(winners)} · AUD ${amount}",
            True,
            matches_winner,
        ),
        EvaluationCase(
            "absent-client",
            "Client absent from the records",
            'What is Demo Client Z saving for? If the records contain no entry for this client, reply "Not found".',
            "Not found",
            True,
            lambda answer: _plain_text(answer).strip(".\"'“”‘’").strip().casefold() == "not found",
        ),
        EvaluationCase(
            "general-question",
            "General compound interest question",
            "How much is a fictional AUD $100 deposit worth after two years at 10% interest "
            "compounded annually with no fees or additional deposits? Reply with the final AUD balance only.",
            "AUD $121",
            False,
            _matches_balance,
        ),
    )


async def run_evaluation(client: AsyncOpenAI, snapshot: TestRecordToolResult) -> EvaluationResponse:
    """Score each answer and whether the model chose to use the database tool."""
    cases = _evaluation_cases(snapshot)

    def get_snapshot() -> TestRecordToolResult:
        return snapshot

    results = []
    for case in cases:
        fields = dict(
            id=case.id,
            title=case.title,
            question=case.question,
            expected_answer=case.expected_answer,
            expected_database_function_used=case.expects_database_function,
        )
        try:
            answer, used = await answer_question(case.question, client, get_snapshot)
        except OpenAIServiceError as exc:
            results.append(EvaluationCaseResult(**fields, status="error", error=str(exc)))
            continue

        matched = case.matches_answer(answer)
        passed = matched and used == case.expects_database_function
        results.append(EvaluationCaseResult(
            **fields,
            status="passed" if passed else "failed",
            answer=answer,
            database_function_used=used,
            answer_matched=matched,
        ))
    return EvaluationResponse(model=OPENAI_MODEL, cases=results)
