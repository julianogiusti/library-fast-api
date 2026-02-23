from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, SECRET_KEY

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    subject: identificador do usuário (recomendado: user_id como string)
    """
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}

    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    # PyJWT pode retornar str (v2+) — ok.
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Retorna o payload decodificado.
    Levanta ExpiredSignatureError para token expirado,
    InvalidTokenError para token inválido.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
