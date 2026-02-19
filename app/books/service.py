from sqlmodel import Session

from app.core.exceptions import NotFoundException

from .model import Book, BookCreate, BookFilters, BookUpdate, Page
from .repository import BookRepository


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
        filters: BookFilters,
    ) -> Page[Book]:

        items, total = self.repository.list_paginated(
            session=session,
            page=page,
            size=size,
            filters=filters,
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
            raise NotFoundException("Book not found")

        update_data = book_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(book, key, value)

        return self.repository.update(session, book)

    def delete_book(self, session: Session, book_id: int) -> None:
        book = self.repository.get_by_id(session, book_id)

        if not book:
            raise NotFoundException("Book not found")

        self.repository.delete(session, book)
