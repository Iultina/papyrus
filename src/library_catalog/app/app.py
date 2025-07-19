from fastapi import FastAPI
from loguru import logger
from app.api import main as book_api


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/docs", redoc_url="/docs")
    try:
        book_api.configure(app)
    except Exception as error:
        logger.error("Ошибка при конфигурации приложения: {e}")
        raise error
    return app


app = create_app()
