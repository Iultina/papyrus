from typing import Annotated
from app.repositories.unit_of_work import UnitOfWork
from app.infra.database.db import get_async_session
from app.services.author_service import AuthorService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_author_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthorService:
    return AuthorService(uow=UnitOfWork(session))
