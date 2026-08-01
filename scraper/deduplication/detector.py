from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.listings import Listing
from fuzzywuzzy import fuzz # Requires fuzzywuzzy, will add to requirements

class DeduplicationEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_existing(self, marketplace_id: str, external_listing_id: str) -> Listing | None:
        """Exact match based on marketplace ID and their internal ID"""
        query = select(Listing).filter(
            Listing.marketplace_id == marketplace_id,
            Listing.external_listing_id == external_listing_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def detect_cross_platform_duplicate(self, parsed_data: dict) -> Listing | None:
        """
        Fuzzy matching to detect if the same car is posted on multiple platforms.
        This is a complex problem in production. Here we use a heuristic score.
        """
        # Search for active listings in the same city with same year and similar price
        if not parsed_data.get("price") or not parsed_data.get("registration_year"):
            return None

        price_margin = parsed_data["price"] * 0.05 # 5% price diff max
        min_price = parsed_data["price"] - price_margin
        max_price = parsed_data["price"] + price_margin

        query = select(Listing).filter(
            Listing.registration_year == parsed_data["registration_year"],
            Listing.price >= min_price,
            Listing.price <= max_price,
            # We would usually filter by city/state here as well
        )
        
        result = await self.session.execute(query)
        candidates = result.scalars().all()

        for candidate in candidates:
            # Check title similarity
            title_score = fuzz.token_sort_ratio(candidate.title, parsed_data["title"])
            if title_score > 85:
                # Check mileage (within 500km)
                if candidate.km_driven and parsed_data.get("km_driven"):
                    if abs(candidate.km_driven - parsed_data["km_driven"]) < 500:
                        return candidate # High confidence duplicate
        
        return None
