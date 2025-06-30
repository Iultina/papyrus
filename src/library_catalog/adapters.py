from src.library_catalog.api.openlibrary import OpenLibraryAPI
from src.library_catalog.typing import BookDataProvider, ExternalBookData


class OpenLibraryAdapter(BookDataProvider):
    """Адаптер, приводящий OpenLibraryAPI к интерфейсу BookDataProvider."""

    def __init__(self) -> None:
        self.api = OpenLibraryAPI()

    async def fetch_book_data(self, title: str) -> ExternalBookData | None:
        book = await self.api.search_book(title)
        if not book:
            return None

        description_json = (
            await self.api.get_description(book.get("key", ""))
            if book.get("key")
            else None
        )
        description = None

        if description_json:
            description = description_json.get("description")
        cover_url = (
            self.api.get_cover_url(book["cover_i"]) if "cover_i" in book else None
        )

        return ExternalBookData(description=description, cover_url=cover_url)
