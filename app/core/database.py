from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,  # mude para True se quiser ver SQL no console
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
