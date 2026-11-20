"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from app.api.routes.questions import router as questions_router
from app.api.routes.test_records import router as test_records_router
from app.core.config import OPENAI_API_KEY
from app.db.session import SessionLocal, engine
from app.services.test_record_service import initialize_sample_table


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize the demo database and share the HTTP client across requests."""
    client = None
    try:
        with SessionLocal.begin() as db:
            initialize_sample_table(db)
        if OPENAI_API_KEY:
            client = AsyncOpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=0)
        yield {"openai_client": client}
    finally:
        if client is not None:
            await client.close()
        engine.dispose()


app = FastAPI(title="Financial Advisor AI Lab", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(test_records_router)
app.include_router(questions_router)
