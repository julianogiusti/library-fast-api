import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient

PASSWORD = "12345678"
PROTECTED_URL = "/books/"


def _unique_email() -> str:
    return f"test_{uuid.uuid4().hex[:12]}@example.com"


def _create_user(client: TestClient, email: str, password: str = PASSWORD):
    return client.post("/users/", json={"email": email, "password": password})


def _login(client: TestClient, email: str, password: str = PASSWORD):
    return client.post(
        "/users/token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_user_should_return_201_and_user_read(client: TestClient):
    email = _unique_email()

    response = _create_user(client, email=email)

    assert response.status_code == HTTPStatus.CREATED, response.text
    data = response.json()

    assert "id" in data
    assert data["email"] == email
    assert data["is_active"] is True
    assert "created_at" in data
    assert "hashed_password" not in data


def test_create_user_should_return_422_for_invalid_email(client: TestClient):
    response = _create_user(client, email="not-an-email")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text


def test_create_user_should_return_409_when_email_already_registered(client: TestClient):
    email = _unique_email()

    r1 = _create_user(client, email=email)
    assert r1.status_code == HTTPStatus.CREATED, r1.text

    r2 = _create_user(client, email=email)
    assert r2.status_code == HTTPStatus.CONFLICT, r2.text


def test_login_should_return_access_token(client: TestClient):
    email = _unique_email()

    r_create = _create_user(client, email=email)
    assert r_create.status_code == HTTPStatus.CREATED, r_create.text

    r_login = _login(client, email=email)
    assert r_login.status_code == HTTPStatus.OK, r_login.text

    data = r_login.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10


def test_login_should_return_401_for_wrong_password(client: TestClient):
    email = _unique_email()

    r_create = _create_user(client, email=email)
    assert r_create.status_code == HTTPStatus.CREATED, r_create.text

    r_login = _login(client, email=email, password="wrongpass123")
    assert r_login.status_code == HTTPStatus.UNAUTHORIZED, r_login.text


def test_protected_endpoint_should_return_401_without_token(client: TestClient):
    response = client.get(PROTECTED_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text


def test_protected_endpoint_should_return_401_with_invalid_token(client: TestClient):
    response = client.get(PROTECTED_URL, headers=_auth_headers("invalid.token.here"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text


def test_protected_endpoint_should_allow_access_with_valid_token(client: TestClient):
    email = _unique_email()

    r_create = _create_user(client, email=email)
    assert r_create.status_code == HTTPStatus.CREATED, r_create.text

    r_login = _login(client, email=email)
    assert r_login.status_code == HTTPStatus.OK, r_login.text
    token = r_login.json()["access_token"]

    response = client.get(PROTECTED_URL, headers=_auth_headers(token))
    assert response.status_code == HTTPStatus.OK, response.text

    data = response.json()
    assert set(["items", "total", "page", "size", "pages"]).issubset(data.keys())
    assert isinstance(data["items"], list)
