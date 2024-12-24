import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.app import app

client = TestClient(app)

@patch('src.services.parameters.get_parameters')
def test_get_parameters(mock_get):
    """Test la récupération des paramètres"""
    mock_get.return_value = {
        "n_estimators": 100,
        "criterion": "gini"
    }
    response = client.get("/api/v1/parameters")
    assert response.status_code == 200
    data = response.json()
    assert "n_estimators" in data
    assert "criterion" in data 