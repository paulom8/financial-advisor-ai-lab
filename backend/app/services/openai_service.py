"""Small, bounded OpenAI Responses API integration for the learning lab."""

from openai import (
    APIConnectionError,
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    NotFoundError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
)

from app.core.config import OPENAI_MODEL


INSTRUCTIONS = (
    "Answer concisely for an educational lab. Use fictional examples and provide "
    "general educational information. Avoid personalized financial advice."
)


class OpenAIServiceError(Exception):
    """A safe, user-facing error from the model integration."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


async def answer_question(question: str, client: AsyncOpenAI | None) -> str:
    """Send one question to OpenAI and return its text response."""
    if client is None:
        raise OpenAIServiceError(
            "OpenAI is not configured. Set OPENAI_API_KEY in backend/.env and restart the backend.",
            status_code=503,
        )

    try:
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=question,
            max_output_tokens=500,
            store=False,
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
    answer = response.output_text.strip()
    if answer:
        return answer
    for item in response.output:
        if item.type == "message":
            for part in item.content:
                if part.type == "refusal" and part.refusal.strip():
                    return part.refusal.strip()
    raise OpenAIServiceError("OpenAI returned an empty answer. Please try another question.")
