"""Initialize the demo table with one synthetic row when it is empty."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import TestRecord
from app.repositories.test_record_repository import TestRecordRepository


def initialize_sample_table(db: Session) -> None:
    """Initialize and seed the table within the caller's transaction."""
    # Workers starting together must agree on which one creates and seeds the table.
    db.execute(text("SELECT pg_advisory_xact_lock(hashtext('financial_advisor_lab.seed_test'))"))
    TestRecord.__table__.create(bind=db.connection(), checkfirst=True)
    repository = TestRecordRepository(db)
    if not repository.has_records():
        repository.add("Sample record for the database learning exercise")
