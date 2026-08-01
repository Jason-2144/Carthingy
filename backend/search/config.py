from pydantic_settings import BaseSettings
from typing import Optional

class SearchSettings(BaseSettings):
    # Meilisearch Config
    MEILI_URL: str = "http://localhost:7700"
    MEILI_MASTER_KEY: str = "masterKey"
    
    # Indexes
    LISTINGS_INDEX: str = "listings"
    CARS_INDEX: str = "cars"
    
    # Redis for Analytics
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # NLP Config (if using local lightweight parsing)
    ENABLE_NLP_PARSING: bool = True

    class Config:
        env_prefix = "SEARCH_"

search_settings = SearchSettings()
