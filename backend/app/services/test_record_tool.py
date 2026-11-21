"""Read-only, bounded database access for the model's function call."""

from app.db.session import SessionLocal
from app.repositories.test_record_repository import TestRecordRepository
from app.services.test_record_service import SYNTHETIC_SAVINGS_PATTERN


MAX_TOOL_RECORDS = 50


def list_test_records_for_tool() -> dict[str, object]:
    """Return approved demo clients and goals with their saved numeric targets."""
    with SessionLocal() as db:
        candidates = TestRecordRepository(db).list_descriptions_matching(
            SYNTHETIC_SAVINGS_PATTERN.pattern, limit=MAX_TOOL_RECORDS + 1
        )

    # Check the full text again at the boundary before sending it to the provider.
    descriptions = [text for text in candidates if SYNTHETIC_SAVINGS_PATTERN.fullmatch(text)]
    return {
        "limit": MAX_TOOL_RECORDS,
        "truncated": len(descriptions) > MAX_TOOL_RECORDS,
        "records": descriptions[:MAX_TOOL_RECORDS],
    }
