from __future__ import annotations

import os
import threading
import webbrowser

import uvicorn


def launch_app() -> None:
    host = os.getenv("API_TRACKER_HOST", "127.0.0.1")
    port = int(os.getenv("API_TRACKER_PORT", "8000"))
    open_browser = os.getenv("API_TRACKER_OPEN_BROWSER", "true").lower() not in {
        "0",
        "false",
        "no",
    }
    if open_browser:
        url = f"http://{host}:{port}"
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)
