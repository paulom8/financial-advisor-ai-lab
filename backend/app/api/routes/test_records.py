"""Endpoints for listing the sample records."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.test_record_repository import TestRecordRepository
from app.schemas.test_record import TestRecordResponse

router = APIRouter(prefix="/api/test-records", tags=["test-records"])


@router.get("", response_model=list[TestRecordResponse])
def list_test_records(db: Session = Depends(get_db)) -> list[TestRecordResponse]:
    """Return every row from the Test table."""
    return TestRecordRepository(db).list_all()
