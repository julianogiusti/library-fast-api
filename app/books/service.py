from sqlmodel import Session

from app.core.exceptions import NotFoundException
from app.users.model import User

from .model import Book, BookCreate, BookFilters, BookUpdate, Page
from .repository import BookRepository


class BookService:
    def __init__(self):
        self.repository = BookRepository()

    def create_book(self, session: Session, book_create: BookCreate, user: User) -> Book:
        book = Book(
            **book_create.model_dump(),
            user_id=user.id,
        )
        return self.repository.create(session, book)

    def list_books(self, session: Session, user: User) -> list[Book]:
        return self.repository.list(session, user_id=user.id)

    def list_books_paginated(
        self,
        session: Session,
        page: int,
        size: int,
        filters: BookFilters,
        user: User,
    ) -> Page[Book]:

        items, total = self.repository.list_paginated(
            session=session,
            page=page,
            size=size,
            filters=filters,
            user_id=user.id,
        )

        return Page.create(
            items=items,
            total=total,
            page=page,
            size=size,
        )

    def get_book(self, session: Session, book_id: int, user: User) -> Book:
        book = self.repository.get_by_id(session, book_id, user_id=user.id)

        if not book:
            raise NotFoundException("Book not found")

        return book

    def update_book(
        self, session: Session, book_id: int, book_update: BookUpdate, user: User
    ) -> Book:
        book = self.repository.get_by_id(session, book_id, user_id=user.id)

        if not book:
            raise NotFoundException("Book not found")

        update_data = book_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(book, key, value)

        return self.repository.update(session, book)

    def delete_book(self, session: Session, book_id: int, user: User) -> None:
        book = self.repository.get_by_id(session, book_id, user_id=user.id)

        if not book:
            raise NotFoundException("Book not found")

        self.repository.delete(session, book)
