
import json
from pathlib import Path

from backend.app import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_prediction_with_sample_input():
    client = app.test_client()

    with open(
        PROJECT_ROOT / "sample_input.json",
        encoding="utf-8"
    ) as file:
        sample = json.load(file)

    response = client.post("/predict", json=sample)

    assert response.status_code == 200

    result = response.get_json()
    assert result["prediction"] in [0, 1]
    assert result["class"] in ["Normal", "Attack"]
    assert "model" in result


def test_missing_features_returns_400():
    client = app.test_client()

    response = client.post("/predict", json={})

    assert response.status_code == 400
