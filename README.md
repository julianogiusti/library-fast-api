# library-api

![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-7C3AED)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)

Simple Library API built with FastAPI and SQLModel to demonstrate structured backend architecture, pagination, filtering, centralized error handling and integration testing.

This project focuses on backend design principles rather than feature completeness.

---

## Tech Stack

- Python 3.14
- FastAPI
- SQLModel
- SQLite
- Pytest
- uv (environment management)

---

## Environment

Ubuntu 24.04.3 LTS

### Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

---

## Setup

### 1. Create virtual environment

```bash
uv python install 3.14
uv venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
uv sync
```

---

## Running the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## Database

- SQLite is used for simplicity
- The database file (`library.db`) is created automatically on first run
- No manual migrations are required

---

## Running tests

```bash
pytest
```

Tests use:

- SQLite in-memory database
- Dependency override for sessions
- Full integration testing via FastAPI TestClient

---

## Architecture

The project follows a responsibility-based structure:

```
app/
├── books/
│   ├── model.py        # SQLModel models
│   ├── repository.py   # Data access layer
│   ├── service.py      # Business logic
│   └── router.py       # HTTP layer
├── core/
│   ├── database.py     # Engine and session management
│   ├── exceptions.py   # Domain exceptions
│   └── error_schema.py # Standardized error response
└── main.py             # Application setup
```

### Layers

- **Router**: Handles HTTP concerns
- **Service**: Contains business rules
- **Repository**: Handles database interaction
- **Core**: Cross-cutting concerns

The service layer does not depend on FastAPI-specific exceptions.

---

## API Features

### CRUD operations

- Create book
- List books
- Get book by ID
- Update book
- Delete book

---

### Pagination

Query parameters:

- `page`
- `size`

Example:

```bash
curl "http://127.0.0.1:8000/books/?page=1&size=10"
```

---

### Filtering

Supported filters:

- `status`
- `author`
- `title`

Example:

```bash
curl "http://127.0.0.1:8000/books/?status=TO_READ&author=Martin"
```

---

### Ordering

Parameters:

- `order_by`
- `order` (asc | desc)

Example:

```bash
curl "http://127.0.0.1:8000/books/?order_by=title&order=asc"
```

---

## Error Handling

The API uses centralized exception handling.

All errors follow a standardized format:

```json
{
  "type": "NotFoundException",
  "title": "Not found",
  "detail": "Book not found",
  "status": 404,
  "timestamp": "2026-02-19T14:30:44.660365+00:00"
}
```

Validation errors (422) follow the same structure and include additional details.

---

## Design Decisions

### SQLModel
Chosen to combine SQLAlchemy and Pydantic in a clean and typed way.

### Service Layer
Business logic is isolated from HTTP framework concerns.

### Centralized Error Handling
Prevents scattered HTTPException usage and ensures consistent API responses.

### Integration Testing
Validates real behavior including pagination, filtering and ordering.

---

## Project Goals

This project demonstrates:

- Structured backend design
- Clean separation of concerns
- Centralized error handling
- Integration testing strategy
- Consistent API contracts

---

## Future Improvements

- PostgreSQL support
- Deployment configuration
- Frontend integration (React)

---

## Code Quality (Ruff + pre-commit)

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [pre-commit](https://pre-commit.com/) to automatically run checks before commits.

### Install git hooks

```bash
uv run pre-commit install
```

### Run hooks on all files (without committing)

```bash
uv run pre-commit run --all-files
```

### Run hooks on specific files

```bash
uv run pre-commit run --files <file>
```

### Run a specific hook

```bash
uv run pre-commit run <hook_id> --all-files
uv run pre-commit run <hook_id> --files <file>
```

### Run Ruff manually

```bash
uv run ruff check . --fix
uv run ruff format .
```
