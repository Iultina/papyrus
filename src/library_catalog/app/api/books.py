from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status


from app.schemas import (
    BookCreateSchema,
    BookFilterSchema,
    BookReadSchema,
)

from app.services.book_service import BookService
from app.exceptions import AuthorsNotFoundError, BookDeleteError, BookNotFoundError
from app.dependencies.books import get_book_service

router = APIRouter(tags=["books"])


@router.get("/books", response_model=list[BookReadSchema])
async def get_books(
    service: Annotated[BookService, Depends(get_book_service)],
    filters: BookFilterSchema = Depends(),
) -> list[BookReadSchema]:
    books = await service.list_books(filters)
    return [BookReadSchema.from_db(book) for book in books]


@router.get("/books/{book_id}", response_model=BookReadSchema)
async def get_book(
    book_id: int,
    service: Annotated[BookService, Depends(get_book_service)],
) -> BookReadSchema:
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return BookReadSchema.from_db(book)


@router.post("/books", response_model=BookReadSchema)
async def add_book(
    data: BookCreateSchema,
    service: Annotated[BookService, Depends(get_book_service)],
) -> BookReadSchema:
    try:
        book = await service.add_book(data)
        return BookReadSchema.from_db(book)
    except AuthorsNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/books/{book_id}", response_model=BookReadSchema)
async def update_book(
    book_id: int,
    service: Annotated[BookService, Depends(get_book_service)],
    data: BookCreateSchema = Body(...),
) -> BookReadSchema:
    try:
        book = await service.update_book(book_id, data)
        return BookReadSchema.from_db(book)
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AuthorsNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    service: Annotated[BookService, Depends(get_book_service)],
) -> None:
    try:
        await service.delete_book(book_id)
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BookDeleteError as e:
        raise HTTPException(status_code=500, detail=str(e))
