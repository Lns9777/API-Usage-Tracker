from fastapi.testclient import TestClient

from backend.app.main import app


def test_analytics_endpoints_exist():
    client = TestClient(app)

    overview = client.get("/analytics/overview")
    assert overview.status_code == 200

    cost = client.get("/analytics/cost")
    assert cost.status_code == 200

    tokens = client.get("/analytics/tokens")
    assert tokens.status_code == 200

    latency = client.get("/analytics/latency")
    assert latency.status_code == 200

    errors = client.get("/analytics/errors")
    assert errors.status_code == 200
