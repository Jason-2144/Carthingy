from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from backend.ai.assistant.copilot import copilot
from backend.ai.reports.generator import ai_report_generator

router = APIRouter(prefix="/ai", tags=["AI Copilot & Reports"])

class ChatRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class ReportRequest(BaseModel):
    city: str
    make: str
    model_name: str

@router.post("/chat")
async def chat_with_copilot(request: ChatRequest):
    try:
        response = await copilot.chat(request.query, request.context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/report")
async def generate_market_report(request: ReportRequest):
    try:
        # Fetch some recent data from search engine as context
        from backend.search.engine import search_engine
        results = await search_engine.search_listings(
            filters={"make": request.make, "model": request.model_name, "registration_city": request.city},
            limit=50
        )
        report = await ai_report_generator.generate_market_report(
            city=request.city,
            make=request.make,
            model_name=request.model_name,
            data=results.get("hits", [])
        )
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
