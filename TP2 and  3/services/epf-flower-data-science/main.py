from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from src.app import get_application
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.middleware.rate_limiter import limiter
from src.errors.http_errors import (
    NotFoundError,
    ValidationError,
    not_found_error_handler,
    validation_error_handler
)

app = get_application()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too Many Requests",
            "detail": "Rate limit exceeded. Please try again later.",
            "path": request.url.path
        }
    )

# Custom error handlers
app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)

# Default 404 handler
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found",
            "path": request.url.path
        }
    )

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=307)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)