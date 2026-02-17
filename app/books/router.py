from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.database import get_session

from .model import Book, BookCreate, BookUpdate, Page
from .service import BookService

router = APIRouter(prefix="/books", tags=["Books"])

service = BookService()


@router.post("/", response_model=Book)
def create(book: BookCreate, session: Session = Depends(get_session)):
    return service.create_book(session, book)


@router.get("/", response_model=Page[Book])
def list_books(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return service.list_books_paginated(session, page, size)



@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    return service.get_book(session, book_id)


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    return service.update_book(session, book_id, book_update)


@router.delete("/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    service.delete_book(session, book_id)
    return {"detail": "Book deleted successfully"}
