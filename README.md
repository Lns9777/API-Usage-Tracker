# API Tracker

## What API Tracker Is

API Tracker is a local-first API usage and cost observability tool. It records request volume, token usage, latency, status, and versioned pricing for models from providers such as OpenAI and Gemini.

The project is built to keep data local by default. It stores usage and pricing in a local SQLite database and does not persist prompts, responses, or raw API keys in the application database.

## Features

- Local FastAPI backend with SQLite storage
- Versioned pricing records for historical cost tracking
- Usage capture for input, output, thinking, cached, and total tokens
- Cost calculation per request and across analytics views
- React + Vite dashboard for usage, analytics, providers, models, and pricing
- SDK wrappers for OpenAI and Gemini
- Packaged launcher command that starts the local app and opens the browser
- Open-source repository setup with tests, CI, and release automation

## Installation

### Prerequisites

- Python 3.10 or newer
- Node.js 20 or newer for frontend development

### Local development install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd frontend
npm install
```

### Package install

If you install this project as a package, the launcher command is:

```bash
api-tracker
```

## Starting the Application

### Backend only

```bash
uvicorn backend.app.main:app --reload
```

### Frontend only

```bash
cd frontend
npm run dev
```

### Packaged app

After building the frontend assets and packaging them into the backend static directory, run:

```bash
api-tracker
```

The launcher starts the backend server and opens the browser to the local dashboard.

## SDK Usage

### Initialize the SDK

```python
import os
from sdk.api_tracker import APITracker

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

## Database Location

By default, the SQLite database is stored in a stable user data directory so it survives uninstall and reinstall.

The path is resolved in this order:

1. `API_TRACKER_DB_PATH` if set
2. `DATABASE_URL` if set
3. A user-data location based on the operating system

Typical defaults:

- Windows: `%LOCALAPPDATA%\\APITracker\\api_tracker.db`
- macOS/Linux: `~/.local/share/APITracker/api_tracker.db`

If the preferred user-data directory cannot be created, the app falls back to a writable local `.api-tracker-data/` directory in the current workspace.

## Configuration

Environment variables:

```bash
DATABASE_URL=sqlite:///./api_tracker.db
API_TRACKER_DATA_DIR=
API_TRACKER_DB_PATH=
API_TRACKER_HOST=127.0.0.1
API_TRACKER_PORT=8000
API_TRACKER_OPEN_BROWSER=true
OPENAI_API_KEY=
GEMINI_API_KEY=
TRACKER_BACKEND_URL=http://localhost:8000
VITE_API_BASE_URL=http://localhost:8000
```

Notes:

- `DATABASE_URL` overrides the database connection string
- `API_TRACKER_DATA_DIR` sets the user-data root used for SQLite storage
- `API_TRACKER_DB_PATH` points directly to a specific SQLite file
- `API_TRACKER_OPEN_BROWSER=false` disables browser auto-open for the launcher

## Development Setup

### Backend

```bash
python -m compileall backend sdk tests
pytest -q
```

### Frontend

```bash
cd frontend
npm run build
```

### Packaging assets

```bash
cd frontend
npm run build
cd ..
python scripts/package_frontend_assets.py
python scripts/verify_frontend_assets.py
```

## Contributing

This repository is intended to be open source and contributor friendly.

Contribution files:

- [`CONTRIBUTING.md`](L:/Personal/APITracker/CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](L:/Personal/APITracker/CODE_OF_CONDUCT.md)
- [`SECURITY.md`](L:/Personal/APITracker/SECURITY.md)
- [`CHANGELOG.md`](L:/Personal/APITracker/CHANGELOG.md)
- [`LICENSE`](L:/Personal/APITracker/LICENSE)

Contribution expectations:

- Open changes through pull requests
- Require review before merge
- Keep the app local-first
- Avoid storing prompts, responses, or raw API keys
- Add tests for behavior changes

## License

API Tracker is released under the MIT License. See [`LICENSE`](L:/Personal/APITracker/LICENSE).

