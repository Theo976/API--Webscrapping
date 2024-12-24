from fastapi import APIRouter
from src.schemas.message import MessageResponse

router = APIRouter(prefix="/hello", tags=["hello"])

@router.get("/", response_model=MessageResponse)
async def hello():
    """Premier endpoint de test"""
    return MessageResponse(message="Hello, World!")
