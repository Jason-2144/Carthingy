from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import datetime

from backend.deal_engine.engine import deal_engine
from backend.deal_engine.analytics.insights import dealer_insights_engine
from backend.deal_engine.jobs.tasks import recalculate_deal_scores_task, generate_insights_report_task
from backend.valuation.prediction.service import prediction_service

router = APIRouter(prefix="/deal-intelligence", tags=["Deal Intelligence"])

class ListingAnalysisRequest(BaseModel):
    id: Optional[str] = None
    price: float
    make: str
    model: str
    variant: str
    registration_year: int
    km_driven: int
    ownership: int
    registration_city: str
    registration_state: str
    first_seen: Optional[datetime.datetime] = None
    price_drop_count: int = 0
    # Additional valuation fields
    fuel: str = "Petrol"
    transmission: str = "Manual"
    body_type: str = "Sedan"

@router.post("/analyze")
async def analyze_listing(request: ListingAnalysisRequest):
    data = request.model_dump()
    if not data.get('first_seen'):
        data['first_seen'] = datetime.datetime.now()
        
    try:
        # Get valuation first
        val_result = prediction_service.predict(data)
        estimated_value = val_result.get('estimated_market_value', 0)
        
        # Run Deal Engine
        report = await deal_engine.analyze_listing(data, estimated_value)
        report['valuation'] = val_result
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{listing_id}")
async def similar_listings(listing_id: str, limit: int = 20):
    try:
        return await deal_engine.get_similar_vehicles(listing_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/hidden-gems")
async def hidden_gems(limit: int = 10):
    try:
        return await dealer_insights_engine.get_hidden_gems(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/fast-flips")
async def fast_flips(limit: int = 10):
    try:
        return await dealer_insights_engine.get_fast_flip_opportunities(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jobs/recalculate")
async def trigger_recalculate():
    recalculate_deal_scores_task.delay()
    return {"status": "Recalculation job submitted"}
