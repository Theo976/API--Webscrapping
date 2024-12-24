from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer
from src.api.router import router
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.middleware.rate_limiter import limiter

security = HTTPBearer()

def get_application() -> FastAPI:
    """Crée et configure l'application FastAPI"""
    app = FastAPI(
        title="Iris Prediction API",
        version="1.0.0",
        description="API for Iris flower prediction",
        openapi_tags=[
            {"name": "authentication", "description": "Authentication operations"},
            {"name": "data", "description": "Data operations"},
            {"name": "model", "description": "Model operations"},
            {"name": "parameters", "description": "Parameters operations"}
        ]
    )
    
    # Rate limiting
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    
    # Router principal
    app.include_router(router)
    
    # Redirection racine vers Swagger
    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs", status_code=307)
    
    # Gestionnaire d'erreurs pour le rate limiting
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "detail": "Too many requests. Try again later.",
                "retry_after": str(exc.retry_after)
            }
        )
    
    # Gestionnaire d'erreurs global
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc)
            }
        )
        
    return app

# Créer l'instance de l'application
app = get_application()
