from app.api.routers.auth import router as auth_router
from app.api.routers.books import router as books_router
from app.api.routers.cart import router as cart_router
from app.api.routers.order import router as order_router

from fastapi import APIRouter

router = APIRouter()
"""
example:
    router.include_router(xxx, tags=["xxx"], prefix="/xxx")
"""
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(books_router, prefix="/books", tags=["books"])
router.include_router(cart_router, prefix="/cart", tags=["cart"])
router.include_router(order_router, prefix="/order", tags=["order"])
