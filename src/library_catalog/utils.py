from src.library_catalog.models import Book

from src.library_catalog.adapters import BookDataProvider


async def update_book_with_external_data(
    new_book: Book, provider: BookDataProvider
) -> None:
    external_data = await provider.fetch_book_data(new_book.title)
    if external_data:
        new_book.description = external_data.description
        new_book.cover_url = external_data.cover_url
