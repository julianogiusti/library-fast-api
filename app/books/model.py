from datetime import UTC, date, datetime
from enum import StrEnum
from math import ceil
from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class ReadingStatus(StrEnum):
    TO_READ = "TO_READ"
    READING = "READING"
    DONE = "DONE"


class BookBase(SQLModel):
    title: str
    author: str
    status: ReadingStatus = ReadingStatus.TO_READ
    start_date: date | None = None
    end_date: date | None = None


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    status: ReadingStatus | None = None
    start_date: date | None = None
    end_date: date | None = None


class BookFilters(BaseModel):
    status: ReadingStatus | None = None
    author: str | None = None
    title: str | None = None
    order_by: Literal["title", "author", "created_at", "start_date", "end_date"] = "created_at"
    order: Literal["asc", "desc"] = "desc"


class Page[T](BaseModel):
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
