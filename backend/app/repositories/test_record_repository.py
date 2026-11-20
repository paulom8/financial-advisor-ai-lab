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

    def has_records(self) -> bool:
        return self.db.scalar(select(TestRecord.id).limit(1)) is not None

    def add(self, description: str) -> None:
        self.db.add(TestRecord(description=description))
