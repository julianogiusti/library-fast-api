import os

from sqlmodel import Session, SQLModel, create_engine

# Importar models para registrar no SQLModel.metadata antes do create_all
from app.books.model import Book  # noqa: F401
from app.users.model import User  # noqa: F401

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,  # mude para True se quiser ver SQL no console
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
