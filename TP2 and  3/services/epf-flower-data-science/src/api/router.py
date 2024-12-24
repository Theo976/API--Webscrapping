from fastapi import APIRouter
from src.api.routes import data, hello, parameters, model, auth
from src.config.api_config import API_PREFIX

router = APIRouter(prefix=API_PREFIX)

# Inclusion des routers avec les bons préfixes
router.include_router(hello.router, prefix="/hello")
router.include_router(data.router, prefix="/data")
router.include_router(model.router, prefix="/model")
router.include_router(parameters.router, prefix="/parameters")
router.include_router(auth.router, prefix="/auth")