import pytest
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def client():
    from src.app import app
    from fastapi.testclient import TestClient
    return TestClient(app)