from fastapi.testclient import TestClient

def test_read_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
