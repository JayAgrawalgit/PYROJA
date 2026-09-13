"""API package router registration."""

from fastapi import APIRouter
from .health import router as health_router
from .sync import router as sync_router
from .orders import router as orders_router
from .import_api import router as import_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(sync_router)
api_router.include_router(orders_router)
api_router.include_router(import_router)

__all__ = ["api_router"]
