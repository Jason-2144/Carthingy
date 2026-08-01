import json
import uuid
import time
from backend.search.config import search_settings
from backend.search.analytics.tracker import search_analytics
from typing import Dict, Any, List

class SavedSearchManager:
    def __init__(self):
        self.redis = search_analytics.redis
        self.prefix = "saved_searches:"

    async def save_search(self, user_id: str, name: str, query: str, filters: Dict[str, Any]) -> str:
        search_id = str(uuid.uuid4())
        payload = {
            "id": search_id,
            "name": name,
            "query": query,
            "filters": filters,
            "created_at": int(time.time())
        }
        await self.redis.hset(f"{self.prefix}{user_id}", search_id, json.dumps(payload))
        return search_id

    async def get_saved_searches(self, user_id: str) -> List[Dict[str, Any]]:
        raw_data = await self.redis.hgetall(f"{self.prefix}{user_id}")
        results = []
        for v in raw_data.values():
            results.append(json.loads(v))
        return sorted(results, key=lambda x: x["created_at"], reverse=True)

    async def delete_saved_search(self, user_id: str, search_id: str):
        await self.redis.hdel(f"{self.prefix}{user_id}", search_id)

saved_search_manager = SavedSearchManager()
