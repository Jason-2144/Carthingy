FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We need the backend models for SQLAlchemy
COPY backend/ /app/backend/
COPY scraper/ /app/scraper/

# Command will be overridden by docker-compose for worker/beat
CMD ["celery", "-A", "scraper.queue.celery_app", "worker", "--loglevel=info", "-Q", "scrape_jobs,process_listings", "-c", "5"]
