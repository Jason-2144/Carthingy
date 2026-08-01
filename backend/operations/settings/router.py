from fastapi import APIRouter
from pydantic import BaseModel
import redis.asyncio as redis
from backend.operations.config import ops_settings

router = APIRouter(prefix="/settings", tags=["Operations Settings"])
r = redis.from_url(ops_settings.REDIS_URL, decode_responses=True)

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.get("/")
async def get_settings():
    settings = await r.hgetall("system_settings")
    return settings

@router.post("/")
async def update_setting(update: SettingUpdate):
    await r.hset("system_settings", update.key, update.value)
    return {"status": "success"}
