from app.api.routers.auth import router as auth_router

from fastapi import APIRouter

router = APIRouter()
"""
example:
    router.include_router(xxx, tags=["xxx"], prefix="/xxx")
"""
router.include_router(auth_router, prefix="/auth", tags=["category"])
