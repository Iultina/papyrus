from fastapi import APIRouter, Depends
from typing import Annotated

from app.schemas import (
    AuthorCreateSchema,
    AuthorReadBasicSchema,
    AuthorReadSchema,
)
from app.services.author_service import AuthorService
from app.dependencies.authors import get_author_service

router = APIRouter(tags=["authors"])


@router.get("/authors", response_model=list[AuthorReadSchema])
async def get_authors(
    service: Annotated[AuthorService, Depends(get_author_service)],
) -> list[AuthorReadSchema]:
    authors = await service.list_authors()
    return [AuthorReadSchema.model_validate(author) for author in authors]


@router.post("/authors", response_model=AuthorReadBasicSchema)
async def add_author(
    data: AuthorCreateSchema,
    service: Annotated[AuthorService, Depends(get_author_service)],
) -> AuthorReadBasicSchema:
    new_author = await service.add_author(data)
    return AuthorReadBasicSchema.model_validate(new_author)
