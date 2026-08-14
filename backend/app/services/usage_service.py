from __future__ import annotations

from datetime import datetime,timezone
from typing import Any

from sqlalchemy.orm import Session

from ..models import ApiUsage, Model, ModelPricing, Project, Provider
from .cost_service import PricingSnapshot, calculate_costs


def _get_or_create_project(db: Session, name: str) -> Project:
    project = db.query(Project).filter(Project.name == name).first()
    if project:
        return project
    project = Project(name=name, environment="development")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def _get_or_create_provider(db: Session, name: str) -> Provider:
    provider = db.query(Provider).filter(Provider.name == name).first()
    if provider:
        return provider
    provider = Provider(name=name)
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def _get_or_create_model(db: Session, provider_id: int, model_name: str) -> Model:
    model = (
        db.query(Model)
        .filter(Model.provider_id == provider_id, Model.model_name == model_name)
        .first()
    )
    if model:
        return model
    model = Model(provider_id=provider_id, model_name=model_name, model_type="text")
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_applicable_pricing(
    db: Session, model_id: int, timestamp: datetime
) -> ModelPricing | None:
    pricing = (
        db.query(ModelPricing)
        .filter(
            ModelPricing.model_id == model_id,
            ModelPricing.effective_from <= timestamp,
            (
                (ModelPricing.effective_to.is_(None))
                | (ModelPricing.effective_to >= timestamp)
            ),
        )
        .order_by(ModelPricing.effective_from.desc())
        .first()
    )
    if pricing:
        return pricing
    return (
        db.query(ModelPricing)
        .filter(ModelPricing.model_id == model_id)
        .order_by(ModelPricing.effective_from.desc())
        .first()
    )


def create_usage(db: Session, payload: dict[str, Any]) -> ApiUsage:
    project = _get_or_create_project(db, payload["project"])
    provider = _get_or_create_provider(db, payload["provider"])
    model = _get_or_create_model(db, provider.id, payload["model"])
    # timestamp = payload.get("timestamp") or datetime.utcnow()
    timestamp = payload.get("timestamp") or datetime.now(timezone.utc)
    pricing = get_applicable_pricing(db, model.id, timestamp)
    snapshot = PricingSnapshot(
        input_price_per_1m=getattr(pricing, "input_price_per_1m", 0.0),
        output_price_per_1m=getattr(pricing, "output_price_per_1m", 0.0),
        thinking_price_per_1m=getattr(pricing, "thinking_price_per_1m", 0.0),
        cached_input_price_per_1m=getattr(pricing, "cached_input_price_per_1m", 0.0),
    )
    costs = calculate_costs(
        pricing=snapshot,
        input_tokens=payload.get("input_tokens", 0),
        output_tokens=payload.get("output_tokens", 0),
        thinking_tokens=payload.get("thinking_tokens", 0),
        cached_tokens=payload.get("cached_tokens", 0),
    )
    usage = ApiUsage(
        project_id=project.id,
        provider_id=provider.id,
        model_id=model.id,
        internal_request_id=payload["internal_request_id"],
        provider_request_id=payload.get("provider_request_id"),
        timestamp=timestamp,
        input_tokens=payload.get("input_tokens", 0),
        output_tokens=payload.get("output_tokens", 0),
        thinking_tokens=payload.get("thinking_tokens", 0),
        cached_tokens=payload.get("cached_tokens", 0),
        total_tokens=payload.get("total_tokens", 0),
        input_cost=costs["input_cost"],
        output_cost=costs["output_cost"],
        thinking_cost=costs["thinking_cost"],
        cached_cost=costs["cached_cost"],
        total_cost=costs["total_cost"],
        audio_seconds=payload.get("audio_seconds", 0.0),
        characters=payload.get("characters", 0),
        request_count=payload.get("request_count", 1),
        latency_ms=payload.get("latency_ms", 0.0),
        status=payload.get("status", "success"),
        http_status_code=payload.get("http_status_code"),
        error_type=payload.get("error_type"),
        metadata_json=payload.get("metadata", {}),
        capture_content=payload.get("capture_content", False),
    )
    db.add(usage)
    db.commit()
    db.refresh(usage)
    return usage
