# API Tracker

API Tracker is a local-first API usage and cost observability platform. It tracks request counts, token usage, latency, errors, and versioned pricing for providers such as OpenAI and Gemini.

## Principles

- Local storage by default
- No prompts or responses stored
- No raw API keys stored
- Historical pricing is preserved with versioned records
- Tracking failures never break provider calls

## Repository Layout

```text
api-tracker/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── routes/
│       ├── services/
│       └── repositories/
├── frontend/
│   └── src/
│       ├── components/
│       ├── hooks/
│       ├── layouts/
│       ├── pages/
│       ├── services/
│       ├── types/
│       └── utils/
├── sdk/
│   └── api_tracker/
├── migrations/
├── tests/
├── .env.example
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## What It Includes

- FastAPI backend
- SQLAlchemy data model
- SQLite local storage by default
- Versioned pricing and historical cost calculation
- Python SDK with OpenAI and Gemini adapters
- React + Vite dashboard
- Local-only request filtering and inspection
- Backend and frontend tests
- Docker support

## Environment

Copy `.env.example` to `.env` if needed. The default values are local-first.

```bash
DATABASE_URL=sqlite:///./api_tracker.db
OPENAI_API_KEY=
GEMINI_API_KEY=
VITE_API_BASE_URL=http://localhost:8000
TRACKER_BACKEND_URL=http://localhost:8000
```

## Install

### Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run

### Backend

```bash
uvicorn backend.app.main:app --reload
```

### Frontend

```bash
cd frontend
npm run dev
```

### Docker

```bash
docker compose up --build
```

## Database

The default database is local SQLite:

- `api_tracker.db`

Alembic scaffold:

- `migrations/versions/0001_initial_schema.py`

Commands:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

## SDK

```python
import os
from api_tracker import APITracker

tracker = APITracker(
    project="Pharmacy-AI",
    backend_url=os.getenv("TRACKER_BACKEND_URL", "http://localhost:8000"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
)
```

### OpenAI

```python
response = tracker.openai.chat(
    model="gpt-5",
    messages=[{"role": "user", "content": "Analyze this prescription"}],
)
```

### Gemini

```python
response = tracker.gemini.generate(
    model="gemini-2.5-flash",
    contents="Analyze this prescription",
)
```

The SDK automatically reads usage metadata from the provider response. Developers do not pass token counts or cost manually.

## Pricing

Pricing is stored centrally in the local database, with versioning via:

- `effective_from`
- `effective_to`

Historical requests always use the pricing that was active when the request happened.

## Local-Only Policy

By default the app:

- stores data locally
- does not store prompts
- does not store responses
- does not store raw API keys
- does not expose any secret-persistence UI

If you change `DATABASE_URL`, that is an explicit deployment choice.

## Testing

### Backend

```bash
python -m compileall backend sdk tests
pytest -q
```

### Frontend

```bash
cd frontend
npm run test -- --run
npm run build
```

## Current Validation

- Python syntax check: passed
- Backend tests: passed
- Frontend tests: passed
- Frontend production build: passed

## Current Limits

- The dashboard uses lightweight charts instead of full charting libraries
- The request inspector is a modal, not a split-pane workflow
- The app is intentionally local-first, so team/shared deployment is not the default path

## Current Commands Summary

### Backend startup

```bash
uvicorn backend.app.main:app --reload
```

### Frontend startup

```bash
cd frontend
npm run dev
```

### Backend tests

```bash
pytest -q
```

### Frontend tests

```bash
cd frontend
npm run test -- --run
```

### Frontend build

```bash
cd frontend
npm run build
```

### Docker

```bash
docker compose up --build
```

