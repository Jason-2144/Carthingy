from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from pydantic import BaseModel
from backend.valuation.prediction.service import prediction_service
from backend.valuation.statistics.market import market_intelligence_service
from backend.valuation.jobs.tasks import retrain_model_task, generate_market_report_task

router = APIRouter(prefix="/valuation", tags=["Valuation & Market Intelligence"])

class VehicleData(BaseModel):
    make: str
    model: str
    variant: str
    registration_year: int
    km_driven: int
    fuel: str
    transmission: str
    ownership: int
    registration_city: str
    registration_state: str
    body_type: str

@router.post("/estimate")
async def estimate_vehicle_value(data: VehicleData):
    try:
        result = prediction_service.predict(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-stats/fastest-selling")
async def get_fastest_selling():
    try:
        return await market_intelligence_service.get_fastest_selling_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-stats/price-trends")
async def get_price_trends():
    try:
        return await market_intelligence_service.get_price_trends()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jobs/retrain")
async def trigger_retrain():
    # In production, this might just delay the celery task
    retrain_model_task.delay()
    return {"status": "Retraining job submitted to queue"}

@router.post("/jobs/report")
async def trigger_report():
    generate_market_report_task.delay()
    return {"status": "Report generation job submitted to queue"}
