import asyncio
import logging
from typing import AsyncGenerator
from playwright.async_api import Browser, Page, TimeoutError as PlaywrightTimeoutError
from scraper.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class OLXConnector(BaseConnector):
    MARKETPLACE_NAME = "OLX"
    BASE_URL = "https://www.olx.in"

    async def initialize(self) -> None:
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()

    async def login(self) -> bool:
        return True

    async def search(self, query: str = "", filters: dict = {}) -> AsyncGenerator[str, None]:
        search_url = f"{self.BASE_URL}/cars_c84?q={query}"
        
        await self.page.goto(search_url, wait_until="networkidle")

        # Handle Load More button pagination
        for _ in range(5):
            urls = await self._extract_urls_from_page()
            for url in urls:
                yield url
            
            try:
                load_more = await self.page.query_selector('button[data-aut-id="btnLoadMore"]')
                if load_more and await load_more.is_visible():
                    await load_more.click()
                    await asyncio.sleep(2)
                else:
                    break
            except Exception:
                break

    async def _extract_urls_from_page(self) -> list[str]:
        elements = await self.page.query_selector_all('li[data-aut-id="itemBox"] a')
        urls = []
        for el in elements:
            href = await el.get_attribute("href")
            if href:
                urls.append(f"{self.BASE_URL}{href}")
        return list(set(urls))

    async def extract_listing(self, url: str) -> dict:
        try:
            await self.page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(1)

            title = await self._safe_text_content('h1[data-aut-id="itemTitle"]')
            price = await self._safe_text_content('span[data-aut-id="itemPrice"]')
            description = await self._safe_text_content('div[data-aut-id="itemDescriptionContent"]')
            
            # Key value attributes (Brand, Model, Year, KM driven)
            attributes = await self.page.evaluate('''() => {
                const attrNodes = document.querySelectorAll('div[data-aut-id="itemParams"] div');
                return Array.from(attrNodes).map(node => node.innerText);
            }''')

            # Images
            images = await self.page.evaluate('''() => {
                const imgNodes = document.querySelectorAll('div.image-gallery-slide img');
                return Array.from(imgNodes).map(img => img.src);
            }''')

            seller_name = await self._safe_text_content('div[data-aut-id="profileCard"] span')

            return {
                "url": url,
                "title": title,
                "price": price,
                "description": description,
                "attributes": attributes,
                "images": images,
                "seller_name": seller_name,
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
