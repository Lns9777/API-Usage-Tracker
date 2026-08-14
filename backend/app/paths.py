from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "API Tracker"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_data_dir() -> Path:
    override = os.getenv("API_TRACKER_DATA_DIR")
    if override:
        return _ensure_dir(Path(override).expanduser())

    if os.name == "nt":
        base = os.getenv("LOCALAPPDATA") or Path.home() / "AppData" / "Local"
        preferred = Path(base) / "APITracker"
        try:
            return _ensure_dir(preferred)
        except PermissionError:
            return _ensure_dir(Path.cwd() / ".api-tracker-data")

    if os.name == "posix":
        base = os.getenv("XDG_DATA_HOME")
        if base:
            preferred = Path(base) / "APITracker"
        else:
            preferred = Path.home() / ".local" / "share" / "APITracker"
        try:
            return _ensure_dir(preferred)
        except PermissionError:
            return _ensure_dir(Path.cwd() / ".api-tracker-data")

    return _ensure_dir(Path.cwd() / ".api-tracker-data")


def get_database_path() -> Path:
    override = os.getenv("API_TRACKER_DB_PATH")
    if override:
        path = Path(override).expanduser()
    else:
        path = get_data_dir() / "api_tracker.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_database_url() -> str:
    override = os.getenv("DATABASE_URL")
    if override:
        return override
    return f"sqlite:///{get_database_path().as_posix()}"


def get_frontend_dist_dir() -> Path:
    return Path(__file__).resolve().parent / "static"
