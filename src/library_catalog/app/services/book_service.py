from typing import Sequence
from app.infra.database.models import Author, Book
from app.schemas import BookCreateSchema, BookFilterSchema
from app.adapters.adapters import BookDataProvider
from app.repositories.unit_of_work import UnitOfWork
from loguru import logger

from app.exceptions import AuthorsNotFoundError, BookDeleteError, BookNotFoundError


class BookService:
    """
    Сервис для управления книгами.

    Инкапсулирует бизнес-логику работы с сущностями книг, включая создание,
    обновление, удаление, получение и обогащение данными из внешнего источника.

    Атрибуты:
        uow (UnitOfWork): Единица работы, предоставляющая доступ к репозиториям и управлению транзакциями.
        provider (BookDataProvider): Источник внешних данных для обогащения информации о книгах.
    """

    def __init__(self, uow: UnitOfWork, provider: BookDataProvider):
        self.uow = uow
        self.provider = provider

    async def list_books(self, filters: BookFilterSchema) -> Sequence[Book]:
        return await self.uow.books.list(filters)

    async def get_book_by_id(self, book_id: int) -> Book | None:
        return await self.uow.books.get_by_id(book_id)

    async def add_book(self, data: BookCreateSchema) -> Book:
        authors = await self._resolve_authors(data.authors)

        book = Book(**data.model_dump(exclude={"authors"}))
        book.authors = authors

        await self._update_book_with_external_data(book)
        await self.uow.books.add(book)
        await self.uow.commit()
        return book

    async def update_book(self, book_id: int, data: BookCreateSchema) -> Book:
        book = await self.uow.books.get_by_id(book_id)
        if not book:
            raise ValueError("Книга не найдена")

        update_data = data.model_dump()

        if "authors" in update_data:
            book.authors = await self._resolve_authors(update_data["authors"])
            del update_data["authors"]

        for key, value in update_data.items():
            setattr(book, key, value)

        await self._update_book_with_external_data(book)
        await self.uow.commit()
        await self.uow.session.refresh(book)
        return book

    async def delete_book(self, book_id: int) -> None:
        book = await self.uow.books.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(f"Книга с id {book_id} не найдена")

        try:
            await self.uow.books.delete(book)
            await self.uow.commit()
            logger.info(f"Книга с id {book_id} удалена")
        except Exception as e:
            await self.uow.rollback()
            logger.error(f"Ошибка при удалении книги с id {book_id}: {e}")
            raise BookDeleteError(f"Ошибка при удалении книги с id {book_id}") from e

    async def _update_book_with_external_data(
        self,
        new_book: Book,
    ) -> None:
        external_data = await self.provider.fetch_book_data(new_book.title)
        if external_data:
            new_book.description = external_data.description
            new_book.cover_url = external_data.cover_url

    async def _resolve_authors(self, ids: list[int]) -> list[Author]:
        authors = await self.uow.authors.get_by_ids(ids)
        authors_by_id = {a.id: a for a in authors}
        missing = [i for i in ids if i not in authors_by_id]
        if missing:
            logger.warning(f"Авторы не найдены: {missing}")
            raise AuthorsNotFoundError(f"Некоторые авторы не найдены: {missing}")
        return list(authors_by_id.values())
