from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.data import train_model, load_trained_model
from src.auth.firebase_auth import get_current_user, get_current_admin

security = HTTPBearer()
router = APIRouter(prefix="/model", tags=["model"])

@router.post("/train")
async def train_model_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Train model (protected endpoint)"""
    try:
        train_model()
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict")
async def predict(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    sepal_length: float = Query(...),
    sepal_width: float = Query(...),
    petal_length: float = Query(...),
    petal_width: float = Query(...)
):
    """Make predictions (protected endpoint)"""
    try:
        model = load_trained_model()
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))