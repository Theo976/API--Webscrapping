from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from firebase_admin import auth
from src.auth.firebase_auth import get_current_user, get_current_admin

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
    """Step 16: User login"""
    try:
        user_record = auth.get_user_by_email(user.email)
        custom_token = auth.create_custom_token(user_record.uid)
        return {"access_token": custom_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")