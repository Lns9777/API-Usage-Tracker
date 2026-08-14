# API Tracker

API Tracker is a local-first API usage and cost observability app. It tracks requests, token usage, latency, errors, and versioned pricing for provider models such as OpenAI and Gemini.

## Core Principles

- Local storage by default
- No prompts or responses stored
- No raw API keys stored
- Pricing is versioned and preserved historically
- Tracking failures never break provider calls

## Features

- FastAPI backend with SQLite storage
- Versioned pricing records
- Usage capture for input, output, thinking, and cached tokens
- Cost calculation per request
- Analytics overview and per-dimension breakdowns
- React + Vite dashboard
- Provider, model, and pricing management pages
- Python SDK for OpenAI and Gemini adapters
- Backend and frontend test coverage

## Repository Layout

```text
APITracker/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── routes/
│       └── services/
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

## Backend API

The backend exposes these main routes:

- `GET /`
- `GET /health`
- `GET /projects`
- `GET /usage`
- `GET /usage/{usage_id}`
- `GET /pricing`
- `POST /pricing`
- `PUT /pricing/{pricing_id}`
- `DELETE /pricing/{pricing_id}`
- `GET /providers`
- `POST /providers`
- `GET /models`
- `POST /models`
- `GET /analytics/overview`
- `GET /analytics/cost`
- `GET /analytics/tokens`
- `GET /analytics/latency`
- `GET /analytics/errors`
- `GET /analytics/by-project`
- `GET /analytics/by-provider`
- `GET /analytics/by-model`

## Frontend Pages

- Overview
- Projects
- Usage
- Analytics
- Providers
- Models
- Pricing
- Errors
- Settings

## Environment

Copy `.env.example` to `.env` and adjust values as needed.

```bash
DATABASE_URL=sqlite:///./api_tracker.db
OPENAI_API_KEY=
GEMINI_API_KEY=
VITE_API_BASE_URL=http://localhost:8000
TRACKER_BACKEND_URL=http://localhost:8000
```

Notes:

- `DATABASE_URL` defaults to local SQLite
- API keys are only used by the SDK at runtime
- No secrets are intended to be stored in the app database

## Installation

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

## Run Locally

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

## SDK Usage

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

The SDK reads usage metadata from the provider response and sends it to the local backend automatically.

## Pricing

Pricing is stored in the local database as versioned records.

Each pricing row includes:

- `model_id`
- `input_price_per_1m`
- `output_price_per_1m`
- `thinking_price_per_1m`
- `cached_input_price_per_1m`
- `currency`
- `effective_from`
- `effective_to`

Historical usage is resolved against the pricing row active at the request timestamp.

## Local-Only Policy

This app is intentionally local-first:

- Usage data stays on the local backend unless you change the deployment target
- Prompts and responses are not meant to be persisted
- API keys are not stored in the database
- Pricing and model metadata are stored locally for observability

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

## Common Commands

### Start backend

```bash
uvicorn backend.app.main:app --reload
```

### Start frontend

```bash
cd frontend
npm run dev
```

### Run backend tests

```bash
pytest -q
```

### Run frontend tests

```bash
cd frontend
npm run test -- --run
```

### Build frontend

```bash
cd frontend
npm run build
```

### Run with Docker

```bash
docker compose up --build
```

## Notes

- SQLite database file: `api_tracker.db`
- Alembic migrations live in `migrations/`
- The app currently uses a lightweight dashboard layout instead of a heavy charting stack
- Cost totals can be very small, so some UI cards may need higher decimal precision than `toFixed(2)`

