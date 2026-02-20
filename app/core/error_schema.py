from datetime import UTC, datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    type: str
    title: str
    detail: str
    status: int
    timestamp: str


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()
