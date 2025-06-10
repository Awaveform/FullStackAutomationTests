from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    API_BASE: Optional[str]
    UI_BASE: Optional[str]

    model_config = {
        "env_file": str(Path(__file__).resolve().parents[1] / ".env"),
        "env_file_encoding": "utf-8",
    }


@lru_cache()
def settings() -> Settings:
    return Settings()


env_settings: Settings = settings()
