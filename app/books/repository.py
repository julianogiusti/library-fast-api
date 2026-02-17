from typing import Optional

from sqlmodel import Session, func, select

from .model import Book


class BookRepository:

    def create(self, session: Session, book: Book) -> Book:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    def list(self, session: Session) -> list[Book]:
        statement = select(Book)
        return session.exec(statement).all()

    def list_paginated(self, session: Session, *, page: int, size: int):
        offset = (page - 1) * size

        statement = select(Book).offset(offset).limit(size)
        items = session.exec(statement).all()

        total_statement = select(func.count()).select_from(Book)
        total = session.exec(total_statement).one()

        return items, total

    def get_by_id(self, session: Session, book_id: int) -> Optional[Book]:
        return session.get(Book, book_id)

    def update(self, session: Session, book: Book) -> Book:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    def delete(self, session: Session, book: Book) -> None:
        session.delete(book)
        session.commit()
