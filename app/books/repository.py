from sqlmodel import Session, func, select

from .model import Book, BookFilters


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
        filters: BookFilters,
    ):
        offset = (page - 1) * size

        conditions = []

        if filters.status:
            conditions.append(Book.status == filters.status)

        if filters.author:
            conditions.append(Book.author.ilike(f"%{filters.author}%"))

        if filters.title:
            conditions.append(Book.title.ilike(f"%{filters.title}%"))

        # Query base (sem paginação)
        statement = select(Book)

        if conditions:
            statement = statement.where(*conditions)

        # Contagem total usando subquery
        total = session.exec(select(func.count()).select_from(statement.subquery())).one()

        # Ordenação
        allowed_order_fields = {
            "title": Book.title,
            "author": Book.author,
            "created_at": Book.created_at,
            "start_date": Book.start_date,
            "end_date": Book.end_date,
        }

        column = allowed_order_fields.get(filters.order_by, Book.created_at)

        if filters.order == "desc":
            statement = statement.order_by(column.desc())
        else:
            statement = statement.order_by(column.asc())

        # Paginação
        statement = statement.offset(offset).limit(size)

        items = session.exec(statement).all()

        return items, total


    def get_by_id(self, session: Session, book_id: int) -> Book | None:
        return session.get(Book, book_id)

    def update(self, session: Session, book: Book) -> Book:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    def delete(self, session: Session, book: Book) -> None:
        session.delete(book)
        session.commit()
