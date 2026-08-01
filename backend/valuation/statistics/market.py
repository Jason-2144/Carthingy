from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine

class MarketIntelligenceService:
    async def get_fastest_selling_models(self) -> list:
        query = """
            SELECT c.make, c.model, AVG(l.ownership) as avg_ownership
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            WHERE l.status = 'SOLD'
            GROUP BY c.make, c.model
            ORDER BY AVG(l.ownership) ASC
            LIMIT 10;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query))
            return [dict(zip(res.keys(), row)) for row in res.fetchall()]

    async def get_price_trends(self) -> dict:
        query = """
            SELECT c.body_type, EXTRACT(MONTH FROM l.first_seen) as month, AVG(l.price) as avg_price
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            GROUP BY c.body_type, EXTRACT(MONTH FROM l.first_seen)
            ORDER BY month ASC;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query))
            data = [dict(zip(res.keys(), row)) for row in res.fetchall()]
        
        # Aggregate logic
        result = {}
        for row in data:
            bt = row['body_type']
            m = row['month']
            p = row['avg_price']
            if bt not in result:
                result[bt] = []
            result[bt].append({"month": m, "avg_price": float(p)})
        return result

    async def get_inventory_trends(self) -> list:
        query = """
            SELECT EXTRACT(DATE FROM first_seen) as date, COUNT(*) as count
            FROM listings
            GROUP BY EXTRACT(DATE FROM first_seen)
            ORDER BY date DESC
            LIMIT 30;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query))
            return [dict(zip(res.keys(), row)) for row in res.fetchall()]

market_intelligence_service = MarketIntelligenceService()
