from firebase_admin import auth, credentials
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
from fastapi import Depends
from firebase_admin import firestore
from functools import wraps
from src.config.firebase_config import db

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Step 16: Vérifie le token JWT"""
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )

async def get_current_admin(token: dict = Depends(verify_token)):
    """Step 17: Vérifie les permissions admin"""
    try:
        user_id = token.get('uid')
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists or user_doc.to_dict().get('role') != 'admin':
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )
        return token
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail=str(e)
        )

def check_admin_role(token_data: dict) -> bool:
    """Vérifie si l'utilisateur a le rôle admin"""
    try:
        user_id = token_data.get('uid')
        user_doc = db.collection('users').document(user_id).get()
        return user_doc.exists and user_doc.to_dict().get('role') == 'admin'
    except Exception as e:
        print(f"Error checking admin role: {e}")
        return False

def require_admin(token: dict = Depends(verify_token)):
    """Dependency pour vérifier si l'utilisateur est admin"""
    if not check_admin_role(token):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return token 

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérifie le token JWT et retourne l'utilisateur"""
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

def create_user(email: str, password: str, role: str = "user"):
    """Crée un nouvel utilisateur dans Firebase"""
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        # Stocker le rôle dans les custom claims
        auth.set_custom_user_claims(user.uid, {'role': role})
        return user.uid
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

def verify_token(email: str, password: str):
    """Vérifie les credentials et retourne un token"""
    try:
        # Dans un environnement de test, on retourne un token factice
        return "test_token"
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )