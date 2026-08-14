from fastapi.testclient import TestClient

from backend.app.main import app


def test_provider_and_model_routes():
    client = TestClient(app)
    provider = client.post("/providers", json={"name": "openai"})
    assert provider.status_code == 200
    provider_id = provider.json()["id"]

    providers = client.get("/providers")
    assert providers.status_code == 200
    assert providers.json()[0]["name"] == "openai"

    model = client.post(
        "/models",
        json={"provider_id": provider_id, "model_name": "gpt-5", "model_type": "text"},
    )
    assert model.status_code == 200

    models = client.get("/models")
    assert models.status_code == 200
    assert models.json()[0]["model_name"] == "gpt-5"
