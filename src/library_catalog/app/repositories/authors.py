from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.database.models import Author


class AuthorRepository:
    """
    Репозиторий для работы с сущностями Author в базе данных.

    Использует асинхронную сессию SQLAlchemy для выполнения операций чтения и записи.

    Атрибуты:
        _session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Методы:
        get_list() -> Sequence[Author]:
            Возвращает список всех авторов с предзагрузкой связанных книг.

        get_by_ids(author_ids: list[int]) -> Sequence[Author]:
            Возвращает список авторов по переданным ID.

        add(author: Author) -> None:
            Добавляет нового автора в текущую сессию (без коммита).
    """

    def __init__(self, async_session: AsyncSession) -> None:
        self._session = async_session

    async def get_list(self) -> Sequence[Author]:
        result = await self._session.execute(
            select(Author).options(selectinload(Author.books))
        )
        authors: Sequence[Author] = result.scalars().all()
        return authors

    async def get_by_ids(self, author_ids: list[int]) -> Sequence[Author]:
        result = await self._session.execute(
            select(Author).where(Author.id.in_(author_ids))
        )
        authors: Sequence[Author] = result.scalars().all()
        return authors

    async def add(self, author: Author) -> None:
        self._session.add(author)
