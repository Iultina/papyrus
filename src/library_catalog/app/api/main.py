from fastapi import FastAPI


def configure(api: FastAPI):
    from app.api import authors, books

    api.include_router(books.router, prefix="/books")
    api.include_router(authors.router, prefix="/authors")
