from datetime import date, datetime, timezone
from enum import Enum
from math import ceil
from typing import Generic, Literal, Optional, TypeVar

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class ReadingStatus(str, Enum):
    TO_READ = "TO_READ"
    READING = "READING"
    DONE = "DONE"


class BookBase(SQLModel):
    title: str
    author: str
    status: ReadingStatus = ReadingStatus.TO_READ
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    status: Optional[ReadingStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class BookFilters(BaseModel):
    status: Optional[ReadingStatus] = None
    author: Optional[str] = None
    title: Optional[str] = None
    order_by: Literal["title", "author", "created_at", "start_date", "end_date"] = "created_at"
    order: Literal["asc", "desc"] = "desc"


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, *, items: list[T], total: int, page: int, size: int):
        pages = ceil(total / size) if size else 1
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
        )
