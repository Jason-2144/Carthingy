from celery import Celery
from scraper.utils.config import settings

celery_app = Celery(
    "scraper",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["scraper.workers.tasks", "scraper.scheduler.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    task_routes={
        "scraper.workers.tasks.scrape_marketplace": {"queue": "scrape_jobs"},
        "scraper.workers.tasks.process_listing": {"queue": "process_listings"},
    }
)
