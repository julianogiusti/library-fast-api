from __future__ import annotations

from sqlmodel import Session

from app.core.security import get_password_hash, verify_password
from app.users.model import User
from app.users.repository import (
    create_user,
    get_user_by_email,
)


class UserAlreadyExistsError(Exception):
    pass


def register_user(*, session: Session, email: str, password: str) -> User:
    existing_user = get_user_by_email(session=session, email=email)
    if existing_user:
        raise UserAlreadyExistsError("User with this email already exists")

    hashed_password = get_password_hash(password)

    user = User(
        email=email,
        hashed_password=hashed_password,
    )

    return create_user(session=session, user=user)


def authenticate_user(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user
