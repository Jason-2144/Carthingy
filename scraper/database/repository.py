from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import uuid
from backend.models.listings import Listing
from backend.models.history import PriceHistory, Image
from backend.models.sellers import Seller
from backend.models.marketplaces import Marketplace
from scraper.deduplication.detector import DeduplicationEngine
import logging

logger = logging.getLogger(__name__)

class ScraperRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.dedup = DeduplicationEngine(session)

    async def get_or_create_marketplace(self, name: str) -> Marketplace:
        query = select(Marketplace).filter(Marketplace.name == name)
        result = await self.session.execute(query)
        mp = result.scalars().first()
        if not mp:
            mp = Marketplace(name=name)
            self.session.add(mp)
            await self.session.flush()
        return mp

    async def get_or_create_seller(self, marketplace_id: uuid.UUID, name: str) -> Seller:
        query = select(Seller).filter(Seller.marketplace_id == marketplace_id, Seller.name == name)
        result = await self.session.execute(query)
        seller = result.scalars().first()
        if not seller:
            seller = Seller(marketplace_id=marketplace_id, name=name)
            self.session.add(seller)
            await self.session.flush()
        return seller

    async def save_listing(self, parsed_data: dict) -> Listing | None:
        if "error" in parsed_data:
            logger.warning(f"Skipping saving listing due to error: {parsed_data['error']}")
            return None
            
        mp = await self.get_or_create_marketplace(parsed_data["marketplace"])
        seller = await self.get_or_create_seller(mp.id, parsed_data["seller_name"])

        # Check existing
        existing = await self.dedup.find_existing(mp.id, parsed_data["external_listing_id"])
        
        now = datetime.now(timezone.utc)
        price = parsed_data.get("price")

        if existing:
            # Update last seen
            existing.last_seen = now
            
            # Check price change
            if price and existing.price != price:
                ph = PriceHistory(
                    listing_id=existing.id,
                    marketplace_id=mp.id,
                    old_price=existing.price,
                    new_price=price,
                    timestamp=now
                )
                self.session.add(ph)
                existing.price = price
                logger.info(f"Price updated for {existing.id}: {existing.price} -> {price}")
                
            await self.session.commit()
            return existing

        # Create new
        new_listing = Listing(
            marketplace_id=mp.id,
            seller_id=seller.id,
            external_listing_id=parsed_data["external_listing_id"],
            url=parsed_data["url"],
            title=parsed_data["title"],
            description=parsed_data["description"],
            price=price or 0,
            registration_year=parsed_data.get("registration_year") or 2000,
            km_driven=parsed_data.get("km_driven") or 0,
            ownership=parsed_data.get("ownership") or 1,
            fuel=parsed_data.get("fuel"),
            transmission=parsed_data.get("transmission"),
            colour=parsed_data.get("colour"),
            registration_state=parsed_data.get("registration_state", "Unknown"),
            registration_city=parsed_data.get("registration_city", "Unknown"),
            first_seen=now,
            last_seen=now
        )
        self.session.add(new_listing)
        await self.session.flush()

        # Add images
        for i, img_url in enumerate(parsed_data.get("images", [])):
            img = Image(listing_id=new_listing.id, image_url=img_url, order=i)
            self.session.add(img)

        await self.session.commit()
        logger.info(f"Created new listing {new_listing.id} from {mp.name}")
        return new_listing
