import psutil
import redis.asyncio as redis
from backend.operations.config import ops_settings
from backend.database.config import engine
from sqlalchemy import text

class SystemMonitor:
    def __init__(self):
        self.redis = redis.from_url(ops_settings.REDIS_URL, decode_responses=True)

    async def get_system_health(self) -> dict:
        health = {
            "status": "healthy",
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "components": {}
        }

        # Check Postgres
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            health["components"]["database"] = "up"
        except Exception as e:
            health["components"]["database"] = "down"
            health["status"] = "degraded"

        # Check Redis
        try:
            await self.redis.ping()
            health["components"]["redis"] = "up"
        except Exception as e:
            health["components"]["redis"] = "down"
            health["status"] = "degraded"

        return health
        
system_monitor = SystemMonitor()
