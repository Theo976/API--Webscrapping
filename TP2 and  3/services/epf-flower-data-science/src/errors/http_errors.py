from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class NotFoundError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)

async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": exc.detail,
            "path": request.url.path
        }
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.detail,
            "path": request.url.path
        }
    ) 