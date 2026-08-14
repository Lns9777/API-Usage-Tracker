"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-13 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("environment", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_index(op.f("ix_projects_name"), "projects", ["name"], unique=True)

    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_providers_id"), "providers", ["id"], unique=False)
    op.create_index(op.f("ix_providers_name"), "providers", ["name"], unique=True)

    op.create_table(
        "models",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=150), nullable=False),
        sa.Column("model_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"]),
        sa.UniqueConstraint("provider_id", "model_name", name="uq_provider_model_name"),
    )
    op.create_index(op.f("ix_models_id"), "models", ["id"], unique=False)
    op.create_index(op.f("ix_models_model_name"), "models", ["model_name"], unique=False)
    op.create_index(op.f("ix_models_provider_id"), "models", ["provider_id"], unique=False)

    op.create_table(
        "model_pricing",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("input_price_per_1m", sa.Float(), nullable=False),
        sa.Column("output_price_per_1m", sa.Float(), nullable=False),
        sa.Column("thinking_price_per_1m", sa.Float(), nullable=False),
        sa.Column("cached_input_price_per_1m", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("effective_from", sa.DateTime(), nullable=False),
        sa.Column("effective_to", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"]),
        sa.UniqueConstraint("model_id", "effective_from", name="uq_model_pricing_version"),
    )
    op.create_index(op.f("ix_model_pricing_id"), "model_pricing", ["id"], unique=False)
    op.create_index(op.f("ix_model_pricing_model_id"), "model_pricing", ["model_id"], unique=False)
    op.create_index(op.f("ix_model_pricing_effective_from"), "model_pricing", ["effective_from"], unique=False)
    op.create_index(op.f("ix_model_pricing_effective_to"), "model_pricing", ["effective_to"], unique=False)

    op.create_table(
        "api_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("provider_id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("internal_request_id", sa.String(length=255), nullable=False),
        sa.Column("provider_request_id", sa.String(length=255), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("thinking_tokens", sa.Integer(), nullable=False),
        sa.Column("cached_tokens", sa.Integer(), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False),
        sa.Column("input_cost", sa.Float(), nullable=False),
        sa.Column("output_cost", sa.Float(), nullable=False),
        sa.Column("thinking_cost", sa.Float(), nullable=False),
        sa.Column("cached_cost", sa.Float(), nullable=False),
        sa.Column("total_cost", sa.Float(), nullable=False),
        sa.Column("audio_seconds", sa.Float(), nullable=False),
        sa.Column("characters", sa.Integer(), nullable=False),
        sa.Column("request_count", sa.Integer(), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("http_status_code", sa.Integer(), nullable=True),
        sa.Column("error_type", sa.String(length=100), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("capture_content", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["provider_id"], ["providers.id"]),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"]),
        sa.UniqueConstraint("internal_request_id"),
    )
    op.create_index(op.f("ix_api_usage_id"), "api_usage", ["id"], unique=False)
    op.create_index(op.f("ix_api_usage_internal_request_id"), "api_usage", ["internal_request_id"], unique=True)
    op.create_index(op.f("ix_api_usage_model_id"), "api_usage", ["model_id"], unique=False)
    op.create_index(op.f("ix_api_usage_project_id"), "api_usage", ["project_id"], unique=False)
    op.create_index(op.f("ix_api_usage_provider_id"), "api_usage", ["provider_id"], unique=False)
    op.create_index(op.f("ix_api_usage_timestamp"), "api_usage", ["timestamp"], unique=False)


def downgrade():
    op.drop_table("api_usage")
    op.drop_table("model_pricing")
    op.drop_table("models")
    op.drop_table("providers")
    op.drop_table("projects")
