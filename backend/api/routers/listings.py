from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.config import get_db_session
from backend.repositories.listing_repo import ListingRepository
from backend.schemas.listing import ListingResponse, PaginatedListingsResponse
from backend.dependencies.auth import get_current_user

router = APIRouter()

def get_listing_repo(db: AsyncSession = Depends(get_db_session)) -> ListingRepository:
    return ListingRepository(db)

@router.get("/search", response_model=PaginatedListingsResponse)
async def search_listings(
    brand: str | None = Query(None, description="Car Make/Brand"),
    model: str | None = Query(None, description="Car Model"),
    variant: str | None = Query(None, description="Car Variant"),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    min_year: int | None = Query(None),
    max_year: int | None = Query(None),
    min_km: int | None = Query(None),
    max_km: int | None = Query(None),
    fuel: str | None = Query(None),
    transmission: str | None = Query(None),
    body_type: str | None = Query(None),
    state: str | None = Query(None),
    city: str | None = Query(None),
    ownership: int | None = Query(None),
    marketplace_id: str | None = Query(None),
    seller_id: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    repo: ListingRepository = Depends(get_listing_repo)
):
    offset = (page - 1) * size
    total, listings = await repo.search_listings(
        brand=brand, model=model, variant=variant,
        min_price=min_price, max_price=max_price,
        min_year=min_year, max_year=max_year,
        min_km=min_km, max_km=max_km,
        fuel=fuel, transmission=transmission, body_type=body_type,
        state=state, city=city, ownership=ownership,
        marketplace_id=marketplace_id, seller_id=seller_id,
        limit=size, offset=offset
    )
    
    return PaginatedListingsResponse(
        total=total,
        items=listings,
        page=page,
        size=size
    )

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: str, repo: ListingRepository = Depends(get_listing_repo)):
    listing = await repo.get_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing
