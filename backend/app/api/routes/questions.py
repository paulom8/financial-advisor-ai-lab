"""Endpoint for one question and one model answer."""

from fastapi import APIRouter, HTTPException, Request

from app.schemas.question import QuestionRequest, QuestionResponse
from app.services.openai_service import OpenAIServiceError, answer_question

router = APIRouter(prefix="/api/ask", tags=["questions"])


@router.post("", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest, request: Request) -> QuestionResponse:
    """Return one OpenAI answer without storing a conversation."""
    try:
        answer = await answer_question(payload.question, request.state.openai_client)
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    return QuestionResponse(answer=answer)
