from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine
from typing import List, Dict, Any

class RecommendationEngine:
    async def get_trending(self, limit: int = 10) -> List[Dict[str, Any]]:
        # Fetch highly viewed / recently updated listings
        query = """
            SELECT l.id, l.title, l.price, l.registration_city, c.make, c.model, l.first_seen
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            WHERE l.status = 'ACTIVE'
            ORDER BY l.first_seen DESC
            LIMIT :limit
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"limit": limit})
            return [dict(zip(res.keys(), row)) for row in res.fetchall()]

recommendation_engine = RecommendationEngine()
