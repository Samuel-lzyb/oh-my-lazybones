"""Application configuration — all settings from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App-wide settings, loaded from environment or .env file."""

    database_url: str = "sqlite+aiosqlite:///lazybones.db"
    meili_url: str = "http://localhost:7700"
    meili_master_key: str = "dev-master-key"
    environment: str = "development"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
