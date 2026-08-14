from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, get_db
from backend.app.main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_module():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db


def teardown_module():
    app.dependency_overrides.clear()


def test_project_crud():
    client = TestClient(app)
    response = client.post("/projects", json={"name": "alpha", "description": "A", "environment": "dev"})
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "alpha"

    response = client.put(f"/projects/{project_id}", json={"description": "B"})
    assert response.status_code == 200
    assert response.json()["description"] == "B"


def test_pricing_and_usage_endpoints():
    client = TestClient(app)
    provider = client.post("/providers", json={"name": "openai"}).json()
    model = client.post("/models", json={"provider_id": provider["id"], "model_name": "gpt-5", "model_type": "text"}).json()
    client.post(
        "/pricing",
        json={
            "model_id": model["id"],
            "input_price_per_1m": 1.0,
            "output_price_per_1m": 2.0,
            "thinking_price_per_1m": 3.0,
            "cached_input_price_per_1m": 4.0,
            "currency": "USD",
            "effective_from": datetime.utcnow().isoformat(),
            "effective_to": None,
        },
    )
    usage = client.post(
        "/usage",
        json={
            "project": "alpha",
            "provider": "openai",
            "model": "gpt-5",
            "internal_request_id": "req-1",
            "input_tokens": 1000000,
            "output_tokens": 1000000,
            "thinking_tokens": 1000000,
            "cached_tokens": 1000000,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
    assert usage.status_code == 200
    assert usage.json()["total_cost"] == 10.0


def test_analytics_overview():
    client = TestClient(app)
    response = client.get("/analytics/overview")
    assert response.status_code == 200
    assert "requests" in response.json()
