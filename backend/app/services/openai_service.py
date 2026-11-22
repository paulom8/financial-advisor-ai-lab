"""Small, bounded OpenAI Responses API integration for the learning lab."""

import json
from collections.abc import Callable
from typing import Literal

from openai import (
    APIConnectionError,
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    NotFoundError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
    omit,
)
from openai.types.responses import FunctionToolParam, Response, ResponseInputParam
from sqlalchemy.exc import SQLAlchemyError
from starlette.concurrency import run_in_threadpool

from app.core.config import OPENAI_MODEL
from app.services.test_record_tool import TestRecordToolResult


TOOL_NAME = "list_test_records"
INSTRUCTIONS = (
    "Answer concisely for an educational lab. Use fictional examples and provide "
    "general educational information. Avoid personalized financial advice. "
    f"Use {TOOL_NAME} when the question asks about saved demo records. Base any "
    "record-specific answer only on the returned demo records, and describe "
    "comparisons within those records. If a requested client is absent, say they "
    "are absent from the returned records."
)

TOOLS: list[FunctionToolParam] = [
    {
        "type": "function",
        "name": TOOL_NAME,
        "description": "Read approved fictional savings goals and targets saved in PostgreSQL.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


class OpenAIServiceError(Exception):
    """A safe, user-facing error from the model integration."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


async def answer_question(
    question: str,
    client: AsyncOpenAI | None,
    list_records: Callable[[], TestRecordToolResult],
) -> tuple[str, bool]:
    """Answer one question, optionally completing one validated read-only call."""
    if client is None:
        raise OpenAIServiceError(
            "OpenAI is not configured. Set OPENAI_API_KEY in backend/.env and restart the backend.",
            status_code=503,
        )

    response = await _request_response(client, question, tool_choice="auto")
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        return _answer_text(response), False
    if len(calls) != 1:
        raise OpenAIServiceError("OpenAI requested too many database function calls.")

    call = calls[0]
    if getattr(call, "name", None) != TOOL_NAME or call.namespace:
        raise OpenAIServiceError("OpenAI requested an unsupported function.")
    call_id = getattr(call, "call_id", None)
    if call.status not in (None, "completed") or not isinstance(call_id, str) or not call_id.strip():
        raise OpenAIServiceError("OpenAI returned an incomplete database function call.")
    raw_arguments = getattr(call, "arguments", None)
    if not isinstance(raw_arguments, str) or len(raw_arguments) > 256:
        raise OpenAIServiceError("OpenAI returned invalid function arguments.")
    try:
        arguments = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        raise OpenAIServiceError("OpenAI returned invalid function arguments.") from exc
    if not isinstance(arguments, dict) or arguments:
        raise OpenAIServiceError("OpenAI returned invalid function arguments.")

    try:
        result = await run_in_threadpool(list_records)
    except SQLAlchemyError as exc:
        raise OpenAIServiceError(
            "The database function could not read the fictional records. "
            "Check the database connection and try again.",
            status_code=503,
        ) from exc

    # Replay the provider's items in order, including encrypted reasoning if returned.
    response = await _request_response(
        client,
        [
            {"role": "user", "content": question},
            *(item.model_dump(mode="json", exclude_none=True) for item in response.output),
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": json.dumps(result, ensure_ascii=False, separators=(",", ":")),
            },
        ],
        tool_choice="none",
    )
    if any(item.type == "function_call" for item in response.output):
        raise OpenAIServiceError("OpenAI requested more than one database function call.")
    answer = _answer_text(response)
    if result["truncated"]:
        answer += (
            f"\n\nThe database function returned only the first {result['limit']} "
            "matching fictional rows. More matching rows exist."
        )
    return answer, True


async def _request_response(
    client: AsyncOpenAI,
    input_items: str | ResponseInputParam,
    *,
    tool_choice: Literal["auto", "none"],
) -> Response:
    try:
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=input_items,
            max_output_tokens=500,
            store=False,
            tools=TOOLS,
            tool_choice=tool_choice,
            parallel_tool_calls=False,
            include=["reasoning.encrypted_content"] if tool_choice == "auto" else omit,
        )
    except AuthenticationError as exc:
        raise OpenAIServiceError(
            "OpenAI rejected the backend API key. Update OPENAI_API_KEY and restart the backend.",
            status_code=503,
        ) from exc
    except (PermissionDeniedError, NotFoundError) as exc:
        raise OpenAIServiceError(
            "Check that the backend's OpenAI project can access the configured OPENAI_MODEL.",
            status_code=503,
        ) from exc
    except RateLimitError as exc:
        if exc.code == "insufficient_quota":
            raise OpenAIServiceError(
                "The OpenAI project has insufficient quota. Check its billing and usage limits.",
                status_code=503,
            ) from exc
        raise OpenAIServiceError(
            "OpenAI's rate limit was reached. Wait a moment before trying again.", status_code=429
        ) from exc
    except APITimeoutError as exc:
        raise OpenAIServiceError("OpenAI timed out. Please try again.", status_code=504) from exc
    except APIConnectionError as exc:
        raise OpenAIServiceError(
            "Could not connect to OpenAI. Check the backend's internet connection and try again."
        ) from exc
    except OpenAIError as exc:
        raise OpenAIServiceError("OpenAI could not complete the request. Please try again.") from exc

    if response.status != "completed":
        if response.incomplete_details and response.incomplete_details.reason == "max_output_tokens":
            raise OpenAIServiceError("The answer reached the output limit. Try a narrower question.")
        raise OpenAIServiceError("OpenAI did not complete the answer. Try rephrasing the question.")
    return response


def _answer_text(response: Response) -> str:
    answer = response.output_text.strip()
    if answer:
        return answer
    for item in response.output:
        if item.type == "message":
            for part in item.content:
                if part.type == "refusal" and part.refusal.strip():
                    return part.refusal.strip()
    raise OpenAIServiceError("OpenAI returned an empty answer. Please try another question.")
