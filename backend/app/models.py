from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.utcnow()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    environment = Column(String(50), default="development", nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    usage = relationship("ApiUsage", back_populates="project")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    models = relationship("Model", back_populates="provider", cascade="all, delete-orphan")


class Model(Base):
    __tablename__ = "models"
    __table_args__ = (UniqueConstraint("provider_id", "model_name", name="uq_provider_model_name"),)

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False, index=True)
    model_name = Column(String(150), nullable=False, index=True)
    model_type = Column(String(50), default="text", nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)

    provider = relationship("Provider", back_populates="models")
    pricing = relationship("ModelPricing", back_populates="model", cascade="all, delete-orphan")
    usage = relationship("ApiUsage", back_populates="model_ref")


class ModelPricing(Base):
    __tablename__ = "model_pricing"
    __table_args__ = (
        UniqueConstraint("model_id", "effective_from", name="uq_model_pricing_version"),
    )

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    input_price_per_1m = Column(Float, default=0.0, nullable=False)
    output_price_per_1m = Column(Float, default=0.0, nullable=False)
    thinking_price_per_1m = Column(Float, default=0.0, nullable=False)
    cached_input_price_per_1m = Column(Float, default=0.0, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    effective_from = Column(DateTime, default=utcnow, nullable=False, index=True)
    effective_to = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    model = relationship("Model", back_populates="pricing")


class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    internal_request_id = Column(String(255), nullable=False, unique=True, index=True)
    provider_request_id = Column(String(255), nullable=True, index=True)
    timestamp = Column(DateTime, default=utcnow, nullable=False, index=True)
    input_tokens = Column(Integer, default=0, nullable=False)
    output_tokens = Column(Integer, default=0, nullable=False)
    thinking_tokens = Column(Integer, default=0, nullable=False)
    cached_tokens = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    input_cost = Column(Float, default=0.0, nullable=False)
    output_cost = Column(Float, default=0.0, nullable=False)
    thinking_cost = Column(Float, default=0.0, nullable=False)
    cached_cost = Column(Float, default=0.0, nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)
    audio_seconds = Column(Float, default=0.0, nullable=False)
    characters = Column(Integer, default=0, nullable=False)
    request_count = Column(Integer, default=1, nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
    status = Column(String(30), default="success", nullable=False)
    http_status_code = Column(Integer, nullable=True)
    error_type = Column(String(100), nullable=True)
    metadata_json = Column(JSON, default=dict, nullable=False)
    capture_content = Column(Boolean, default=False, nullable=False)

    project = relationship("Project", back_populates="usage")
    provider = relationship("Provider")
    model_ref = relationship("Model", back_populates="usage")
