from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)


class TrackerTransport:
    def __init__(self, endpoint: str, timeout: float = 2.0):
        self.endpoint = endpoint.rstrip("/")
        self.timeout = timeout

    def send_usage(self, usage: dict) -> bool:
        try:
            response = requests.post(f"{self.endpoint}/usage", json=usage, timeout=self.timeout)
            if not response.ok:
                print("Usage payload:", usage)
                print("Backend response:", response.status_code, response.text)
            response.raise_for_status()
            return True
        except Exception as exc:
            logger.exception("API Tracker failed to record usage: %s", exc)
            return False
