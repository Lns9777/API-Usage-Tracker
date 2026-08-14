from __future__ import annotations

from datetime import datetime,timezone
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    environment: str = "development"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    environment: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProviderCreate(BaseModel):
    name: str


class ProviderResponse(ProviderCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ModelCreate(BaseModel):
    provider_id: int
    model_name: str
    model_type: str = "text"


class ModelResponse(ModelCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PricingCreate(BaseModel):
    model_id: int
    input_price_per_1m: float = 0.0
    output_price_per_1m: float = 0.0
    thinking_price_per_1m: float = 0.0
    cached_input_price_per_1m: float = 0.0
    currency: str = "USD"
    effective_from: datetime
    effective_to: Optional[datetime] = None


class PricingUpdate(BaseModel):
    input_price_per_1m: Optional[float] = None
    output_price_per_1m: Optional[float] = None
    thinking_price_per_1m: Optional[float] = None
    cached_input_price_per_1m: Optional[float] = None
    currency: Optional[str] = None
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None


class PricingResponse(PricingCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UsageDataIn(BaseModel):
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
    metadata: dict[str, Any] = Field(default_factory=dict)
    capture_content: bool = False


class UsageResponse(BaseModel):
    id: int
    project_id: int
    provider_id: int
    model_id: int
    internal_request_id: str
    provider_request_id: Optional[str]
    timestamp: datetime
    input_tokens: int
    output_tokens: int
    thinking_tokens: int
    cached_tokens: int
    total_tokens: int
    input_cost: float
    output_cost: float
    thinking_cost: float
    cached_cost: float
    total_cost: float
    audio_seconds: float
    characters: int
    request_count: int
    latency_ms: float
    status: str
    http_status_code: Optional[int]
    error_type: Optional[str]
    metadata_json: dict[str, Any]
    capture_content: bool
    model_config = ConfigDict(from_attributes=True)
