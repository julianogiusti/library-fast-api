from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlmodel import Session

from app.core.database import get_session
from app.core.error_schema import ErrorResponse
from app.users.dependencies import get_current_user
from app.users.model import User

from .model import BookCreate, BookFilters, BookRead, BookUpdate, Page
from .service import BookService

router = APIRouter(prefix="/books", tags=["Books"])

service = BookService()


@router.post(
    "/",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def create(
    book: BookCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.create_book(session, book, current_user)


@router.get(
    "/",
    response_model=Page[BookRead],
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def list_books(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: BookFilters = Depends(),
):
    return service.list_books_paginated(
        session=session,
        page=page,
        size=size,
        filters=filters,
        user=current_user,
    )


@router.get(
    "/{book_id}",
    response_model=BookRead,
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def get_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.get_book(session, book_id, current_user)


@router.put(
    "/{book_id}",
    response_model=BookRead,
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return service.update_book(session, book_id, book_update, current_user)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "No Content"},
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service.delete_book(session, book_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
