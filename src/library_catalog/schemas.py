from pydantic import BaseModel


from pydantic import Field
from typing import Literal, Self
from datetime import datetime


class AuthorBaseSchema(BaseModel):
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorReadBasicSchema(AuthorBaseSchema):
    id: int


class AuthorReadSchema(AuthorReadBasicSchema):
    books: list["BookBaseSchema"] | None = None


class BookBaseSchema(BaseModel):
    title: str
    year_published: int = Field(ge=1)
    genre: str
    num_pages: int = Field(ge=0)
    availability: Literal["в наличии", "выдана"]

    model_config = {"from_attributes": True}

    @classmethod
    def from_db(cls, book) -> Self:
        return cls(
            title=book.title,
            year_published=book.year_published,
            genre=book.genre,
            num_pages=book.num_pages,
            availability=book.availability,
        )


class BookCreateSchema(BookBaseSchema):
    authors: list[int]


class BookReadSchema(BookBaseSchema):
    id: int
    authors: list["AuthorReadBasicSchema"]
    created_at: datetime
    updated_at: datetime
    description: str | None
    cover_url: str | None

    @classmethod
    def from_db(cls, book) -> Self:
        return cls(
            id=book.id,
            title=book.title,
            year_published=book.year_published,
            genre=book.genre,
            num_pages=book.num_pages,
            availability=book.availability,
            description=book.description,
            cover_url=book.cover_url,
            authors=[
                AuthorReadBasicSchema.model_validate(author)
                for author in (book.authors or [])
            ],
            created_at=book.created_at,
            updated_at=book.updated_at,
        )


class BookFilterSchema(BaseModel):
    title: str | None = None
    genre: str | None = None
    availability: Literal["в наличии", "выдана"] | None = None
    year_published: int | None = None
