"""Endpoint for one question and one model answer."""

from fastapi import APIRouter, HTTPException, Request

from app.schemas.question import QuestionRequest, QuestionResponse
from app.services.openai_service import OpenAIServiceError, answer_question
from app.services.test_record_tool import list_test_records_for_tool

router = APIRouter(prefix="/api/ask", tags=["questions"])


@router.post("", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest, request: Request) -> QuestionResponse:
    """Return one OpenAI answer without storing a conversation."""
    try:
        answer, database_function_used = await answer_question(
            payload.question,
            request.state.openai_client,
            list_test_records_for_tool,
        )
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    return QuestionResponse(answer=answer, database_function_used=database_function_used)
