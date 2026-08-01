from abc import ABC, abstractmethod
from typing import AsyncGenerator
from playwright.async_api import Browser, Page

class BaseConnector(ABC):
    """
    Interface that all marketplace connectors must implement.
    Ensures a consistent API for the worker to interact with regardless of the marketplace.
    """
    
    def __init__(self, browser: Browser):
        self.browser = browser
        self.page: Page | None = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the page context and any specific headers/cookies."""
        pass

    @abstractmethod
    async def login(self) -> bool:
        """Perform login if the marketplace requires authentication."""
        pass

    @abstractmethod
    async def search(self, query: str = "", filters: dict = {}) -> AsyncGenerator[str, None]:
        """
        Execute search and yield listing URLs.
        Handles pagination internally.
        """
        pass

    @abstractmethod
    async def extract_listing(self, url: str) -> dict:
        """
        Open a specific listing URL, extract raw data and return as a dictionary.
        This dict will be passed to the parser/normalizer.
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Clean up resources, close pages/contexts."""
        pass
