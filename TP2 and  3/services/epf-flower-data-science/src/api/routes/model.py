from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.data import train_model, load_trained_model
from src.auth.firebase_auth import get_current_user, get_current_admin
from src.middleware.rate_limiter import limiter
from typing import Dict, Any
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

# Définir le router
security = HTTPBearer()
router = APIRouter(prefix="/model", tags=["model"])

@router.post("/train")
@limiter.limit("5/minute")
async def train_model_endpoint(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: Dict[str, Any] = Depends(get_current_admin)  # Seuls les admins peuvent entraîner
) -> JSONResponse:
    """
    Train model (protected endpoint, admin only)
    
    Rate limit: 5 requests per minute
    """
    try:
        train_model()
        return JSONResponse(
            status_code=200,
            content={"message": "Model trained successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict")
@limiter.limit("10/minute")
async def predict(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    sepal_length: float = Query(...),
    sepal_width: float = Query(...),
    petal_length: float = Query(...),
    petal_width: float = Query(...)
):
    """Make predictions (protected endpoint)"""
    try:
        logger.info("=== Début de la prédiction ===")
        logger.info(f"Token reçu: {credentials.credentials[:50]}...")
        
        model = load_trained_model()
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        logger.info(f"Prédiction réussie: {prediction[0]}")
        
        return JSONResponse(
            status_code=200,
            content={
                "prediction": prediction[0],
                "input_data": {
                    "sepal_length": sepal_length,
                    "sepal_width": sepal_width,
                    "petal_length": petal_length,
                    "petal_width": petal_width
                }
            }
        )
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de prédiction: {str(e)}"
        )