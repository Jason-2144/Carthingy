from celery.schedules import crontab
from scraper.queue.celery_app import celery_app

# Define recurring scraping jobs
celery_app.conf.beat_schedule = {
    "scrape-olx-daily": {
        "task": "scraper.workers.tasks.scrape_marketplace",
        "schedule": crontab(hour="*/6", minute=0), # Every 6 hours
        "args": ("olx", "cars", {}),
    },
    "scrape-fb-daily": {
        "task": "scraper.workers.tasks.scrape_marketplace",
        "schedule": crontab(hour="*/6", minute=30),
        "args": ("facebook", "cars", {}),
    }
}
