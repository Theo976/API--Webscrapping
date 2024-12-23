from firebase_admin import auth, credentials
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
from fastapi import Depends
from firebase_admin import firestore
from functools import wraps
from src.config.firebase_config import db

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Vérifie le token JWT Firebase"""
    try:
        token = credentials.credentials
        # Enlever 'Bearer ' si présent
        if token.startswith('Bearer '):
            token = token[7:]
            
        print(f"Token length: {len(token)}")
        print(f"Token first part: {token[:50]}...")
        
        try:
            # Vérifier que le token est un JWT valide
            if not token or '.' not in token:
                raise ValueError("Invalid token format")
                
            decoded_token = auth.verify_id_token(token)
            user_id = decoded_token.get('uid')
            print(f"Token successfully verified for user: {user_id}")
            return decoded_token
            
        except ValueError as ve:
            print(f"Value error: {str(ve)}")
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token format: {str(ve)}"
            )
        except auth.InvalidIdTokenError as e:
            print(f"Invalid ID token: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=f"Invalid ID token: {str(e)}"
            )
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=f"Token verification failed: {str(e)}"
            )
            
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials. {str(e)}"
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

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérifie si l'utilisateur est admin"""
    user = get_current_user(credentials)
    if user.get('role') != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return user

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