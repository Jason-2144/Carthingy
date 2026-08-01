from celery import Celery
import asyncio
import os
from backend.search.indexes.client import search_client
from backend.search.config import search_settings
from backend.database.config import engine
from sqlalchemy import text

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
search_tasks_app = Celery("search_tasks", broker=redis_url)

@search_tasks_app.task
def sync_index_task(batch_size: int = 1000):
    """
    Syncs the postgres database to Meilisearch index in batches.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_sync(batch_size))
    return {"status": "Index synchronized"}

async def _run_sync(batch_size: int):
    search_client.setup_listings_index()
    
    query = """
        SELECT l.id, l.title, l.price, l.registration_year, l.km_driven, l.ownership,
               l.fuel, l.transmission, l.colour, l.registration_city, l.registration_state,
               c.make, c.model, c.variant, c.body_type,
               extract(epoch from l.first_seen) as first_seen
        FROM listings l
        JOIN cars c ON l.car_id = c.id
        WHERE l.status = 'ACTIVE'
        LIMIT :limit OFFSET :offset
    """
    
    offset = 0
    while True:
        async with engine.connect() as conn:
            res = await conn.execute(text(query), {"limit": batch_size, "offset": offset})
            rows = res.fetchall()
            
        if not rows:
            break
            
        documents = []
        for row in rows:
            doc = dict(zip(res.keys(), row))
            # Convert UUID to string for Meilisearch
            doc["id"] = str(doc["id"])
            doc["price"] = float(doc["price"]) if doc["price"] is not None else 0.0
            documents.append(doc)
            
        search_client.add_documents(search_settings.LISTINGS_INDEX, documents)
        offset += batch_size
