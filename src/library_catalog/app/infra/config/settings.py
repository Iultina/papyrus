from dotenv import load_dotenv
from loguru import logger
from pydantic import Field
from sys import exit
from app.infra.config.postgres import PostgresSettings


class Settings(PostgresSettings):
    host: str = Field(validation_alias="HOST", default="127.0.0.1")
    port: int = Field(validation_alias="PORT", default=5100)
    # storage_path: str = Field(validation_alias="STORAGE_PATH", default="/tmp")
    book_api_url: str = Field(
        validation_alias="BOOK_API_URL", default="https://openlibrary.org"
    )
    book_covers_api_url: str = Field(
        validation_alias="BOOK_COVERS_API_URL", default="https://covers.openlibrary.org"
    )


def _generate() -> Settings:
    load_dotenv()
    try:
        return Settings()
    except Exception as e:
        logger.error(e)
        exit(1)


settings = _generate()
