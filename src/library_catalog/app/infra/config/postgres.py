from pydantic import Field
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_user: str = Field(validation_alias="POSTGRES_USER")
    postgres_password: str = Field(validation_alias="POSTGRES_PASSWORD")
    db_host: str = Field(validation_alias="DB_HOST", default="localhost")
    db_port: int = Field(validation_alias="DB_PORT", default=5432)
    postgres_db: str = Field(validation_alias="POSTGRES_DB")

    # @computed_field(return_type=str) Надо?
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )
