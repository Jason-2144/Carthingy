from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from backend.models.listings import Listing
from backend.models.enums import ListingStatus
from backend.models.history import Image, PriceHistory
from backend.models.sellers import Seller
from backend.models.marketplaces import Marketplace
from backend.models.cars import Car

class ListingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_listings(
        self,
        brand: str | None = None,
        model: str | None = None,
        variant: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
        min_km: int | None = None,
        max_km: int | None = None,
        fuel: str | None = None,
        transmission: str | None = None,
        body_type: str | None = None,
        state: str | None = None,
        city: str | None = None,
        ownership: int | None = None,
        marketplace_id: str | None = None,
        seller_id: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[int, list[Listing]]:
        """
        High performance search leveraging indexes and pre-loading related entities.
        Returns a tuple of (total_count, listings)
        """
        base_query = select(Listing).filter(
            Listing.status == ListingStatus.ACTIVE, 
            Listing.is_deleted == False
        )
        
        # Apply filters
        filters = []
        if min_price is not None: filters.append(Listing.price >= min_price)
        if max_price is not None: filters.append(Listing.price <= max_price)
        if min_year is not None: filters.append(Listing.registration_year >= min_year)
        if max_year is not None: filters.append(Listing.registration_year <= max_year)
        if min_km is not None: filters.append(Listing.km_driven >= min_km)
        if max_km is not None: filters.append(Listing.km_driven <= max_km)
        if fuel: filters.append(func.lower(Listing.fuel) == fuel.lower())
        if transmission: filters.append(func.lower(Listing.transmission) == transmission.lower())
        if state: filters.append(func.lower(Listing.registration_state) == state.lower())
        if city: filters.append(func.lower(Listing.registration_city) == city.lower())
        if ownership is not None: filters.append(Listing.ownership == ownership)
        if marketplace_id: filters.append(Listing.marketplace_id == marketplace_id)
        if seller_id: filters.append(Listing.seller_id == seller_id)
        
        # Join with Car for deep metadata filtering
        if brand or model or variant or body_type:
            base_query = base_query.join(Car)
            if brand: filters.append(func.lower(Car.make) == brand.lower())
            if model: filters.append(func.lower(Car.model) == model.lower())
            if variant: filters.append(func.lower(Car.variant).contains(variant.lower()))
            if body_type: filters.append(func.lower(Car.body_type) == body_type.lower())

        if filters:
            base_query = base_query.filter(and_(*filters))

        # Count query
        count_query = select(func.count()).select_from(base_query.subquery())
        total = (await self.session.execute(count_query)).scalar()

        # Data query with relationships
        data_query = base_query.options(
            selectinload(Listing.marketplace),
            selectinload(Listing.seller),
            selectinload(Listing.images),
            selectinload(Listing.price_history)
        ).order_by(Listing.first_seen.desc()).offset(offset).limit(limit)

        result = await self.session.execute(data_query)
        listings = list(result.scalars().all())

        return total, listings

    async def get_by_id(self, listing_id: str) -> Listing | None:
        query = select(Listing).filter(Listing.id == listing_id).options(
            selectinload(Listing.marketplace),
            selectinload(Listing.seller),
            selectinload(Listing.images),
            selectinload(Listing.price_history)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
