from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class UsageData:
    project: str
    provider: str
    model: str
    internal_request_id: str
    provider_request_id: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    thinking_tokens: int = 0
    cached_tokens: int = 0
    total_tokens: int = 0
    audio_seconds: float = 0.0
    characters: int = 0
    request_count: int = 1
    latency_ms: float = 0.0
    status: str = "success"
    http_status_code: Optional[int] = None
    error_type: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    capture_content: bool = False

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
