"""Run the model evaluation on demand."""

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from starlette.concurrency import run_in_threadpool

from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.services.model_evaluation import EvaluationDataError, run_evaluation
from app.services.test_record_tool import list_test_records_for_tool

router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])


@router.post("", response_model=EvaluationResponse)
async def evaluate_model(payload: EvaluationRequest, request: Request) -> EvaluationResponse:
    """Grade the model against the same snapshot provided to its database calls."""
    if request.headers.get("content-type", "").partition(";")[0].strip().lower() != "application/json":
        raise HTTPException(status_code=415, detail="Start an evaluation with a JSON request.")
    client = request.state.openai_client
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="OpenAI is not configured. Set OPENAI_API_KEY in backend/.env and restart the backend.",
        )

    try:
        snapshot = await run_in_threadpool(list_test_records_for_tool)
        return await run_evaluation(client, snapshot)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503, detail="Could not read the fictional records for evaluation."
        ) from exc
    except EvaluationDataError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
