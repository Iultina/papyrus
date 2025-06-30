from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///papyrus.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_async_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
