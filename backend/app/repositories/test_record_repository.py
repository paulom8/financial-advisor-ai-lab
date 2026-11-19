"""Database queries for Test records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TestRecord


class TestRecordRepository:
    """Encapsulate persistence operations for TestRecord."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[TestRecord]:
        """Return all rows ordered by their generated identifier."""
        return list(self.db.scalars(select(TestRecord).order_by(TestRecord.id)))

    def create(self, description: str) -> TestRecord:
        """Insert and return a record, using the database timestamp default."""
        record = TestRecord(description=description)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
