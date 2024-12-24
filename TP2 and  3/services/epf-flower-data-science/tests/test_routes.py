import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_data_endpoints():
    """Test data processing endpoints"""
    # Test load
    response = client.get("/api/v1/data/load")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Test process
    response = client.get("/api/v1/data/process")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Test split
    response = client.get("/api/v1/data/split")
    assert response.status_code == 200
    data = response.json()
    assert "train" in data
    assert "test" in data

def test_model_endpoints():
    """Test model endpoints"""
    # Test train
    response = client.post("/api/v1/model/train")
    assert response.status_code == 200

    # Test predict
    response = client.get("/api/v1/model/predict", params={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert "prediction" in response.json()