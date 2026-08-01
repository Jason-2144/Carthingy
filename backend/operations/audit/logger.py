import redis.asyncio as redis
import json
import time
import uuid
from typing import Optional, Dict, Any
from backend.operations.config import ops_settings

class AuditLogger:
    def __init__(self):
        self.redis = redis.from_url(ops_settings.REDIS_URL, decode_responses=True)
        self.stream_name = "audit_stream"
        
    async def log_event(
        self, 
        event_type: str, 
        user_id: str, 
        action: str, 
        resource_id: Optional[str] = None, 
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "resource_id": resource_id or "",
            "details": json.dumps(details) if details else "{}",
            "ip_address": ip_address or "",
            "user_agent": user_agent or ""
        }
        
        # Add to Redis Stream
        await self.redis.xadd(self.stream_name, event)
        
    async def get_recent_events(self, count: int = 100):
        # Read from end of stream backwards
        # xrevrange is efficient for recent events
        messages = await self.redis.xrevrange(self.stream_name, max="+", min="-", count=count)
        events = []
        for msg_id, msg_data in messages:
            msg_data['stream_id'] = msg_id
            events.append(msg_data)
        return events

audit_logger = AuditLogger()
