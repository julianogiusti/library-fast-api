from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.core.exceptions import NotFoundException

from .model import Book, BookCreate, BookUpdate, Page
from .repository import BookRepository, ReadingStatus


class BookService:

    def __init__(self):
        self.repository = BookRepository()

    def create_book(self, session: Session, book_create: BookCreate) -> Book:
        book = Book.model_validate(book_create)
        return self.repository.create(session, book)

    def list_books(self, session: Session) -> list[Book]:
        return self.repository.list(session)

    def list_books_paginated(
        self,
        session: Session,
        page: int,
        size: int,
        status: Optional[ReadingStatus] = None,
        author: Optional[str] = None,
        title: Optional[str] = None,
        order_by: str = "created_at",
        order: str = "desc",
    ) -> Page[Book]:

        items, total = self.repository.list_paginated(
            session=session,
            page=page,
            size=size,
            status=status,
            author=author,
            title=title,
            order_by=order_by,
            order=order,
        )

        return Page.create(
            items=items,
            total=total,
            page=page,
            size=size,
        )


    def get_book(self, session: Session, book_id: int) -> Book:
        book = self.repository.get_by_id(session, book_id)

        if not book:
            raise NotFoundException("Book not found")

        return book

    def update_book(self, session: Session, book_id: int, book_update: BookUpdate) -> Book:
        book = self.repository.get_by_id(session, book_id)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(book, key, value)

        return self.repository.update(session, book)

    def delete_book(self, session: Session, book_id: int) -> None:
        book = self.repository.get_by_id(session, book_id)

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        self.repository.delete(session, book)
