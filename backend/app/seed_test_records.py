"""Explicitly insert the five fictional function-calling examples, idempotently."""

from app.db.session import SessionLocal, engine
from app.repositories.test_record_repository import TestRecordRepository
from app.services.test_record_service import (
    SYNTHETIC_PREFIX_PATTERN,
    SYNTHETIC_RECORD_PREFIXES,
    SYNTHETIC_RECORDS,
    initialize_test_table,
)


def seed_synthetic_records() -> tuple[int, int]:
    """Insert missing labelled examples, retaining all existing table rows."""
    with SessionLocal.begin() as db:
        initialize_test_table(db)
        repository = TestRecordRepository(db)
        existing_prefixes = {
            match.group()
            for description in repository.list_descriptions_matching(SYNTHETIC_PREFIX_PATTERN.pattern)
            if (match := SYNTHETIC_PREFIX_PATTERN.match(description)) is not None
        }
        missing = [
            description
            for prefix, description in zip(SYNTHETIC_RECORD_PREFIXES, SYNTHETIC_RECORDS)
            if prefix not in existing_prefixes
        ]
        for description in missing:
            repository.add(description)
    return len(missing), len(SYNTHETIC_RECORDS)


def main() -> None:
    added, expected = seed_synthetic_records()
    print(f"Added {added} of {expected} fictional demo records; existing rows were preserved.")
    engine.dispose()


if __name__ == "__main__":
    main()
