"""Independent retrieval-only and grounded-answer requests."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from sqlalchemy.exc import DBAPIError

from app.schemas.question import QuestionRequest
from app.services.document_embeddings import (
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    SemanticPassage,
    embed_texts,
    semantic_rank,
)
from app.services.document_rag import Passage, generate, load_sections, retrieve
from app.services.document_vector_search import rank_saved_passages
from app.services.openai_service import OpenAIServiceError

router = APIRouter(prefix="/api/documents", tags=["documents"])


class RetrievalResponse(BaseModel):
    passages: list[Passage]


class ComparisonResponse(BaseModel):
    keyword_passages: list[Passage]
    semantic_passages: list[SemanticPassage]
    embedding_model: str


class VectorSearchResponse(BaseModel):
    passages: list[SemanticPassage]
    embedding_model: str


@router.post("/vector-search", response_model=VectorSearchResponse)
async def search_saved_vectors(payload: QuestionRequest, request: Request):
    seed_message = "Run python -m app.seed_document_vectors from the backend folder to seed the passages."
    try:
        (vector,) = await embed_texts([payload.question], request.state.openai_client)
        if len(vector) != EMBEDDING_DIMENSIONS:
            raise OpenAIServiceError("The embedding model returned an unexpected vector dimension.")
        passages = await run_in_threadpool(rank_saved_passages, vector)
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    except DBAPIError as exc:
        detail = seed_message if getattr(exc.orig, "sqlstate", None) == "42P01" else (
            "PostgreSQL vector search failed. Check the database connection and pgvector setup."
        )
        raise HTTPException(status_code=503, detail=detail) from exc
    if not passages:
        raise HTTPException(status_code=503, detail=seed_message)
    return VectorSearchResponse(passages=passages, embedding_model=EMBEDDING_MODEL)


@router.post("/compare", response_model=ComparisonResponse)
async def compare_retrieval(payload: QuestionRequest, request: Request):
    sections = load_sections()
    try:
        semantic = await semantic_rank(payload.question, sections, request.state.openai_client)
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    return ComparisonResponse(
        keyword_passages=retrieve(payload.question, sections),
        semantic_passages=semantic,
        embedding_model=EMBEDDING_MODEL,
    )


@router.post("/retrieve", response_model=RetrievalResponse)
def retrieve_documents(payload: QuestionRequest):
    return RetrievalResponse(passages=retrieve(payload.question))


@router.post("/ask")
async def ask_documents(payload: QuestionRequest, request: Request):
    passages = retrieve(payload.question)
    try:
        answer, model_called = await generate(payload.question, passages, request.state.openai_client)
    except OpenAIServiceError as exc:
        # Keep retrieval visible even if generation fails.
        return {"passages": passages, "status": "error", "error": str(exc),
                "answer": "", "citations": [], "model_called": None}
    return {**answer.model_dump(), "passages": passages, "model_called": model_called}
