from typing import Optional

from sqlmodel import Session, func, select

from .model import Book, ReadingStatus


class BookRepository:
    def create(self, session: Session, book: Book) -> Book:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    def list(self, session: Session) -> list[Book]:
        statement = select(Book)
        return session.exec(statement).all()

    def list_paginated(
        self,
        session: Session,
        *,
        page: int,
        size: int,
        status: Optional[ReadingStatus] = None,
        author: Optional[str] = None,
        title: Optional[str] = None,
        order_by: str = "created_at",
        order: str = "desc",
    ):
        offset = (page - 1) * size

        statement = select(Book)
        count_statement = select(func.count()).select_from(Book)

        # Filtros
        if status:
            statement = statement.where(Book.status == status)
            count_statement = count_statement.where(Book.status == status)

        if author:
            statement = statement.where(Book.author.ilike(f"%{author}%"))
            count_statement = count_statement.where(Book.author.ilike(f"%{author}%"))

        if title:
            statement = statement.where(Book.title.ilike(f"%{title}%"))
            count_statement = count_statement.where(Book.title.ilike(f"%{title}%"))

        # Ordenação
        allowed_order_fields = {
            "title": Book.title,
            "author": Book.author,
            "created_at": Book.created_at,
            "start_date": Book.start_date,
            "end_date": Book.end_date,
        }

        column = allowed_order_fields.get(order_by, Book.created_at)

        if order not in {"asc", "desc"}:
            order = "desc"

        if order == "desc":
            statement = statement.order_by(column.desc())
        else:
            statement = statement.order_by(column.asc())

        # Paginação
        statement = statement.offset(offset).limit(size)

        items = session.exec(statement).all()
        total = session.exec(count_statement).one()

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
