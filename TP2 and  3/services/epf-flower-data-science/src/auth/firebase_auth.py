from firebase_admin import auth, credentials
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
from fastapi import Depends
from firebase_admin import firestore
from functools import wraps
from src.config.firebase_config import db
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Vérifie le token JWT Firebase"""
    try:
        token = credentials.credentials
        if token.startswith('Bearer '):
            token = token[7:]
        
        logger.info("=== Début de la vérification du token ===")
        logger.info(f"Token reçu (50 premiers caractères): {token[:50]}")
        
        try:
            # Vérifier le token
            logger.info("Tentative de vérification avec verify_id_token...")
            decoded_token = auth.verify_id_token(token)
            logger.info(f"Token vérifié avec succès pour l'utilisateur: {decoded_token.get('uid')}")
            logger.info(f"Claims du token: {decoded_token}")
            return decoded_token
            
        except auth.InvalidIdTokenError as e:
            logger.error(f"Token invalide (InvalidIdTokenError): {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=f"Token invalide (InvalidIdTokenError): {str(e)}"
            )
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la vérification: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=f"Erreur de vérification: {str(e)}"
            )
                
    except Exception as e:
        logger.error(f"Erreur générale: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Erreur générale: {str(e)}"
        )

def verify_credentials(email: str, password: str):
    """Vérifie les credentials et retourne un token"""
    try:
        user = auth.get_user_by_email(email)
        # Dans un cas réel, vérifiez le mot de passe avec Firebase
        return auth.create_custom_token(user.uid)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Récupère l'utilisateur courant"""
    token = await verify_firebase_token(credentials)
    return token

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Vérifie si l'utilisateur est admin"""
    token = await verify_firebase_token(credentials)
    if token.get('role') != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return token

def check_admin_role(token_data: dict) -> bool:
    """Vérifie si l'utilisateur a le rôle admin"""
    try:
        user_id = token_data.get('uid')
        user_doc = db.collection('users').document(user_id).get()
        return user_doc.exists and user_doc.to_dict().get('role') == 'admin'
    except Exception as e:
        print(f"Error checking admin role: {e}")
        return False

def require_admin(token: dict = Depends(verify_firebase_token)):
    """Dependency pour vérifier si l'utilisateur est admin"""
    if not check_admin_role(token):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return token 

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