from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.data import process_iris_data, split_iris_data
import pandas as pd

security = HTTPBearer()
router = APIRouter(prefix="/data", tags=["data"])

@router.get("/load")
async def load_dataset():
    """Step 6: Load the Iris dataset"""
    try:
        data = pd.read_csv("src/data/Iris.csv")
        return data.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/process")
async def process_data():
    """Step 7-8: Process the dataset"""
    try:
        data = process_iris_data()
        return data.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/split")
async def split_data():
    """Step 9: Split into train/test"""
    try:
        train, test = split_iris_data()
        return {
            "train": train.to_dict(orient='records'),
            "test": test.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))