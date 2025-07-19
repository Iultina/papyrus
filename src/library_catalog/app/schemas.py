from typing import Annotated, Literal
from datetime import datetime
from pydantic import BaseModel, Field, conint

Str50 = Annotated[str, Field(min_length=1, max_length=50, strip_whitespace=True)]
Str100 = Annotated[str, Field(min_length=1, max_length=100, strip_whitespace=True)]
Str500 = Annotated[str, Field(min_length=1, max_length=500, strip_whitespace=True)]
Year = Annotated[int, Field(ge=1, le=2100)]
Pages = Annotated[int, Field(ge=1, le=50000)]


class AuthorBaseSchema(BaseModel):
    first_name: Str50
    last_name: Str50

    model_config = {"from_attributes": True}


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorReadBasicSchema(AuthorBaseSchema):
    id: int


class AuthorReadSchema(AuthorReadBasicSchema):
    books: list["BookBaseSchema"] | None = None


class BookBaseSchema(BaseModel):
    title: Str500
    year_published: Year
    genre: Str100
    num_pages: Pages
    availability: Literal["в наличии", "выдана"]

    model_config = {"from_attributes": True}

    @classmethod
    def from_db(cls, book) -> "Self":
        return cls(
            title=book.title,
            year_published=book.year_published,
            genre=book.genre,
            num_pages=book.num_pages,
            availability=book.availability,
        )


class BookCreateSchema(BookBaseSchema):
    authors: list[conint(strict=True, ge=1)] = Field(min_length=1)


class BookReadSchema(BookBaseSchema):
    id: int
    authors: list["AuthorReadBasicSchema"]
    created_at: datetime
    updated_at: datetime
    description: str | None
    cover_url: str | None

    @classmethod
    def from_db(cls, book) -> "Self":
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
    title: Str500 | None = None
    genre: Str100 | None = None
    availability: Literal["в наличии", "выдана"] | None = None
    year_published: Year | None = None
