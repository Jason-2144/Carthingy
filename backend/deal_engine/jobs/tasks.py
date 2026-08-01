from celery import Celery
import asyncio
import os
from backend.deal_engine.analytics.insights import dealer_insights_engine

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
deal_tasks_app = Celery("deal_tasks", broker=redis_url)

@deal_tasks_app.task
def recalculate_deal_scores_task():
    # In a full production system, this would iterate over active listings,
    # run them through the DealScoreCalculator, and update a deal_scores table.
    return {"status": "Scores recalculated (mocked)"}

@deal_tasks_app.task
def generate_insights_report_task():
    loop = asyncio.get_event_loop()
    gems = loop.run_until_complete(dealer_insights_engine.get_hidden_gems())
    flips = loop.run_until_complete(dealer_insights_engine.get_fast_flip_opportunities())
    
    # Store or email report
    return {
        "hidden_gems_found": len(gems),
        "fast_flips_found": len(flips),
        "status": "Report Generated"
    }
