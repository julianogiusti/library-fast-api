from typing import Optional
from sqlmodel import Session, select
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
