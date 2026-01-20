# Payout Service (Django + DRF + Celery)

REST API for managing payout requests with asynchronous processing via Celery.

## Key Features

- Layered architecture: API → services → repositories
- PostgreSQL persistence and async processing via Celery + Redis
- DRF + Swagger UI (drf-spectacular)
- Validation on input (amount, recipient details, description length)
- Safe Celery enqueue on transaction commit
- Seed data command for local/dev usage

## Requirements

- Python 3.10+
- PostgreSQL
- Redis (broker + result backend)

## Setup (local, without Docker)

1. Create `.env` from `.env.example` (use local DB/Redis settings).
2. Install dependencies:

```bash
make install
```

3. Apply migrations:

```bash
make migrate
```

4. Seed initial data:

```bash
make seed
```

5. Run API:

```bash
make run
```

6. Run Celery worker:

```bash
make worker
```

## Setup (Docker)

```bash
docker compose up --build
```

Then run migrations and seed (inside the container):

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_payouts
```

Notes:
- The local steps are only for running without Docker.
- With Docker, you only need the Docker section above.

## API

- Base: `http://localhost:8000/api/` (also available as `/api/v1/`)
- Healthcheck: `http://localhost:8000/health/`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

### Endpoints

- `GET /api/payouts/`
- `GET /api/payouts/{id}/`
- `POST /api/payouts/`
- `PATCH /api/payouts/{id}/`
- `DELETE /api/payouts/{id}/`

## Tests

```bash
make test
```

## Type Checking (optional)

```bash
make typecheck
```

## Deployment (concept)

- Services: PostgreSQL, Redis, Django web app, Celery worker
- Run Django with Gunicorn + a process manager (systemd or supervisor)
- Run Celery worker as a separate service; scale by adding workers
- Use a reverse proxy (Nginx) for TLS termination and static/media handling
- Configure environment variables and secrets in the deployment environment
- Apply migrations during deploy and run health checks after rollout

## Notes

- Celery task updates payout status from `pending` → `processing` → `completed`.
- `recipient_details` requires an `account` field.
