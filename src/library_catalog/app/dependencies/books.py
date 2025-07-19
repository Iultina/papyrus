from typing import Annotated
from app.repositories.unit_of_work import UnitOfWork
from app.services.book_service import BookService
from app.adapters.adapters import BookDataProvider, OpenLibraryAdapter
from app.adapters.openlibrary import OpenLibraryAPI
from app.infra.config import settings
from app.infra.database.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_book_data_provider() -> BookDataProvider:
    return OpenLibraryAdapter(
        api=OpenLibraryAPI(
            base_url=settings.book_api_url, covers_url=settings.book_covers_api_url
        )
    )


def get_book_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    provider: Annotated[BookDataProvider, Depends(get_book_data_provider)],
) -> BookService:
    return BookService(uow=UnitOfWork(session), provider=provider)
