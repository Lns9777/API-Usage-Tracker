<div align="center">

# 📊 llmapi-tracker

**A local-first API usage and cost observability platform for LLM applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#prerequisites)
[![Node](https://img.shields.io/badge/node-20%2B-green.svg)](#prerequisites)
[![Local First](https://img.shields.io/badge/data-local--first-brightgreen.svg)](#what-api-tracker-is)

</div>

---

## Table of Contents

- [What API Tracker Is](#what-api-tracker-is)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Development Install](#local-development-install)
  - [Package Install](#package-install)
- [Starting the Application](#starting-the-application)
- [SDK Usage](#sdk-usage)
- [Database Location](#database-location)
- [Configuration](#configuration)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)

---

## What API Tracker Is

`llmapi-tracker` is a **local-first API usage and cost observability platform** for LLM applications. It records request counts, token usage, latency, errors, and versioned pricing for provider models such as OpenAI and Gemini.

The project is designed to keep data local by default. It stores usage and pricing in a local SQLite database and **does not persist prompts, responses, or raw API keys** in the application database.

---

## Features

| Category | Capability |
|---|---|
| 🖥️ Backend | Local FastAPI backend with SQLite storage |
| 💰 Pricing | Versioned pricing records for historical cost tracking |
| 📈 Usage | Capture for input, output, thinking, cached, and total tokens |
| 🧮 Cost | Request-level and analytics-level cost calculation |
| 📊 Dashboard | React + Vite dashboard for usage, analytics, providers, models, and pricing |
| 🔌 SDKs | Wrappers for OpenAI and Gemini |
| 🚀 Launcher | Packaged launcher command that starts the local app and opens the browser |
| 🧪 Quality | Open-source repository with tests, CI, and release automation |

---

## Installation

### Prerequisites

- Python **3.10** or newer
- Node.js **20** or newer for frontend development

### Local Development Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd frontend
npm install
```

### Package Install

```bash
pip install llmapi-tracker
```

Optional provider SDK support:

```bash
pip install "llmapi-tracker[openai]"
pip install "llmapi-tracker[gemini]"
pip install "llmapi-tracker[all]"
```

---

## Starting the Application

### Backend Only

```bash
uvicorn backend.app.main:app --reload
```

### Frontend Only

```bash
cd frontend
npm run dev
```

### Packaged App

After the frontend assets are built and packaged into the backend static directory:

```bash
api-tracker
```

> The launcher starts the backend server and opens the browser to the local dashboard.

---

## SDK Usage

### Initialize the SDK

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

> The SDK reads usage metadata from the provider response and sends it to the local backend automatically.

---

## Database Location

By default, the SQLite database is stored in a stable user data directory so it survives uninstall and reinstall.

The path is resolved in this order:

1. `API_TRACKER_DB_PATH` if set
2. `DATABASE_URL` if set
3. A user-data location based on the operating system

**Typical defaults**

| OS | Path |
|---|---|
| Windows | `%LOCALAPPDATA%\APITracker\api_tracker.db` |
| macOS / Linux | `~/.local/share/APITracker/api_tracker.db` |

> If the preferred user-data directory cannot be created, the app falls back to a writable local `.api-tracker-data/` directory in the current workspace.

---

## Configuration

Environment variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | Overrides the database connection string |
| `API_TRACKER_DATA_DIR` | Sets the user-data root used for SQLite storage |
| `API_TRACKER_DB_PATH` | Points directly to a specific SQLite file |
| `API_TRACKER_HOST` | Host the backend binds to (default `127.0.0.1`) |
| `API_TRACKER_PORT` | Port the backend binds to (default `8000`) |
| `API_TRACKER_OPEN_BROWSER` | Set to `false` to disable browser auto-open for the launcher |
| `OPENAI_API_KEY` | API key used by the OpenAI SDK wrapper |
| `GEMINI_API_KEY` | API key used by the Gemini SDK wrapper |
| `TRACKER_BACKEND_URL` | Backend URL used by the SDK client |
| `VITE_API_BASE_URL` | Backend URL used by the frontend dashboard |

Example `.env`:

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

---

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

### Packaging Assets

```bash
cd frontend
npm run build
cd ..
python scripts/package_frontend_assets.py
python scripts/verify_frontend_assets.py
```

---

## Contributing

`llmapi-tracker` is intended to be open source and contributor friendly.

**Contribution files**

- [`CONTRIBUTING.md`](L:/Personal/APITracker/CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](L:/Personal/APITracker/CODE_OF_CONDUCT.md)
- [`SECURITY.md`](L:/Personal/APITracker/SECURITY.md)
- [`CHANGELOG.md`](L:/Personal/APITracker/CHANGELOG.md)
- [`LICENSE`](L:/Personal/APITracker/LICENSE)

**Contribution expectations**

- ✅ Open changes through pull requests
- ✅ Require review before merge
- ✅ Keep the app local-first
- 🚫 Avoid storing prompts, responses, or raw API keys
- ✅ Add tests for behavior changes

---

## License

`llmapi-tracker` is released under the **MIT License**. See [`LICENSE`](L:/Personal/APITracker/LICENSE).