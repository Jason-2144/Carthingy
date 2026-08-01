from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine

class DealerInsightsEngine:
    async def get_fast_flip_opportunities(self, limit: int = 10) -> list:
        # Listings priced significantly below market for high demand cars
        # This requires joining a pre-calculated deal score or estimating on the fly.
        # Since deal_score is not stored natively yet, we mock a heuristic query:
        # e.g., High demand models that are recently posted and have below average price.
        query = """
            SELECT l.id, l.title, l.price, l.first_seen
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            WHERE l.status = 'ACTIVE'
              AND l.first_seen >= NOW() - INTERVAL '3 days'
            ORDER BY l.price ASC
            LIMIT :limit;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"limit": limit})
            return [dict(zip(res.keys(), row)) for row in res.fetchall()]

    async def get_hidden_gems(self, limit: int = 10) -> list:
        # Old listings with multiple price drops, might be negotiable
        query = """
            SELECT l.id, l.title, l.price, l.first_seen,
                   (SELECT COUNT(*) FROM history h WHERE h.listing_id = l.id) as price_drops
            FROM listings l
            WHERE l.status = 'ACTIVE'
              AND l.first_seen <= NOW() - INTERVAL '60 days'
            ORDER BY price_drops DESC, l.first_seen ASC
            LIMIT :limit;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"limit": limit})
            return [dict(zip(res.keys(), row)) for row in res.fetchall()]

dealer_insights_engine = DealerInsightsEngine()
