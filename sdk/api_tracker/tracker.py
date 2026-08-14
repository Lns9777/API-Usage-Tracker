from __future__ import annotations

import logging
import uuid

from .models import UsageData
from .transport import TrackerTransport

logger = logging.getLogger(__name__)


class Tracker:
    def __init__(self, project: str, provider: str, backend_url: str = "http://localhost:8000"):
        self.project = project
        self.provider = provider
        self.transport = TrackerTransport(backend_url)

    def record(self, model: str, **kwargs):
        def _int_or_zero(value):
            return 0 if value is None else int(value)

        usage = UsageData(
            project=self.project,
            provider=self.provider,
            model=model,
            internal_request_id=kwargs.get("internal_request_id") or str(uuid.uuid4()),
            provider_request_id=kwargs.get("provider_request_id"),
            input_tokens=_int_or_zero(kwargs.get("input_tokens", 0)),
            output_tokens=_int_or_zero(kwargs.get("output_tokens", 0)),
            thinking_tokens=_int_or_zero(kwargs.get("thinking_tokens", 0)),
            cached_tokens=_int_or_zero(kwargs.get("cached_tokens", 0)),
            total_tokens=_int_or_zero(kwargs.get("total_tokens", 0)),
            audio_seconds=kwargs.get("audio_seconds", 0.0),
            characters=kwargs.get("characters", 0),
            request_count=kwargs.get("request_count", 1),
            latency_ms=kwargs.get("latency_ms", 0.0),
            status=kwargs.get("status", "success"),
            http_status_code=kwargs.get("http_status_code"),
            error_type=kwargs.get("error_type"),
            metadata=kwargs.get("metadata", {}),
            capture_content=kwargs.get("capture_content", False),
        )
        try:
            self.transport.send_usage(usage.to_dict())
        except Exception as exc:
            logger.exception("Tracking failed: %s", exc)
        return usage
