from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database.config import get_db_session
from backend.models.listings import Listing
from pydantic import BaseModel

router = APIRouter()

class AnalyticsOverview(BaseModel):
    total_active_listings: int
    average_price: float
    average_mileage: float

@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(db: AsyncSession = Depends(get_db_session)):
    # In a real high-scale system, these values would be pre-computed in AnalyticsMetric
    # For real-time demonstration, we use aggregate functions
    
    result = await db.execute(
        select(
            func.count(Listing.id).label("total_listings"),
            func.avg(Listing.price).label("avg_price"),
            func.avg(Listing.km_driven).label("avg_mileage")
        ).filter(Listing.status == 'active', Listing.is_deleted == False)
    )
    row = result.first()
    
    return AnalyticsOverview(
        total_active_listings=row.total_listings or 0,
        average_price=float(row.avg_price) if row.avg_price else 0.0,
        average_mileage=float(row.avg_mileage) if row.avg_mileage else 0.0
    )
