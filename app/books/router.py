from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlmodel import Session

from app.core.database import get_session
from app.core.error_schema import ErrorResponse

from .model import Book, BookCreate, BookFilters, BookUpdate, Page
from .service import BookService

router = APIRouter(prefix="/books", tags=["Books"])

service = BookService()

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED, responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
    },)
def create(book: BookCreate, session: Session = Depends(get_session)):
    return service.create_book(session, book)


@router.get("/", response_model=Page[Book], responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
    })
def list_books(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: BookFilters = Depends(),
):
    return service.list_books_paginated(
        session=session,
        page=page,
        size=size,
        filters=filters,
    )


@router.get(
    "/{book_id}",
    response_model=Book,
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def get_book(book_id: int, session: Session = Depends(get_session)):
    return service.get_book(session, book_id)


@router.put(
    "/{book_id}",
    response_model=Book,
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def update_book(
    book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)
):
    return service.update_book(session, book_id, book_update)

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "No Content"},
        404: {"model": ErrorResponse, "description": "Book not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    service.delete_book(session, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
