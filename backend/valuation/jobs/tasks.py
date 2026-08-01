from celery import Celery
import asyncio
from backend.valuation.training.pipeline import TrainingPipeline
from backend.valuation.reports.generator import report_generator
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("valuation_tasks", broker=redis_url)

@celery_app.task
def retrain_model_task():
    pipeline = TrainingPipeline()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(pipeline.run())
    return result

@celery_app.task
def generate_market_report_task():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(report_generator.generate_monthly_report())
    return result

# celery -A backend.valuation.jobs.tasks worker -l info
