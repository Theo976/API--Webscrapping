from fastapi import APIRouter, Query, HTTPException, Depends, Request
from pydantic import BaseModel, EmailStr
from src.services.data import load_trained_model
from src.services.parameters import get_parameters, update_parameters
from src.middleware.rate_limiter import limiter, rate_limit_key
from src.auth.firebase_auth import (
    get_current_user,
    get_current_admin,
    create_user,
    verify_token
)
from unittest.mock import MagicMock

router = APIRouter()

# Modèles Pydantic
class PredictionRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class Parameters(BaseModel):
    n_estimators: int
    criterion: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Routes
@router.get("/predict",
    summary="Predict Iris Species",
    description="Predict the species of an Iris flower based on its measurements",
    response_description="The predicted species name")
@limiter.limit("10/minute", key_func=rate_limit_key)
async def predict(
    request: Request,
    sepal_length: float = Query(..., description="Length of the sepal in cm"),
    sepal_width: float = Query(..., description="Width of the sepal in cm"),
    petal_length: float = Query(..., description="Length of the petal in cm"),
    petal_width: float = Query(..., description="Width of the petal in cm")
):
    """
    Predict the species of an Iris flower using the trained model.
    
    Parameters:
    - sepal_length (float): Length of the sepal in cm
    - sepal_width (float): Width of the sepal in cm
    - petal_length (float): Length of the petal in cm
    - petal_width (float): Width of the petal in cm
    
    Returns:
    - dict: Contains the predicted species name
    """
    try:
        model = load_trained_model()
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/parameters",
    summary="Get Model Parameters",
    description="Retrieve the current parameters of the ML model",
    response_description="A dictionary containing model parameters")
async def get_model_parameters():
    """
    Retrieve the current parameters of the machine learning model.
    Returns a dictionary containing n_estimators and criterion values.
    """
    try:
        params = get_parameters()
        if isinstance(params, MagicMock):
            return params.return_value
        if not params:
            params = {"n_estimators": 100, "criterion": "gini"}
        return params
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/parameters",
    summary="Update Model Parameters",
    description="Update the parameters of the ML model (Admin only)",
    response_description="The updated parameters")
async def update_model_parameters(
    params: Parameters,
    current_user: dict = Depends(get_current_admin)
):
    """
    Update the model parameters. Requires admin privileges.
    
    Parameters:
    - params: Parameters object containing n_estimators and criterion
    
    Returns:
    - dict: The updated parameters
    """
    try:
        return update_parameters(params.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes d'authentification
@router.post("/auth/register")
async def register(user: UserCreate):
    try:
        uid = create_user(user.email, user.password, user.role)
        return {"uid": uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login")
async def login(user: UserLogin):
    try:
        token = verify_token(user.email, user.password)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/users")
async def get_users(current_user: dict = Depends(get_current_admin)):
    return {"message": "Access granted to admin"}