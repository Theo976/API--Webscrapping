import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.app import app

client = TestClient(app)

def test_register_validation():
    """Test la validation des données d'enregistrement"""
    response = client.post("/api/v1/auth/register", json={
        "email": "invalid-email",
        "password": "short",
        "role": "user"
    })
    assert response.status_code == 422

@patch('firebase_admin.auth')
def test_register_success(mock_auth):
    """Test l'enregistrement réussi d'un utilisateur"""
    mock_auth.create_user.return_value = MagicMock(uid="test123")
    
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "validPassword123",
        "role": "user"
    })
    assert response.status_code == 200
    assert "uid" in response.json()

def test_login_validation():
    """Test la validation des données de connexion"""
    response = client.post("/api/v1/auth/login", json={
        "email": "invalid-email",
        "password": ""
    })
    assert response.status_code == 422

@patch('src.auth.firebase_auth.verify_token')
def test_login_success(mock_verify):
    """Test la connexion réussie"""
    mock_verify.return_value = "fake_token"
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "validPassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_unauthorized_access():
    """Test l'accès non autorisé à la liste des utilisateurs"""
    response = client.get("/api/v1/auth/users")
    assert response.status_code == 403