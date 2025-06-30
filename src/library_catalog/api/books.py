from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.library_catalog.utils import update_book_with_external_data
from src.library_catalog.adapters import BookDataProvider
from src.library_catalog.dependencies import get_book_data_provider
from src.library_catalog.db import SessionDep
from src.library_catalog.models import Author, Book
from src.library_catalog.schemas import (
    BookCreateSchema,
    BookFilterSchema,
    BookReadSchema,
)

book_router = APIRouter()


@book_router.get("/books", response_model=list[BookReadSchema])
async def get_books(
    session: SessionDep, filters: BookFilterSchema = Depends()
) -> list[BookReadSchema]:
    query = select(Book).options(selectinload(Book.authors))

    if filters.title:
        query = query.filter(Book.title.ilike(f"%{filters.title}%"))

    if filters.genre:
        query = query.filter(Book.genre.ilike(filters.genre))

    if filters.availability:
        query = query.filter(Book.availability == filters.availability)

    if filters.year_published:
        query = query.filter(Book.year_published == filters.year_published)

    result = await session.execute(query)
    books = result.scalars().all()
    return [BookReadSchema.from_db(book) for book in books]


@book_router.get("/books/{book_id}", response_model=BookReadSchema)
async def get_book(book_id: int, session: SessionDep) -> BookReadSchema:
    query = select(Book).where(Book.id == book_id).options(selectinload(Book.authors))
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return BookReadSchema.from_db(book)


@book_router.post("/books/add_book", response_model=BookReadSchema)
async def add_book(
    book: BookCreateSchema,
    session: SessionDep,
    provider: Annotated[BookDataProvider, Depends(get_book_data_provider)],
) -> BookReadSchema:
    result = await session.execute(select(Author).where(Author.id.in_(book.authors)))
    author_objs = list(result.scalars().all())

    if len(author_objs) != len(book.authors):
        raise HTTPException(status_code=400, detail="Некоторые авторы не найдены")

    new_book = Book(**book.model_dump(exclude={"authors"}))
    new_book.authors = author_objs

    await update_book_with_external_data(new_book, provider)

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    await session.refresh(new_book, attribute_names=["authors"])

    return BookReadSchema.from_db(new_book)


@book_router.put("/books/{book_id}", response_model=BookReadSchema)
async def update_book(
    book_id: int,
    session: SessionDep,
    provider: Annotated[BookDataProvider, Depends(get_book_data_provider)],
    updated_data: BookCreateSchema = Body(
        ..., description="Новые данные для обновления книги"
    ),
) -> BookReadSchema:
    query = select(Book).where(Book.id == book_id).options(selectinload(Book.authors))
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    data = updated_data.model_dump()

    # обработка авторов
    if "authors" in data:
        result = await session.execute(
            select(Author).where(Author.id.in_(data["authors"]))
        )
        author_objs = list(result.scalars().all())

        if len(author_objs) != len(data["authors"]):
            raise HTTPException(status_code=400, detail="Некоторые авторы не найдены")

        book.authors = author_objs
        del data["authors"]

    for key, value in data.items():
        setattr(book, key, value)

    await update_book_with_external_data(book, provider)

    await session.commit()
    await session.refresh(book)

    return BookReadSchema.from_db(book)


@book_router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: SessionDep) -> None:
    query = select(Book).where(Book.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    await session.delete(book)
    await session.commit()
