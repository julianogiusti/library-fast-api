from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.books.router import router as books_router
from app.core.database import create_db_and_tables
from app.core.error_schema import ErrorResponse, utc_now_iso
from app.core.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    payload = ErrorResponse(
        type=type(exc).__name__,
        title=exc.title,
        detail=exc.message,
        status=exc.status_code,
        timestamp=utc_now_iso(),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    payload = ErrorResponse(
        type=type(exc).__name__,
        title="Validation error",
        detail="Request data is invalid.",
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        timestamp=utc_now_iso(),
    )
    content = payload.model_dump()
    content["errors"] = exc.errors()
    return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content=content)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    payload = ErrorResponse(
        type=type(exc).__name__,
        title="HTTP error",
        detail=str(exc.detail),
        status=exc.status_code,
        timestamp=utc_now_iso(),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    payload = ErrorResponse(
        type=type(exc).__name__,
        title="Internal server error",
        detail="An unexpected error occurred.",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        timestamp=utc_now_iso(),
    )
    return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=payload.model_dump())


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(books_router)
