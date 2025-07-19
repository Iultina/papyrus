from typing import Protocol
from app.adapters.openlibrary import OpenLibraryAPI
from app.typing import ExternalBookData


class BookDataProvider(Protocol):
    """Протокол поставщика данных о книгах из внешних API.

    Любой класс, реализующий этот протокол, должен предоставлять
    метод для получения базовой информации о книге по её названию.
    """

    async def fetch_book_data(self, title: str) -> ExternalBookData | None:
        """Выполняет поиск книги по названию и возвращает объект с описанием и ссылкой на обложку, если найдены.

        Использует внешний источник (например, Open Library или Google Books) для получения дополнительных данных.
        """
        ...


class OpenLibraryAdapter(BookDataProvider):
    """Адаптер, приводящий OpenLibraryAPI к интерфейсу BookDataProvider."""

    def __init__(self, api: OpenLibraryAPI) -> None:
        self.api = api

    async def fetch_book_data(self, title: str) -> ExternalBookData | None:
        book = await self.api.search_book(title)
        if not book:
            return

        description_json = await self.api.get_description(book.get("key"))
        description = None

        if description_json:
            description = description_json.get("description")
        cover_url = (
            self.api.get_cover_url(book["cover_i"]) if "cover_i" in book else None
        )

        return ExternalBookData(description=description, cover_url=cover_url)
