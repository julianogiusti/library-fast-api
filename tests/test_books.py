from http import HTTPStatus


def test_should_create_book_successfully(client, auth_headers):
    response = client.post(
        "/books/",
        json={"title": "Clean Code", "author": "Robert C. Martin", "status": "TO_READ"},
        headers=auth_headers,
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["title"] == "Clean Code"
    assert data["author"] == "Robert C. Martin"
    assert data["status"] == "TO_READ"


def test_should_return_empty_list_when_no_books(client, auth_headers):
    response = client.get("/books/", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0


def test_should_list_created_book(client, auth_headers):
    client.post(
        "/books/",
        json={"title": "Clean Architecture", "author": "Robert C. Martin", "status": "TO_READ"},
        headers=auth_headers,
    )

    response = client.get("/books/", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Clean Architecture"


def test_should_paginate_books(client, auth_headers):
    # cria 3 livros
    for i in range(3):
        client.post(
            "/books/",
            json={"title": f"Book {i}", "author": "Author", "status": "TO_READ"},
            headers=auth_headers,
        )

    response = client.get("/books/?size=2&page=1", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 2


def test_should_return_second_page_correctly(client, auth_headers):
    # cria 3 livros
    for i in range(3):
        client.post(
            "/books/",
            json={"title": f"Book {i}", "author": "Author", "status": "TO_READ"},
            headers=auth_headers,
        )

    # página 1
    response_page_1 = client.get("/books/?size=2&page=1", headers=auth_headers)
    data_page_1 = response_page_1.json()

    # página 2
    response_page_2 = client.get("/books/?size=2&page=2", headers=auth_headers)
    data_page_2 = response_page_2.json()

    assert data_page_1["total"] == 3
    assert len(data_page_1["items"]) == 2

    assert data_page_2["total"] == 3
    assert len(data_page_2["items"]) == 1


def test_should_filter_books_by_status(client, auth_headers):
    client.post(
        "/books/",
        json={"title": "Book 1", "author": "Author", "status": "TO_READ"},
        headers=auth_headers,
    )

    client.post(
        "/books/",
        json={"title": "Book 2", "author": "Author", "status": "READING"},
        headers=auth_headers,
    )

    response = client.get("/books/?status=TO_READ", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == "TO_READ"


def test_should_filter_books_by_title(client, auth_headers):
    client.post(
        "/books/",
        json={"title": "Clean Code", "author": "Uncle Bob", "status": "TO_READ"},
        headers=auth_headers,
    )

    client.post(
        "/books/",
        json={"title": "Domain Driven Design", "author": "Eric Evans", "status": "TO_READ"},
        headers=auth_headers,
    )

    response = client.get("/books/?title=Clean", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["total"] == 1
    assert "Clean" in data["items"][0]["title"]


def test_should_order_books_by_title_asc(client, auth_headers):
    client.post(
        "/books/",
        json={"title": "C Book", "author": "A", "status": "TO_READ"},
        headers=auth_headers,
    )
    client.post(
        "/books/",
        json={"title": "A Book", "author": "A", "status": "TO_READ"},
        headers=auth_headers,
    )

    response = client.get("/books/?order_by=title&order=asc", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    titles = [item["title"] for item in data["items"]]

    assert titles == sorted(titles)


def test_should_return_404_when_book_not_found(client, auth_headers):
    response = client.get("/books/999", headers=auth_headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_should_delete_book_successfully(client, auth_headers):
    create_response = client.post(
        "/books/",
        json={"title": "Delete Me", "author": "Author", "status": "TO_READ"},
        headers=auth_headers,
    )
    assert create_response.status_code == HTTPStatus.CREATED
    book_id = create_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}", headers=auth_headers)
    assert delete_response.status_code == HTTPStatus.NO_CONTENT
    assert delete_response.text == ""  # 204 sem body

    get_response = client.get(f"/books/{book_id}", headers=auth_headers)
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_each_user_should_only_see_own_books(client, auth_headers):
    # usuário 1 cria um livro
    create_response_user1 = client.post(
        "/books/",
        json={"title": "User 1 Book", "author": "Author", "status": "TO_READ"},
        headers=auth_headers,
    )
    assert create_response_user1.status_code == HTTPStatus.CREATED

    # cria usuário 2
    client.post(
        "/users/",
        json={
            "email": "user2@example.com",
            "password": "12345678",
        },
    )
    login_user2 = client.post(
        "/users/token",
        data={
            "username": "user2@example.com",
            "password": "12345678",
        },
    )
    token_user2 = login_user2.json()["access_token"]
    auth_headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    # usuário 2 cria outro livro
    create_response_user2 = client.post(
        "/books/",
        json={"title": "User 2 Book", "author": "Author", "status": "TO_READ"},
        headers=auth_headers_user2,
    )
    assert create_response_user2.status_code == HTTPStatus.CREATED

    # lista livros do usuário 1
    list_user1 = client.get("/books/", headers=auth_headers)
    data_user1 = list_user1.json()

    assert data_user1["total"] == 1
    assert data_user1["items"][0]["title"] == "User 1 Book"

    # lista livros do usuário 2
    list_user2 = client.get("/books/", headers=auth_headers_user2)
    data_user2 = list_user2.json()

    assert data_user2["total"] == 1
    assert data_user2["items"][0]["title"] == "User 2 Book"


def test_user_cannot_access_other_users_book(client, auth_headers):
    # usuário 1 cria um livro
    create_response_user1 = client.post(
        "/books/",
        json={"title": "Private Book", "author": "Author", "status": "TO_READ"},
        headers=auth_headers,
    )
    assert create_response_user1.status_code == HTTPStatus.CREATED
    book_id = create_response_user1.json()["id"]

    # cria usuário 2
    client.post(
        "/users/",
        json={
            "email": "user2-access@example.com",
            "password": "12345678",
        },
    )
    login_user2 = client.post(
        "/users/token",
        data={
            "username": "user2-access@example.com",
            "password": "12345678",
        },
    )
    token_user2 = login_user2.json()["access_token"]
    auth_headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    # usuário 2 tenta buscar o livro do usuário 1
    get_response = client.get(f"/books/{book_id}", headers=auth_headers_user2)
    assert get_response.status_code == HTTPStatus.NOT_FOUND

    # usuário 2 tenta deletar o livro do usuário 1
    delete_response = client.delete(f"/books/{book_id}", headers=auth_headers_user2)
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
