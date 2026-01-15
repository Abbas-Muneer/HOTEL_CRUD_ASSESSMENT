import os
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field("super-secret-key", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = Field("sqlite:///./app.db", env="DATABASE_URL")
    FRONTEND_ORIGIN: str = Field("http://localhost:5173", env="FRONTEND_ORIGIN")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
