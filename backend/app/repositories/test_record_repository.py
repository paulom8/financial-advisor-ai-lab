"""Database queries for Test records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TestRecord


class TestRecordRepository:
    """Encapsulate persistence operations for TestRecord."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[TestRecord]:
        """Return all rows ordered by identifier."""
        return list(self.db.scalars(select(TestRecord).order_by(TestRecord.id)))

    def list_descriptions_matching(
        self, pattern: str, *, limit: int | None = None
    ) -> list[str]:
        """Select descriptions that match an application-defined pattern in row order."""
        statement = (
            select(TestRecord.description)
            .where(TestRecord.description.regexp_match(pattern))
            .order_by(TestRecord.id)
        )
        if limit is not None:
            statement = statement.limit(limit)
        return list(self.db.scalars(statement))

    def add(self, description: str) -> None:
        self.db.add(TestRecord(description=description))
