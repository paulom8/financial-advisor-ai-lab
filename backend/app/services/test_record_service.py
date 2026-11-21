"""Set up the demo table and define the approved fictional savings records."""

import re

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import TestRecord


SYNTHETIC_RECORDS = (
    "FICTIONAL DEMO — Demo Client A — emergency fund target: AUD $12,000",
    "FICTIONAL DEMO — Demo Client B — travel fund target: AUD $8,500",
    "FICTIONAL DEMO — Demo Client C — first-home deposit target: AUD $42,000",
    "FICTIONAL DEMO — Demo Client D — laptop fund target: AUD $2,400",
    "FICTIONAL DEMO — Demo Client E — education fund target: AUD $15,000",
)

# The label, client and goal identify the approved example. Its amount can change.
SYNTHETIC_RECORD_PREFIXES = tuple(record.partition("$")[0] + "$" for record in SYNTHETIC_RECORDS)
SYNTHETIC_PREFIX_PATTERN = re.compile(
    "^(?:" + "|".join(re.escape(prefix) for prefix in SYNTHETIC_RECORD_PREFIXES) + ")"
)
SYNTHETIC_SAVINGS_PATTERN = re.compile(
    SYNTHETIC_PREFIX_PATTERN.pattern
    + r"(?:[0-9]{1,9}|[0-9]{1,3}(?:,[0-9]{3}){1,2})(?:\.[0-9]{2})?$"
)


def initialize_test_table(db: Session) -> None:
    """Create the existing table if needed; sample data is inserted explicitly."""
    # Startup and the seed command share this lock until their transactions end.
    db.execute(text("SELECT pg_advisory_xact_lock(hashtext('financial_advisor_lab.seed_test'))"))
    TestRecord.__table__.create(bind=db.connection(), checkfirst=True)
