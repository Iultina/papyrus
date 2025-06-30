from src.library_catalog.adapters import OpenLibraryAdapter
from src.library_catalog.typing import BookDataProvider


def get_book_data_provider() -> BookDataProvider:
    return OpenLibraryAdapter()
