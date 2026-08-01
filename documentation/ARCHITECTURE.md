# CarScope AI - Enterprise Architecture

CarScope AI is a microservices-inspired monolithic architecture built for scale.

## Core Modules
1. **Scraper Engine**: Distributed Celery workers fetching raw data from marketplaces (Cars24, Spinny, etc.) via a dynamic Plugin Architecture.
2. **AI Valuation Engine**: Leverages ML models (LightGBM) and Gemini LLMs to predict true market values and assess vehicle conditions.
3. **Deal Engine**: Scores listings (0-100) based on price-to-value ratios, days on market, and depreciation curves.
4. **Search Engine**: Meilisearch backend providing sub-50ms typo-tolerant search and natural language filtering.
5. **Operations Platform**: Centralized control plane for Auth (JWT, RBAC), Notifications, Audit Logging, and System Monitoring.
6. **AI Copilot**: Natural language assistant translating user queries to structured database queries and synthesizing responses.

## Tech Stack
- **API**: FastAPI (Python 3.11, async)
- **Database**: PostgreSQL 15 (SQLAlchemy Async, Alembic)
- **Cache & Queue**: Redis 7
- **Search**: Meilisearch 1.6
- **Workers**: Celery
- **Infrastructure**: Kubernetes, Docker, Nginx
- **CI/CD**: GitHub Actions
