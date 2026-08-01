# CarScope AI - Production Readiness Checklist

## Infrastructure & Kubernetes
- [ ] Docker images optimized (multi-stage builds, non-root user).
- [ ] Kubernetes Deployments configured with Requests & Limits.
- [ ] Horizontal Pod Autoscalers (HPA) configured for Backend and Workers.
- [ ] Liveness and Readiness probes enabled and tested.
- [ ] Ingress configured with Let's Encrypt TLS certificates.
- [ ] Nginx proxy body sizes and rate limits tuned.

## Database & Storage
- [ ] PostgreSQL running in HA (High Availability) mode.
- [ ] Connection pooling enabled (PgBouncer).
- [ ] Automated daily point-in-time backups configured and tested via `backup.sh`.
- [ ] Redis persistence configured appropriately (AOF/RDB).
- [ ] Meilisearch disk volumes expanded and snapshotted daily.

## Security
- [ ] OWASP headers applied at Nginx level (CSP, HSTS, X-Frame-Options).
- [ ] JWT keys generated using high-entropy random strings.
- [ ] Passwords hashed using bcrypt.
- [ ] Rate limiting applied to `/auth` and public API endpoints.
- [ ] Database credentials mounted as Kubernetes Secrets, NOT env variables in plain text.
- [ ] Penetration testing and automated Bandit security scans passing.

## Observability
- [ ] Prometheus scraping configured for all services.
- [ ] Grafana dashboards built for Business Metrics, Queue Lengths, and API Latencies.
- [ ] FluentBit configured for structured JSON log aggregation to Elasticsearch/OpenSearch.
- [ ] Sentry (or similar) integrated for exception tracking in Backend and Celery workers.

## AI & Operations
- [ ] Gemini API Keys secured and rate limits monitored.
- [ ] Scraper plugins isolated; IP rotation/Proxies configured for Workers.
- [ ] Mobile API versioning enforced.
- [ ] Daily Market Reports automatically triggered and distributed.
