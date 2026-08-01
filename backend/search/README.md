# Search Engine & Data Intelligence

The Search Engine provides sub-second search capabilities over millions of listings using Meilisearch.

## Architecture

* **indexes/**: Contains the `MeiliSearchClient` wrapper and index setup logic.
* **ranking/**: Handled natively by Meilisearch via configured ranking rules (see `client.py`).
* **filters/**: `NaturalQueryParser` converts human-readable queries like "Toyota under 8 lakh automatic" into structured filters and clean text queries.
* **analytics/**: `SearchAnalyticsTracker` uses Redis to asynchronously log search latency, popular queries, no-result queries, and popular filters. Also includes `SavedSearchManager` for storing/retrieving user searches.
* **compare.py**: `CompareEngine` compares up to 10 vehicles by listing IDs, returning detailed differences.
* **recommendations.py**: Provides trending and similar vehicles.
* **jobs/**: Celery tasks to synchronize the Postgres database to the Meilisearch index incrementally.
* **tests/**: Unit testing for parsers, filters, and engines.

## Configuration

Set via environment variables in `config.py`:
* `SEARCH_MEILI_URL`: (default `http://localhost:7700`)
* `SEARCH_MEILI_MASTER_KEY`: Master key for Meilisearch
* `SEARCH_REDIS_URL`: For analytics (default `redis://localhost:6379/0`)
* `SEARCH_ENABLE_NLP_PARSING`: Toggle natural language parsing (default `True`)

## Features

1. **Instant Search & Typo Tolerance**: Powered by Meilisearch algorithms.
2. **Natural Language Parsing**: Automatically extracts `under X price`, `less than Y km`, `less than Z years old`, fuel, transmission, and body types from the query text.
3. **Advanced Filtering**: Combine structured filters seamlessly.
4. **Compare Engine**: Compare up to 10 cars side-by-side.
5. **Saved Searches**: Save queries and filters to run later.
6. **Search Analytics**: Tracks real-time search trends in Redis.

## API Endpoints

All endpoints are prefixed with `/api/v1/search/`

* `POST /`: Search listings (accepts query, filters, sort_by, pagination).
* `GET /autocomplete`: Returns keyword suggestions.
* `POST /saved`: Save a search.
* `GET /saved/{user_id}`: Get saved searches.
* `DELETE /saved/{user_id}/{search_id}`: Delete a saved search.
* `POST /compare`: Compare up to 10 listings.
* `GET /recommendations/trending`: Get trending vehicles.
* `GET /analytics/popular-queries`: Get top searched terms.
* `POST /jobs/sync`: Trigger DB -> Meilisearch sync.
