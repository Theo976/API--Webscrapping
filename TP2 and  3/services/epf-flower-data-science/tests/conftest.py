import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Ajouter le répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Mock Firebase et Slowapi
mock_limiter = MagicMock()
mock_limiter.limit = lambda *args, **kwargs: lambda x: x

class MockSlowapi:
    def __init__(self):
        self.Limiter = lambda *args, **kwargs: mock_limiter

# Mock tous les modules externes
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.auth'] = MagicMock()
sys.modules['firebase_admin.firestore'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['slowapi'] = MockSlowapi()
sys.modules['slowapi.util'] = MagicMock()
sys.modules['slowapi.errors'] = MagicMock()
sys.modules['email_validator'] = MagicMock()

@pytest.fixture(scope="module")
def client():
    from src.app import get_application
    app = get_application()
    with TestClient(app) as test_client:
        yield test_client