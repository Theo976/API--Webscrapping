import pytest
from unittest.mock import patch, MagicMock
from src.config.firebase_config import init_parameters
from src.auth.firebase_auth import verify_token, get_current_admin

@pytest.fixture
def mock_db():
    with patch('src.config.firebase_config.db') as mock:
        yield mock

def test_init_parameters(mock_db):
    """Test l'initialisation des paramètres Firestore"""
    # Mock du document
    mock_doc = MagicMock()
    mock_doc.exists = False
    mock_db.collection().document().get.return_value = mock_doc
    
    assert init_parameters() == True
    mock_db.collection().document().set.assert_called_once()

@pytest.mark.asyncio
async def test_verify_token():
    """Test la vérification du token"""
    with patch('firebase_admin.auth.verify_id_token') as mock_verify:
        mock_verify.return_value = {'uid': 'test123'}
        mock_creds = MagicMock()
        mock_creds.credentials = "fake_token"
        
        result = await verify_token(mock_creds)
        assert result['uid'] == 'test123'

@pytest.mark.asyncio
async def test_admin_access():
    """Test l'accès admin"""
    with patch('src.auth.firebase_auth.verify_token') as mock_verify:
        mock_verify.return_value = {'uid': 'admin123'}
        with patch('src.config.firebase_config.db') as mock_db:
            # Mock du document admin
            mock_doc = MagicMock()
            mock_doc.exists = True
            mock_doc.to_dict.return_value = {'role': 'admin'}
            mock_db.collection().document().get.return_value = mock_doc
            
            result = await get_current_admin({'uid': 'admin123'})
            assert result['uid'] == 'admin123' 