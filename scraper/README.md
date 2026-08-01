# CarScope AI - Scraper Engine

## Architecture

The scraping engine is a distributed, multi-worker system designed to continuously extract and process used car listings from multiple marketplaces (e.g., OLX, Facebook).

### Component Flow

1. **Scheduler (Celery Beat)**: Periodically triggers marketplace search jobs.
2. **Queue (Redis)**: Buffers jobs to prevent overloading workers or the database. Handles retries and prioritization.
3. **Workers (Celery)**: Stateless nodes running Playwright browsers to execute jobs.
4. **Marketplace Connectors**: Abstract interfaces isolating the logic of interacting with specific websites (navigation, extraction, pagination).
5. **Parsers & Normalizers**: Transforms messy HTML data into clean, structured dictionaries, normalizing prices, dates, mileage, etc.
6. **Deduplication Engine**: Uses fuzzy logic and direct matching to prevent storing the same car multiple times.
7. **Database Repository**: Handles UPSERT operations and logs Price History if a listing's price changes.

## Adding a New Marketplace

1. Create a new folder in `scraper/connectors/<name>`.
2. Inherit from `BaseConnector` in `scraper/connectors/base.py`.
3. Implement `initialize()`, `login()`, `search()`, and `extract_listing()`.
4. Create a parser in `scraper/parsers/<name>.py` to map raw extracted fields to the database schema.
5. Update `scraper.workers.tasks.py` to route to the new connector.

## Scaling

To support 10 million listings and 100 workers:
- Deploy `scraper_worker` containers dynamically using Kubernetes (HPA based on queue length).
- Scale Redis or use RabbitMQ for massive message queues.
- Ensure the database connection pool (`pool_size` in config) on each worker is balanced so 100 workers don't exhaust Postgres connection limits. Use PgBouncer in front of PostgreSQL.

## Debugging

- **Network Issues**: Playwright automatically retries. Celery handles task-level retries (exponential backoff).
- **Selector Changes**: If a marketplace changes its HTML structure, the Connector's `extract_listing()` might fail or return `None`. Update the CSS selectors in the connector.
- Logs are streamed to `stdout` in the Docker container and can be monitored via the backend Admin API.
