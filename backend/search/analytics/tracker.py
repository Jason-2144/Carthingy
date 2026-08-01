import redis.asyncio as redis
import json
import time
from backend.search.config import search_settings
from typing import Dict, Any, List

class SearchAnalyticsTracker:
    def __init__(self):
        self.redis = redis.from_url(search_settings.REDIS_URL, decode_responses=True)
        self.prefix = "search_analytics:"

    async def log_search(self, user_id: str, query: str, filters: Dict[str, Any], results_count: int, latency_ms: float):
        timestamp = int(time.time())
        log_entry = {
            "user_id": user_id or "anonymous",
            "query": query,
            "filters": filters,
            "results_count": results_count,
            "latency_ms": latency_ms,
            "timestamp": timestamp
        }
        
        pipe = self.redis.pipeline()
        # Log entry for recent searches history
        await pipe.lpush(f"{self.prefix}recent_logs", json.dumps(log_entry))
        await pipe.ltrim(f"{self.prefix}recent_logs", 0, 9999) # Keep last 10000
        
        # Track query popularity if there's a text query
        if query:
            normalized_query = query.lower().strip()
            await pipe.zincrby(f"{self.prefix}popular_queries", 1, normalized_query)
            
        # Track no-result searches
        if results_count == 0:
            if query:
                await pipe.zincrby(f"{self.prefix}zero_results", 1, query.lower().strip())
                
        # Track brand/model popularity from filters
        if filters.get("make"):
            makes = filters["make"]
            if isinstance(makes, str):
                makes = [makes]
            for make in makes:
                await pipe.zincrby(f"{self.prefix}popular_makes", 1, make)
                
        if filters.get("registration_city"):
            cities = filters["registration_city"]
            if isinstance(cities, str):
                cities = [cities]
            for city in cities:
                await pipe.zincrby(f"{self.prefix}popular_cities", 1, city)
                
        await pipe.execute()

    async def get_popular_queries(self, limit: int = 10) -> List[str]:
        return await self.redis.zrevrange(f"{self.prefix}popular_queries", 0, limit - 1)
        
    async def get_popular_makes(self, limit: int = 10) -> List[str]:
        return await self.redis.zrevrange(f"{self.prefix}popular_makes", 0, limit - 1)
        
    async def get_popular_cities(self, limit: int = 10) -> List[str]:
        return await self.redis.zrevrange(f"{self.prefix}popular_cities", 0, limit - 1)

search_analytics = SearchAnalyticsTracker()
