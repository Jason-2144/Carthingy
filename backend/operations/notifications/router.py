from fastapi import APIRouter
from backend.operations.notifications.manager import notification_manager
from typing import Optional

router = APIRouter(prefix="/notifications", tags=["Operations Notifications"])

@router.get("/{user_id}")
async def get_notifications(user_id: str, include_read: bool = True):
    return await notification_manager.get_user_notifications(user_id, include_read)

@router.put("/{user_id}/{notif_id}/read")
async def mark_read(user_id: str, notif_id: str):
    await notification_manager.mark_as_read(user_id, notif_id)
    return {"status": "success"}
    
@router.put("/{user_id}/read-all")
async def mark_all_read(user_id: str):
    await notification_manager.mark_all_as_read(user_id)
    return {"status": "success"}
