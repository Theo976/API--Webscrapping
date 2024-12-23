import pytest
from fastapi.testclient import TestClient
import os
from unittest.mock import patch, MagicMock

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200

@patch('src.services.data.load_trained_model')
@patch('os.path.exists')
@patch('joblib.load')
def test_predict_endpoint(mock_joblib, mock_exists, mock_model, client):
    # Mock le modèle avec plus de détails
    model = MagicMock()
    model.predict.return_value = ["setosa"]
    mock_model.return_value = model
    mock_exists.return_value = True
    mock_joblib.return_value = model
    
    response = client.get("/api/v1/predict", params={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == "setosa"

@patch('src.api.router.get_parameters')
def test_parameters_endpoint(mock_params, client):
    # Définir les paramètres attendus
    expected_params = {
        "n_estimators": 100,
        "criterion": "gini"
    }
    
    # Mock direct de get_parameters
    mock_params.return_value = expected_params
    print(f"Mock return value: {mock_params.return_value}")  # Debug log
    
    response = client.get("/api/v1/parameters")
    print(f"Response status: {response.status_code}")  # Debug log
    print(f"Response body: {response.json()}")  # Debug log
    
    assert response.status_code == 200
    data = response.json()
    assert data == expected_params, f"Expected {expected_params}, got {data}"

def test_invalid_endpoint(client):
    response = client.get("/api/v1/invalid")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data