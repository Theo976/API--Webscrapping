from fastapi import APIRouter, HTTPException
from src.services.parameters import get_parameters, update_parameters

router = APIRouter(prefix="/parameters", tags=["parameters"])

@router.get("/")
async def get_model_parameters():
    """Get model parameters"""
    try:
        return get_parameters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/")
async def update_model_parameters(params: dict):
    """Update model parameters"""
    try:
        return update_parameters(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
