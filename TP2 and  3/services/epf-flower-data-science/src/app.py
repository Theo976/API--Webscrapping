from fastapi import FastAPI
from src.api.router import router
from fastapi.responses import RedirectResponse

def get_application():
    app = FastAPI(title="Flower API", version="1.0.0")
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return RedirectResponse(url="/docs", status_code=307)
    
    return app
