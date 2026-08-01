# Operations Platform

The Operations Platform is the enterprise-grade operational backbone of CarScope AI. It provides administrators with complete control over the platform and offers robust security, auditing, and notifications for all users.

## Folder Structure

* **authentication/**: Comprehensive authentication system. Implements JWT, Refresh Tokens, Multi-device session tracking, device tracking, login history, password strength validation, and rate limiting (lockout policies).
* **authorization/**: Granular permission and role management system. Supports roles (SUPER_ADMIN, ADMIN, DEALER, BUSINESS_USER, NORMAL_USER, etc.) and fine-grained feature access via permissions.
* **notifications/**: Unified notification delivery engine. Handles in-app notifications, alerting systems for users (e.g., Saved Search matches, Price Drops), and future integrations for Push, SMS, and WhatsApp.
* **audit/**: Extensive logging and auditing system leveraging Redis Streams. Tracks logins, API requests, admin actions, and marketplace state changes with IP and User-Agent capture.
* **workers/**: Integrates with the Celery task queue to manage running tasks. Allows viewing, restarting, and managing scraper workers, queue statuses, and dead queues.
* **monitoring/**: Real-time system health dashboard integration. Exposes metrics on CPU, RAM, Postgres availability, Redis health, and general API latencies.
* **admin/**: Administrative API endpoints aggregating data from monitoring, workers, reports, and auditing to drive the Admin Dashboard.
* **settings/**: Dynamic system configuration. Manages feature flags, rate limit settings, marketplace toggles, and global environment overrides via Redis state without restarting the server.
* **jobs/**: Definitions for asynchronous, scheduled administrative operations.
* **emails/**: Robust HTML email templating and delivery service using SMTP. Handles Welcome, Password Reset, Price Drops, and Reporting emails.
* **reports/**: Automated reporting engine. Generates internal and marketplace analytics in CSV formats for growth, revenues, and system health.
* **tests/**: Unit and integration tests dedicated to operations modules, validating authentication policies, permission matrices, and rate-limiting.

## Security Features Built-in

* Brute Force Protection & IP Blocking via Redis lockout.
* Role-based Access Control (RBAC).
* Multi-device session invalidation (Logout Everywhere).
* Fully stateless scalable architecture backed by Async Postgres & Redis.

## Integration

The operations platform acts as a middleware and standalone API module in the `backend.main` app, leveraging the existing Database configurations and Celery workers created by other modules.
