import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.app import app

client = TestClient(app)

@patch('src.services.data.load_trained_model')
def test_predict_endpoint(mock_model):
    """Test les prédictions du modèle"""
    model = MagicMock()
    model.predict.return_value = ["Iris-setosa"]
    mock_model.return_value = model
    
    response = client.get("/api/v1/model/predict/", params={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert "prediction" in response.json()

@patch('src.services.data.train_model')
def test_train_endpoint(mock_train):
    """Test l'entraînement du modèle"""
    mock_train.return_value = True
    response = client.post("/api/v1/model/train")
    assert response.status_code == 200 