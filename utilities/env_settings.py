from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PLAYWRIGHT_TIMEOUT: str
    PLAYWRIGHT_SLOWMO: str
    HEADLESS: bool = Field(..., alias="HEADLESS")

    LOG_LEVEL: str

    API_BASE: str
    UI_BASE: str

    model_config = {
        "env_file": str(Path(__file__).resolve().parents[1] / ".env"),
        "env_file_encoding": "utf-8",
    }


@lru_cache()
def settings() -> Settings:
    """
    Cached accessor for environment-based settings.
    Loads configuration values from a .env file using Pydantic settings.

    :return: Settings instance
    """

    return Settings()


env_settings: Settings = settings()
