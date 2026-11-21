"""Read-only, bounded database access for the model's function call."""

from app.db.session import SessionLocal
from app.repositories.test_record_repository import TestRecordRepository
from app.services.test_record_service import SYNTHETIC_RECORDS


MAX_TOOL_RECORDS = 50


def list_test_records_for_tool() -> dict[str, object]:
    """Return saved descriptions that exactly match the approved demo records."""
    with SessionLocal() as db:
        descriptions = TestRecordRepository(db).list_matching_descriptions(
            SYNTHETIC_RECORDS, limit=MAX_TOOL_RECORDS + 1
        )

    return {
        "limit": MAX_TOOL_RECORDS,
        "truncated": len(descriptions) > MAX_TOOL_RECORDS,
        "records": descriptions[:MAX_TOOL_RECORDS],
    }
