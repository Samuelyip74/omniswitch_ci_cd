from datetime import UTC, datetime
from uuid import uuid4


def utcnow() -> datetime:
    return datetime.now(UTC)


def make_run_id() -> str:
    return f"run-{utcnow().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
