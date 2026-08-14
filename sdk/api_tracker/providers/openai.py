from __future__ import annotations

import time

from openai import OpenAI

from ..tracker import Tracker


class OpenAITracker:
    def __init__(self, api_key: str, project: str, backend_url: str = "http://localhost:8000"):
        self.client = OpenAI(api_key=api_key)
        self.tracker = Tracker(project=project, provider="openai", backend_url=backend_url)

    def chat(self, model: str, messages: list, **kwargs):
        start = time.perf_counter()
        try:
            response = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
            latency_ms = (time.perf_counter() - start) * 1000
            usage = getattr(response, "usage", None)
            self.tracker.record(
                model=model,
                input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
                output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
                thinking_tokens=getattr(usage, "reasoning_tokens", 0) if usage else 0,
                cached_tokens=getattr(usage, "cached_tokens", 0) if usage else 0,
                total_tokens=getattr(usage, "total_tokens", 0) if usage else 0,
                provider_request_id=getattr(response, "_request_id", None),
                latency_ms=latency_ms,
                status="success",
            )
            return response
        except Exception as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            self.tracker.record(model=model, latency_ms=latency_ms, status="error", error_type=type(exc).__name__)
            raise
