from sqlalchemy.orm import (
    declared_attr,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime
from sqlalchemy import ForeignKey, String, func, Column, Table, Text


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


class Book(Base):
    title: Mapped[str] = mapped_column(String(500))
    year_published: Mapped[int]
    genre: Mapped[str] = mapped_column(String(100))
    num_pages: Mapped[int]
    availability: Mapped[str] = mapped_column(String(20))
    cover_url: Mapped[str | None]
    description: Mapped[str | None] = mapped_column(Text)

    authors: Mapped[list["Author"]] = relationship(
        secondary=author_book, back_populates="books"
    )

    def __str__(self) -> str:
        return self.title


class Author(Base):
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    books: Mapped[list["Book"] | None] = relationship(
        secondary=author_book, back_populates="authors"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
