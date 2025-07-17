from dataclasses import dataclass


@dataclass
class ExternalBookData:
    """Данные о книге, полученные из внешнего источника.

    Атрибуты:
        description: Краткое описание книги, если доступно.
        cover_url: Ссылка на обложку книги в подходящем разрешении.
    """

    description: str | None
    cover_url: str | None
