from typing import Sequence
from app.infra.database.models import Author
from app.schemas import AuthorCreateSchema
from app.repositories.unit_of_work import UnitOfWork


class AuthorService:
    """
    Сервис для работы с авторами.

    Обеспечивает бизнес-логику для получения списка авторов и добавления новых.
    Использует UnitOfWork для управления репозиториями и транзакциями.

    Атрибуты:
        uow (UnitOfWork): Единица работы, инкапсулирующая доступ к репозиториям и транзакциям.
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_authors(self) -> Sequence[Author]:
        return await self.uow.authors.get_list()

    async def add_author(self, data: AuthorCreateSchema) -> Author:
        author = Author(**data.model_dump())
        await self.uow.authors.add(author)
        await self.uow.commit()
        return author
