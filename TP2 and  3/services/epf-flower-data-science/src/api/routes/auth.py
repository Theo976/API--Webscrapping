from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from src.auth.firebase_auth import get_current_user, get_current_admin
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["authentication"])

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserLogin):
    role: str = "user"

@router.post("/register")
async def register(user: UserRegister):
    """Step 16: User registration"""
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        auth.set_custom_user_claims(user_record.uid, {'role': user.role})
        return {"message": "User registered successfully", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
async def login(user: UserLogin):
    """Login endpoint"""
    try:
        # Récupérer l'utilisateur
        user_record = auth.get_user_by_email(user.email)
        
        # Créer un ID token
        custom_token = auth.create_custom_token(user_record.uid)
        
        # Ajouter les claims (rôle)
        auth.set_custom_user_claims(user_record.uid, {
            'role': 'admin'
        })
        
        # Convertir en string si nécessaire
        if isinstance(custom_token, bytes):
            custom_token = custom_token.decode('utf-8')
        
        return {
            "access_token": custom_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Invalid credentials: {str(e)}"
        )