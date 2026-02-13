from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


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
