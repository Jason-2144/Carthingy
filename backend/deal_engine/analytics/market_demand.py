from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.database.config import engine

class MarketDemandEngine:
    async def get_demand_metrics(self, make: str, model: str, city: str) -> dict:
        """
        Calculates demand and supply metrics for a specific vehicle in a region.
        """
        query = """
            SELECT 
                COUNT(*) as active_listings,
                AVG(EXTRACT(DAY FROM (NOW() - first_seen))) as avg_days_on_market,
                SUM(CASE WHEN status = 'SOLD' THEN 1 ELSE 0 END) as sold_last_30_days
            FROM listings l
            JOIN cars c ON l.car_id = c.id
            WHERE c.make = :make 
              AND c.model = :model 
              AND l.registration_city = :city
              AND l.first_seen >= NOW() - INTERVAL '30 days';
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"make": make, "model": model, "city": city})
            row = res.fetchone()
            
            if not row or row.active_listings == 0:
                return {
                    "demand_score": 50,
                    "supply_score": 50,
                    "inventory_pressure": "Balanced",
                    "popularity_index": 50,
                    "average_time_to_sell": 30,
                    "competition_score": 50,
                    "seasonality_factor": 1.0
                }
                
            active = row.active_listings
            sold = row.sold_last_30_days or 0
            avg_dom = float(row.avg_days_on_market or 30)
            
            # Simple heuristic formulas
            supply_score = min(100, active * 2) 
            demand_score = min(100, sold * 5)
            
            if active > sold * 2:
                pressure = "High Supply"
            elif sold > active:
                pressure = "High Demand"
            else:
                pressure = "Balanced"
                
            pop_index = min(100, demand_score * 0.7 + (100 - avg_dom) * 0.3)
            comp_score = supply_score # more supply = more competition for sellers
            
            return {
                "demand_score": round(demand_score, 1),
                "supply_score": round(supply_score, 1),
                "inventory_pressure": pressure,
                "popularity_index": round(pop_index, 1),
                "average_time_to_sell": round(avg_dom, 1),
                "competition_score": round(comp_score, 1),
                "seasonality_factor": 1.05 # Mocked for now
            }

market_demand_engine = MarketDemandEngine()
