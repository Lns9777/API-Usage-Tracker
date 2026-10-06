from __future__ import annotations

import os
import socket
import threading
import webbrowser

import uvicorn


def find_available_port(host: str, preferred_port: int = 8000) -> int:
    """Prefer the standard port, then choose the first available port."""
    candidates = (
        [preferred_port]
        if preferred_port == 0
        else range(preferred_port, preferred_port + 100)
    )
    for port in candidates:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind((host, port))
            except OSError:
                continue
            return probe.getsockname()[1]
    raise RuntimeError(
        f"No available port found between {preferred_port} and {preferred_port + 99}"
    )


def launch_app(*_args: str) -> None:
    host = os.getenv("API_TRACKER_HOST", "127.0.0.1")
    requested_port = int(os.getenv("API_TRACKER_PORT", "8000"))
    port = find_available_port(host, requested_port)
    open_browser = os.getenv("API_TRACKER_OPEN_BROWSER", "true").lower() not in {
        "0",
        "false",
        "no",
    }
    print(f"API Tracker dashboard: http://{host}:{port}")
    if open_browser:
        url = f"http://{host}:{port}"
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)
