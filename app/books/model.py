from datetime import date, datetime
from enum import Enum
from math import ceil
from typing import Generic, Optional, TypeVar

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
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    status: Optional[ReadingStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


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
