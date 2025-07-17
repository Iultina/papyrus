from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.models import Book
from app.schemas import BookFilterSchema


class BookRepository:
    """
    Репозиторий для выполнения операций с книгами (Book) в базе данных.

    Предоставляет методы для фильтрации, получения по ID, добавления и удаления книг.
    Работает с асинхронной сессией SQLAlchemy.

    Атрибуты:
        _session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.

    Методы:
        list(filters: BookFilterSchema) -> Sequence[Book]:
            Возвращает список книг, отфильтрованных по переданным параметрам.

        get_by_id(book_id: int) -> Book | None:
            Возвращает книгу по её ID или None, если книга не найдена.

        add(book: Book) -> None:
            Добавляет новую книгу в сессию (без коммита).

        delete(book: Book) -> None:
            Удаляет книгу из базы данных.
    """

    def __init__(self, async_session: AsyncSession) -> None:
        self._session = async_session

    async def list(self, filters: BookFilterSchema) -> Sequence[Book]:
        query = select(Book).options(selectinload(Book.authors))

        if filters.title:
            query = query.filter(Book.title.ilike(f"%{filters.title}%"))
        if filters.genre:
            query = query.filter(Book.genre.ilike(filters.genre))
        if filters.availability:
            query = query.filter(Book.availability == filters.availability)
        if filters.year_published:
            query = query.filter(Book.year_published == filters.year_published)

        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Book | None:
        result = await self._session.execute(
            select(Book).where(Book.id == book_id).options(selectinload(Book.authors))
        )
        return result.scalar_one_or_none()

    async def add(self, book: Book) -> None:
        self._session.add(book)

    async def delete(self, book: Book) -> None:
        await self._session.delete(book)
