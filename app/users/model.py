from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime, Index, func
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(nullable=False, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )


Index("ix_users_email_unique", User.email, unique=True)


class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
