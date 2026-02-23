from http import HTTPStatus

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlmodel import Session

from app.core.database import get_session
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.users.model import User
from app.users.repository import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

session_dependency = Depends(get_session)
token_dependency = Depends(oauth2_scheme)


def get_current_user(
    token: str = token_dependency,
    session: Session = session_dependency,
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise AppException(
                message="Invalid authentication credentials",
                status_code=HTTPStatus.UNAUTHORIZED,
                title="Unauthorized",
            )

    except ExpiredSignatureError as err:
        raise AppException(
            message="Token expired",
            status_code=HTTPStatus.UNAUTHORIZED,
            title="Unauthorized",
        ) from err

    except InvalidTokenError as err:
        raise AppException(
            message="Invalid authentication credentials",
            status_code=HTTPStatus.UNAUTHORIZED,
            title="Unauthorized",
        ) from err

    user = get_user_by_id(session=session, user_id=int(user_id))

    if not user or not user.is_active:
        raise AppException(
            message="Invalid authentication credentials",
            status_code=HTTPStatus.UNAUTHORIZED,
            title="Unauthorized",
        )

    return user
