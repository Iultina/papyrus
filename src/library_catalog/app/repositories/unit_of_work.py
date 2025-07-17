from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.books import BookRepository
from app.repositories.authors import AuthorRepository


class UnitOfWork:
    """
    Координирует работу с несколькими репозиториями в рамках одной транзакции.

    Позволяет управлять жизненным циклом сессии базы данных, а также обеспечивает
    единый доступ к репозиториям книг и авторов.

    Атрибуты:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой.
        books (BookRepository): Репозиторий для работы с сущностями книг.
        authors (AuthorRepository): Репозиторий для работы с сущностями авторов.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.books = BookRepository(session)
        self.authors = AuthorRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
