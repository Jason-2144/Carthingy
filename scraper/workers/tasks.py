import asyncio
import logging
from celery import shared_task
from playwright.async_api import async_playwright
from scraper.connectors.facebook.connector import FacebookMarketplaceConnector
from scraper.connectors.olx.connector import OLXConnector
from scraper.parsers.facebook import FacebookParser
from scraper.parsers.olx import OLXParser
from scraper.database.repository import ScraperRepository
from backend.database.config import AsyncSessionLocal
from scraper.utils.config import settings

logger = logging.getLogger(__name__)

async def run_scrape_marketplace(marketplace: str, query: str, filters: dict):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
        
        if marketplace.lower() == "facebook":
            connector = FacebookMarketplaceConnector(browser)
        elif marketplace.lower() == "olx":
            connector = OLXConnector(browser)
        else:
            logger.error(f"Unknown marketplace: {marketplace}")
            return

        await connector.initialize()
        await connector.login()

        urls_found = 0
        try:
            async for url in connector.search(query, filters):
                urls_found += 1
                # Dispatch individual listing processing task
                process_listing.delay(marketplace, url)
        except Exception as e:
            logger.error(f"Error during search: {e}")
        finally:
            await connector.shutdown()
            logger.info(f"Finished scraping {marketplace} for '{query}'. Found {urls_found} listings.")


@shared_task(name="scraper.workers.tasks.scrape_marketplace")
def scrape_marketplace(marketplace: str, query: str = "", filters: dict = {}):
    """
    Entry point for a full marketplace scrape. 
    It searches and queues individual listing URLs to be processed.
    """
    logger.info(f"Starting scrape job for {marketplace} - query: {query}")
    asyncio.run(run_scrape_marketplace(marketplace, query, filters))


async def run_process_listing(marketplace: str, url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
        
        connector = None
        parser = None
        
        if marketplace.lower() == "facebook":
            connector = FacebookMarketplaceConnector(browser)
            parser = FacebookParser()
        elif marketplace.lower() == "olx":
            connector = OLXConnector(browser)
            parser = OLXParser()

        if not connector:
            return

        await connector.initialize()
        try:
            raw_data = await connector.extract_listing(url)
            parsed_data = parser.parse(raw_data)
            
            async with AsyncSessionLocal() as session:
                repo = ScraperRepository(session)
                await repo.save_listing(parsed_data)
        except Exception as e:
            logger.error(f"Failed to process {url}: {e}")
        finally:
            await connector.shutdown()


@shared_task(name="scraper.workers.tasks.process_listing", bind=True, max_retries=3)
def process_listing(self, marketplace: str, url: str):
    """
    Processes a single listing URL. Extracts data, parses, and saves to DB.
    """
    try:
        asyncio.run(run_process_listing(marketplace, url))
    except Exception as exc:
        logger.error(f"Task failed, retrying: {exc}")
        self.retry(exc=exc, countdown=2 ** self.request.retries)
