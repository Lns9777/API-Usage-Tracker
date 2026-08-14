from __future__ import annotations

import time

from google import genai

from ..tracker import Tracker


class GeminiTracker:
    def __init__(self, api_key: str, project: str, backend_url: str = "http://localhost:8000"):
        self.client = genai.Client(api_key=api_key)
        self.tracker = Tracker(project=project, provider="gemini", backend_url=backend_url)

    def generate(self, model: str, contents, **kwargs):
        start = time.perf_counter()
        try:
            response = self.client.models.generate_content(model=model, contents=contents, **kwargs)
            latency_ms = (time.perf_counter() - start) * 1000
            usage = getattr(response, "usage_metadata", None)
            self.tracker.record(
                model=model,
                input_tokens=getattr(usage, "prompt_token_count", 0) if usage else 0,
                output_tokens=getattr(usage, "candidates_token_count", 0) if usage else 0,
                thinking_tokens=getattr(usage, "thoughts_token_count", 0) if usage else 0,
                cached_tokens=getattr(usage, "cached_content_token_count", 0) if usage else 0,
                total_tokens=getattr(usage, "total_token_count", 0) if usage else 0,
                provider_request_id=getattr(response, "response_id", None),
                latency_ms=latency_ms,
                status="success",
            )
            return response
        except Exception as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            self.tracker.record(model=model, latency_ms=latency_ms, status="error", error_type=type(exc).__name__)
            raise
