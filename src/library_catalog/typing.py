from dataclasses import dataclass
from typing import Protocol


@dataclass
class ExternalBookData:
    """Данные о книге, полученные из внешнего источника.

    Атрибуты:
        description: Краткое описание книги, если доступно.
        cover_url: Ссылка на обложку книги в подходящем разрешении.
    """

    description: str | None
    cover_url: str | None


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
