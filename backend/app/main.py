"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.test_records import router as test_records_router
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import TestRecord  # noqa: F401 - registers model metadata
from app.services.test_record_service import ensure_sample_record


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create the introductory schema and add its initial sample row."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_sample_record(db)
    yield


app = FastAPI(title="Financial Advisor AI Lab", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(test_records_router)
