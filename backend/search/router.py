from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.search.engine import search_engine
from backend.search.analytics.tracker import search_analytics
from backend.search.analytics.saved_searches import saved_search_manager
from backend.search.compare import compare_engine
from backend.search.recommendations import recommendation_engine
from backend.search.jobs.tasks import sync_index_task

router = APIRouter(prefix="/search", tags=["Search Engine"])

class SearchRequest(BaseModel):
    query: str = ""
    filters: Dict[str, Any] = {}
    sort_by: Optional[str] = None
    page: int = 1
    limit: int = 20
    user_id: Optional[str] = None

class SavedSearchRequest(BaseModel):
    user_id: str
    name: str
    query: str
    filters: Dict[str, Any]

class CompareRequest(BaseModel):
    listing_ids: List[str]

@router.post("/")
async def search(request: SearchRequest):
    try:
        results = await search_engine.search_listings(
            query=request.query,
            filters=request.filters,
            sort_by=request.sort_by,
            page=request.page,
            limit=request.limit,
            user_id=request.user_id
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete")
async def autocomplete(query: str = ""):
    try:
        suggestions = await search_engine.get_autocomplete_suggestions(query)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/saved")
async def save_search(request: SavedSearchRequest):
    try:
        search_id = await saved_search_manager.save_search(
            request.user_id, request.name, request.query, request.filters
        )
        return {"status": "success", "search_id": search_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/saved/{user_id}")
async def get_saved_searches(user_id: str):
    try:
        return await saved_search_manager.get_saved_searches(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/saved/{user_id}/{search_id}")
async def delete_saved_search(user_id: str, search_id: str):
    try:
        await saved_search_manager.delete_saved_search(user_id, search_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_vehicles(request: CompareRequest):
    try:
        return await compare_engine.compare_vehicles(request.listing_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/trending")
async def trending(limit: int = 10):
    try:
        return await recommendation_engine.get_trending(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/popular-queries")
async def popular_queries(limit: int = 10):
    try:
        queries = await search_analytics.get_popular_queries(limit)
        return {"popular_queries": queries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/jobs/sync")
async def trigger_sync():
    sync_index_task.delay()
    return {"status": "Sync job submitted"}
