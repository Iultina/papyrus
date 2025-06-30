from fastapi import FastAPI

from src.library_catalog.models import Base
from src.library_catalog.db import async_engine
from src.library_catalog.api.authors import author_router
from src.library_catalog.api.books import book_router

app = FastAPI()


app.include_router(book_router, prefix="/api", tags=["Books"])
app.include_router(author_router, prefix="/api", tags=["Authors"])


@app.on_event("startup")
async def on_startup() -> None:
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# uvicorn src.library_catalog.main:app --reload
