from fastapi import APIRouter

from app.api.analytics.endpoints import router as analytics_router
from app.api.auth.endpoints import router as auth_router
from app.api.shortie.endpoints import router as shortie_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(shortie_router, prefix="/shortie", tags=["shortie"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
