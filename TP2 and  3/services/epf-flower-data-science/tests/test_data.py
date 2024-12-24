import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.app import app

client = TestClient(app)

def test_process_data():
    """Test le traitement des données"""
    response = client.get("/api/v1/data/process")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_split_data():
    """Test la séparation des données"""
    response = client.get("/api/v1/data/split")
    assert response.status_code == 200
    data = response.json()
    assert "train" in data
    assert "test" in data 