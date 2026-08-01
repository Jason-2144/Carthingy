import redis.asyncio as redis
import json
import uuid
import time
from backend.operations.config import ops_settings

class SessionManager:
    def __init__(self):
        self.redis = redis.from_url(ops_settings.REDIS_URL, decode_responses=True)

    async def create_session(self, user_id: str, user_agent: str, ip_address: str) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "user_agent": user_agent,
            "ip_address": ip_address,
            "created_at": int(time.time()),
            "last_active": int(time.time())
        }
        
        pipe = self.redis.pipeline()
        pipe.hset(f"user_sessions:{user_id}", session_id, json.dumps(session_data))
        pipe.setex(f"session:{session_id}", ops_settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, user_id)
        # Store login history
        pipe.lpush(f"login_history:{user_id}", json.dumps(session_data))
        pipe.ltrim(f"login_history:{user_id}", 0, 99) # Keep last 100 logins
        await pipe.execute()
        
        return session_id
        
    async def get_active_sessions(self, user_id: str) -> list:
        sessions = await self.redis.hgetall(f"user_sessions:{user_id}")
        return [json.loads(s) for s in sessions.values()]
        
    async def logout_session(self, user_id: str, session_id: str):
        pipe = self.redis.pipeline()
        pipe.hdel(f"user_sessions:{user_id}", session_id)
        pipe.delete(f"session:{session_id}")
        await pipe.execute()
        
    async def logout_all(self, user_id: str):
        sessions = await self.get_active_sessions(user_id)
        pipe = self.redis.pipeline()
        for s in sessions:
            pipe.delete(f"session:{s['session_id']}")
        pipe.delete(f"user_sessions:{user_id}")
        await pipe.execute()
        
    async def record_failed_login(self, email: str) -> bool:
        """Returns True if locked out"""
        key = f"failed_logins:{email}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, ops_settings.LOCKOUT_MINUTES * 60)
            
        if count >= ops_settings.MAX_LOGIN_ATTEMPTS:
            await self.redis.setex(f"lockout:{email}", ops_settings.LOCKOUT_MINUTES * 60, "locked")
            return True
        return False
        
    async def is_locked_out(self, email: str) -> bool:
        return await self.redis.exists(f"lockout:{email}") > 0
        
    async def clear_failed_logins(self, email: str):
        await self.redis.delete(f"failed_logins:{email}")
        await self.redis.delete(f"lockout:{email}")

session_manager = SessionManager()
