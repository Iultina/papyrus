from src.library_catalog.db import SessionDep
from src.library_catalog.models import Author
from src.library_catalog.schemas import (
    AuthorCreateSchema,
    AuthorReadBasicSchema,
    AuthorReadSchema,
)
from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

author_router = APIRouter()


@author_router.get("/authors", response_model=list[AuthorReadSchema])
async def get_authors(session: SessionDep) -> list[AuthorReadSchema]:
    result = await session.execute(select(Author).options(selectinload(Author.books)))
    authors = result.scalars().all()
    return [AuthorReadSchema.model_validate(author) for author in authors]


@author_router.post("/authors/add_author", response_model=AuthorReadBasicSchema)
async def add_author(
    author: AuthorCreateSchema, session: SessionDep
) -> AuthorReadBasicSchema:
    new_author = Author(**author.model_dump())
    session.add(new_author)

    await session.commit()
    await session.refresh(new_author)

    return AuthorReadBasicSchema.model_validate(new_author)
