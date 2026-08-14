from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base
from backend.app.models import ModelPricing, Project, Provider, Model
from backend.app.services.usage_service import create_usage, get_applicable_pricing


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def seed_pricing(db):
    project = Project(name="demo", environment="dev")
    provider = Provider(name="openai")
    model = Model(model_name="gpt-5", model_type="text", provider=provider)
    db.add_all([project, provider, model])
    db.commit()
    db.refresh(model)
    db.add(
        ModelPricing(
            model_id=model.id,
            input_price_per_1m=1.0,
            output_price_per_1m=2.0,
            thinking_price_per_1m=3.0,
            cached_input_price_per_1m=4.0,
            currency="USD",
            effective_from=datetime(2026, 1, 1),
            effective_to=datetime(2026, 6, 30),
        )
    )
    db.commit()
    return model


def test_get_applicable_pricing_returns_version_for_timestamp():
    db = make_session()
    model = seed_pricing(db)
    pricing = get_applicable_pricing(db, model.id, datetime(2026, 3, 1))
    assert pricing is not None
    assert pricing.input_price_per_1m == 1.0


def test_create_usage_applies_pricing_snapshot():
    db = make_session()
    seed_pricing(db)
    usage = create_usage(
        db,
        {
            "project": "demo",
            "provider": "openai",
            "model": "gpt-5",
            "internal_request_id": "req-1",
            "input_tokens": 1_000_000,
            "output_tokens": 1_000_000,
            "thinking_tokens": 1_000_000,
            "cached_tokens": 1_000_000,
            "timestamp": datetime(2026, 3, 1),
        },
    )
    assert usage.total_cost == 10.0
    assert usage.input_cost == 1.0
