from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB__",
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        env_nested_delimiter="__",
        extra="ignore",
    )
    user: str = Field(...)
    password: str = Field(...)
    db: str = Field(...)
    host: str = Field(...)
    port: int = Field(5432, ge=1, le=65535)
    dialect: str = Field(...)
    engine: str = Field(...)
    echo: bool = Field(False)
    future: bool = Field(True)

    @property
    def url(self) -> str:
        return f"{self.dialect}+aiosqlite:///./{self.db}.db"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP__",
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        case_sensitive=False,
        extra="ignore",
    )

    debug: bool = Field(False)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )
    # noinspection PyArgumentList
    db: DbSettings = DbSettings()
    # noinspection PyArgumentList
    app: AppSettings = AppSettings()


# noinspection PyArgumentList
settings = Settings()
