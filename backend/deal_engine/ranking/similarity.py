from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine

class SimilarityEngine:
    async def find_similar(self, listing_id: str, limit: int = 20) -> list:
        # We find vehicles with same make, model, variant
        # Then rank them by year and km_driven proximity
        
        query = """
            WITH target AS (
                SELECT l.price, l.registration_year, l.km_driven, l.fuel, l.transmission, l.ownership,
                       l.registration_city, c.make, c.model, c.variant, l.car_id
                FROM listings l
                JOIN cars c ON l.car_id = c.id
                WHERE l.id = :listing_id
            )
            SELECT 
                l.id, l.title, l.price, l.registration_year, l.km_driven, l.registration_city,
                100 - (
                    (ABS(l.registration_year - t.registration_year) * 5) + 
                    (LEAST(ABS(l.km_driven - t.km_driven) / GREATEST(t.km_driven, 1), 1) * 30) +
                    (CASE WHEN l.fuel != t.fuel THEN 100 ELSE 0 END) +
                    (CASE WHEN l.transmission != t.transmission THEN 100 ELSE 0 END)
                ) as similarity_score
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            CROSS JOIN target t
            WHERE l.id != :listing_id
              AND l.status = 'ACTIVE'
              AND c.make = t.make
              AND c.model = t.model
            ORDER BY similarity_score DESC
            LIMIT :limit;
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"listing_id": listing_id, "limit": limit})
            similar = []
            for row in res.fetchall():
                sim_score = max(0, min(100, float(row.similarity_score)))
                if sim_score > 0:
                    similar.append({
                        "id": str(row.id),
                        "title": row.title,
                        "price": float(row.price),
                        "registration_year": row.registration_year,
                        "km_driven": row.km_driven,
                        "registration_city": row.registration_city,
                        "similarity_percentage": round(sim_score, 1)
                    })
            return similar

similarity_engine = SimilarityEngine()
