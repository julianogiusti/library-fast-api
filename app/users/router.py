from http import HTTPStatus

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.error_schema import ErrorResponse
from app.core.exceptions import AppException
from app.core.security import create_access_token

from .model import UserCreate, UserRead
from .service import UserAlreadyExistsError, authenticate_user, register_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    try:
        return register_user(
            session=session,
            email=str(payload.email),
            password=payload.password,
        )
    except UserAlreadyExistsError as err:
        raise AppException(
            message="Email already registered",
            status_code=HTTPStatus.CONFLICT,
            title="Conflict",
        ) from err


@router.post(
    "/token",
    responses={
        401: {"model": ErrorResponse, "description": "Incorrect email or password"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    OAuth2PasswordRequestForm envia:
    - username
    - password

    Aqui username = email.
    """
    user = authenticate_user(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise AppException(
            message="Incorrect email or password",
            status_code=HTTPStatus.UNAUTHORIZED,
            title="Unauthorized",
        )

    token = create_access_token(subject=str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer",
    }
