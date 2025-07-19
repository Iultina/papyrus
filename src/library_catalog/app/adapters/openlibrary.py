from app.adapters.base_api_client import HTTPClient


class OpenLibraryAPI(HTTPClient):
    """
    Клиент для взаимодействия с OpenLibrary API.

    Предоставляет методы для поиска книг, получения описания книги и построения ссылки на обложку.

    Атрибуты:
        base_url (str): Базовый URL OpenLibrary API (например, https://openlibrary.org).
        covers_url (str): Базовый URL для загрузки обложек (например, https://covers.openlibrary.org).

    Методы:
        search_book(title: str) -> dict | None:
            Выполняет поиск книги по названию и возвращает первое совпадение.

        get_description(key: str | None) -> dict | None:
            Получает подробное описание книги по её ключу (например, "/works/OL82563W").

        get_cover_url(cover_id: int, size: str = "L") -> str:
            Возвращает URL обложки книги по её идентификатору и размеру (S, M, L).
    """

    def __init__(self, base_url: str, covers_url: str):
        super().__init__(base_url=base_url)
        self.covers_url = covers_url

    async def search_book(self, title: str) -> dict | None:
        endpoint = f"{self.base_url}/search.json"
        params = {"q": title}
        data = await self._send_request("GET", endpoint, params=params)
        if not data:
            return
        for doc in data.get("docs", []):
            if doc.get("title", "").lower() == title.lower():
                return doc

    async def get_description(self, key: str | None) -> dict | None:
        if not key:
            return
        endpoint = f"{self.base_url}/{key}.json"
        return await self._send_request("GET", endpoint, follow_redirects=True)

    def get_cover_url(self, cover_id: int, size: str = "L") -> str:
        return f"{self.covers_url}/b/id/{cover_id}-{size}.jpg"
