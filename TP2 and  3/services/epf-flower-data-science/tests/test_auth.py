import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_login_validation(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "invalid-email",
        "password": "password123"
    })
    assert response.status_code == 422

@patch('firebase_admin.auth')
def test_register_success(mock_auth, client):
    mock_auth.create_user.return_value = MagicMock(uid="test123")
    
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    })
    assert response.status_code == 200
    assert "uid" in response.json()

def test_unauthorized_access(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 403