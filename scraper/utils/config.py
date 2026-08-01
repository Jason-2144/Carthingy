import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class ScraperSettings(BaseSettings):
    REDIS_URL: str = "redis://redis:6379/1"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/carscope"
    MAX_RETRIES: int = 3
    PLAYWRIGHT_HEADLESS: bool = True
    CONCURRENCY: int = 5
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = ScraperSettings()
