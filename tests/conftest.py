import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core.database import get_session
from app.main import app

# Banco em memória
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Cria as tabelas antes de cada teste
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


# Override da dependência
@pytest.fixture(name="client")
def client_fixture(session: Session):

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient):
    # cria usuário
    client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "123456",
        },
    )

    # faz login
    response = client.post(
        "/users/token",
        data={
            "username": "test@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
