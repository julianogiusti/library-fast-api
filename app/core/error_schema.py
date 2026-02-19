from datetime import datetime, timezone

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    type: str
    title: str
    detail: str
    status: int
    timestamp: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
