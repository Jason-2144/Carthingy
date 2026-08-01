from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine
from typing import List, Dict, Any

class CompareEngine:
    async def compare_vehicles(self, listing_ids: List[str]) -> Dict[str, Any]:
        if not listing_ids or len(listing_ids) > 10:
            raise ValueError("Provide between 1 and 10 listing IDs to compare")
            
        # Format for SQL IN clause safely
        placeholders = ", ".join([f":id{i}" for i in range(len(listing_ids))])
        params = {f"id{i}": lid for i, lid in enumerate(listing_ids)}
        
        query = f"""
            SELECT l.id, l.title, l.price, l.registration_year, l.km_driven, l.ownership,
                   l.fuel, l.transmission, l.colour, l.registration_city,
                   c.make, c.model, c.variant, c.body_type
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            WHERE l.id IN ({placeholders})
        """
        
        async with engine.connect() as conn:
            res = await conn.execute(text(query), params)
            vehicles = [dict(zip(res.keys(), row)) for row in res.fetchall()]
            
        # Generate summary
        if not vehicles:
            return {"vehicles": [], "summary": {}}
            
        summary = {
            "cheapest": min(vehicles, key=lambda x: float(x["price"]))["title"] if all(x["price"] is not None for x in vehicles) else None,
            "lowest_mileage": min(vehicles, key=lambda x: int(x["km_driven"]))["title"] if all(x["km_driven"] is not None for x in vehicles) else None,
            "newest": max(vehicles, key=lambda x: int(x["registration_year"]))["title"] if all(x["registration_year"] is not None for x in vehicles) else None,
        }
        
        return {
            "vehicles": vehicles,
            "summary": summary
        }

compare_engine = CompareEngine()
