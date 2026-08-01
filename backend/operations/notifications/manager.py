import redis.asyncio as redis
import json
import time
import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from backend.operations.config import ops_settings

class NotificationType(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PRICE_DROP = "PRICE_DROP"
    NEW_MATCH = "NEW_MATCH"

class NotificationManager:
    def __init__(self):
        self.redis = redis.from_url(ops_settings.REDIS_URL, decode_responses=True)
        
    async def create_notification(
        self, 
        user_id: str, 
        title: str, 
        message: str, 
        type: NotificationType = NotificationType.INFO,
        link: Optional[str] = None
    ):
        notif_id = str(uuid.uuid4())
        notification = {
            "id": notif_id,
            "title": title,
            "message": message,
            "type": type,
            "link": link or "",
            "read": False,
            "created_at": int(time.time())
        }
        
        pipe = self.redis.pipeline()
        pipe.hset(f"notifications:{user_id}", notif_id, json.dumps(notification))
        # Keep track of unread count
        pipe.incr(f"unread_notifications:{user_id}")
        await pipe.execute()
        return notif_id
        
    async def get_user_notifications(self, user_id: str, include_read: bool = True) -> List[Dict[str, Any]]:
        raw_data = await self.redis.hgetall(f"notifications:{user_id}")
        notifications = [json.loads(v) for v in raw_data.values()]
        
        if not include_read:
            notifications = [n for n in notifications if not n["read"]]
            
        return sorted(notifications, key=lambda x: x["created_at"], reverse=True)
        
    async def mark_as_read(self, user_id: str, notif_id: str):
        raw_notif = await self.redis.hget(f"notifications:{user_id}", notif_id)
        if raw_notif:
            notif = json.loads(raw_notif)
            if not notif["read"]:
                notif["read"] = True
                pipe = self.redis.pipeline()
                pipe.hset(f"notifications:{user_id}", notif_id, json.dumps(notif))
                pipe.decr(f"unread_notifications:{user_id}")
                await pipe.execute()
                
    async def mark_all_as_read(self, user_id: str):
        notifications = await self.get_user_notifications(user_id, include_read=False)
        if not notifications:
            return
            
        pipe = self.redis.pipeline()
        for notif in notifications:
            notif["read"] = True
            pipe.hset(f"notifications:{user_id}", notif["id"], json.dumps(notif))
        pipe.set(f"unread_notifications:{user_id}", 0)
        await pipe.execute()

notification_manager = NotificationManager()
