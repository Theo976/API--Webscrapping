from pydantic import BaseModel

class CamelCase(BaseModel):
    class Config:
        populate_by_name = True

class MessageResponse(BaseModel):
    message: str
