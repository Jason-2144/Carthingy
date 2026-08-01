import asyncio
import logging
from typing import AsyncGenerator
from playwright.async_api import Browser, Page, TimeoutError as PlaywrightTimeoutError
from scraper.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class FacebookMarketplaceConnector(BaseConnector):
    MARKETPLACE_NAME = "Facebook Marketplace"
    BASE_URL = "https://www.facebook.com/marketplace"

    async def initialize(self) -> None:
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()

    async def login(self) -> bool:
        # FB Marketplace can often be searched without login for public listings,
        # but complex scraping might require session cookies injected here.
        # For this design, we assume public access or session cookies injected via context.
        return True

    async def search(self, query: str = "", filters: dict = {}) -> AsyncGenerator[str, None]:
        search_url = f"{self.BASE_URL}/search?query={query}"
        # Apply filters to URL as needed based on FB's URL schema
        if "city_id" in filters:
            search_url = f"{self.BASE_URL}/{filters['city_id']}/search?query={query}"

        await self.page.goto(search_url, wait_until="networkidle")

        # Handle Infinite scroll pagination
        for _ in range(5):  # Example: 5 scrolls
            urls = await self._extract_urls_from_page()
            for url in urls:
                yield url
            
            # Scroll down
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2) # Wait for network requests

    async def _extract_urls_from_page(self) -> list[str]:
        # FB specific selector logic (subject to change, using generic placeholders for architecture)
        elements = await self.page.query_selector_all('a[href*="/marketplace/item/"]')
        urls = []
        for el in elements:
            href = await el.get_attribute("href")
            if href:
                urls.append(f"https://www.facebook.com{href}")
        return list(set(urls))

    async def extract_listing(self, url: str) -> dict:
        try:
            await self.page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(1) # Give SPA time to render

            # Extract raw DOM strings. The parser will handle structuring this.
            title = await self._safe_text_content('h1 span')
            price = await self._safe_text_content('div.x1xlc1qs span.x193iq5w')
            description = await self._safe_text_content('div.xz9dl7a')
            
            # Additional elements (Mileage, Fuel, Transmission, etc.) usually in a grid
            attributes = await self.page.evaluate('''() => {
                const attrNodes = document.querySelectorAll('div.x1n2onr6.x1vvkbs');
                return Array.from(attrNodes).map(node => node.innerText);
            }''')

            # Images
            images = await self.page.evaluate('''() => {
                const imgNodes = document.querySelectorAll('img');
                return Array.from(imgNodes).map(img => img.src).filter(src => src.includes('scontent'));
            }''')

            return {
                "url": url,
                "title": title,
                "price": price,
                "description": description,
                "attributes": attributes,
                "images": images,
                "marketplace": self.MARKETPLACE_NAME
            }
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while extracting {url}")
            return {"error": "timeout", "url": url}

    async def _safe_text_content(self, selector: str) -> str | None:
        element = await self.page.query_selector(selector)
        if element:
            return await element.text_content()
        return None

    async def shutdown(self) -> None:
        if self.page:
            await self.page.close()
        if hasattr(self, 'context'):
            await self.context.close()
