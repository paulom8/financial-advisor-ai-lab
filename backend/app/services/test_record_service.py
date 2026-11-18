"""Initialize the demo table with one synthetic row when it is empty."""

from sqlalchemy.orm import Session

from app.repositories.test_record_repository import TestRecordRepository


def ensure_sample_record(db: Session) -> None:
    """Seed one example only for a newly initialized, empty table."""
    repository = TestRecordRepository(db)
    if not repository.list_all():
        repository.create("Sample record for the database learning exercise")
