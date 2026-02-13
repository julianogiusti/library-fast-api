from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from app.core.database import create_db_and_tables
from app.books.router import router as books_router
from app.core.exceptions import NotFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(books_router)
