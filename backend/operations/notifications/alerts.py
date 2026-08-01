from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, Any, List
from backend.database.config import engine
from backend.operations.notifications.manager import notification_manager, NotificationType

class AlertEngine:
    async def process_price_drops(self, listing_id: str, new_price: float, old_price: float):
        # Notify users who have saved this car in their favorites or saved searches
        # This is a conceptual implementation linking the DB.
        
        query = """
            SELECT user_id FROM user_favorites WHERE listing_id = :listing_id
        """
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"listing_id": listing_id})
            users = [row[0] for row in res.fetchall()]
            
        for user_id in users:
            await notification_manager.create_notification(
                user_id=str(user_id),
                title="Price Drop Alert",
                message=f"A vehicle in your favorites has dropped in price to ₹{new_price}",
                type=NotificationType.PRICE_DROP,
                link=f"/listings/{listing_id}"
            )
            
    async def process_new_match(self, user_id: str, search_name: str, listing_id: str):
        await notification_manager.create_notification(
            user_id=user_id,
            title="New Saved Search Match",
            message=f"A new vehicle matching '{search_name}' was just listed.",
            type=NotificationType.NEW_MATCH,
            link=f"/listings/{listing_id}"
        )

alert_engine = AlertEngine()
