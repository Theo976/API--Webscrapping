from unittest.mock import MagicMock

# Mock Firebase
class MockFirebase:
    def __init__(self):
        self.auth = MagicMock()
        self.firestore = MagicMock()

# Mock pour la base de données
class MockDB:
    def __init__(self):
        self.collection = MagicMock()
        self.document = MagicMock()

# Créer les instances mock
mock_firebase = MockFirebase()
mock_db = MockDB() 