from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from backend.search.engine import search_engine

router = APIRouter(prefix="/mobile/v1", tags=["Mobile API"])

@router.get("/listings/search")
async def mobile_search(
    query: str = "",
    client_version: Optional[str] = Header(None),
    device_os: Optional[str] = Header(None)
):
    """
    Stable Mobile API endpoint.
    Handles legacy clients and specific mobile data shapes.
    """
    # Enforce minimum app version
    if client_version and client_version < "1.0.0":
        raise HTTPException(status_code=426, detail="Please update your app to continue using CarScope AI.")
        
    try:
        results = await search_engine.search_listings(query=query)
        # We can format the payload specifically for mobile to reduce payload size
        mobile_hits = []
        for hit in results.get("hits", []):
            mobile_hits.append({
                "id": hit.get("id"),
                "title": hit.get("title"),
                "price": hit.get("price"),
                "image": hit.get("images", [""])[0] if hit.get("images") else None,
                "deal_score": hit.get("deal_score")
            })
        return {"data": mobile_hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
