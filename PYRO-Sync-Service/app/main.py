"""FastAPI application entrypoint for the Windows Sync Service."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import api_router
from app.config import AppConfig, load_config
from app.db.database import Database
from app.logging_config import setup_logging
from app.services.master_service import MasterDataService
from app.services.order_service import OrderService

logger = logging.getLogger("sync_service")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    config: AppConfig = getattr(app.state, "config", None) or load_config()
    setup_logging(
        level=config.logging.level,
        log_file=config.logging.file,
        log_format=config.logging.format,
    )

    logger.info(f"Starting Windows Sync Service v{__version__}")
    logger.info(f"Active FoxPro fiscal data path: {config.foxpro.data_path}")
    logger.info(f"SQLite state database: {config.database.path}")

    db = Database(config.database.path)
    master_service = MasterDataService(config, db=db)
    order_service = OrderService(db=db, master_service=master_service)

    app.state.config = config
    app.state.db = db
    app.state.master_service = master_service
    app.state.order_service = order_service

    # Verify health at startup
    health = master_service.check_health()
    logger.info(f"Startup table status: {health.status}")
    for tbl_name, tbl_info in health.tables.items():
        if tbl_info.exists:
            logger.info(f"  {tbl_name}: OK ({tbl_info.record_count} records)")
        else:
            logger.warning(f"  {tbl_name}: MISSING ({tbl_info.error})")

    yield

    logger.info("Stopping Windows Sync Service")


def create_app(config: AppConfig = None) -> FastAPI:
    """Factory to create and configure the FastAPI application."""
    if config is None:
        config = load_config()

    app = FastAPI(
        title="PYROJA Windows Sync Service",
        description="Local LAN synchronization and order queueing bridge between Android POS tablets and legacy Visual FoxPro 6.0",
        version=__version__,
        lifespan=lifespan,
    )

    db = Database(config.database.path)
    master_service = MasterDataService(config, db=db)
    order_service = OrderService(db=db, master_service=master_service)

    app.state.config = config
    app.state.db = db
    app.state.master_service = master_service
    app.state.order_service = order_service

    # Enable CORS for tablet local LAN connections
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request duration and audit middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"{client_ip} - {request.method} {request.url.path} [{response.status_code}] ({duration_ms:.1f}ms)")
        return response

    # Include routes
    app.include_router(api_router)

    @app.get("/", tags=["General"])
    async def root_info():
        return {
            "service": "PYROJA FoxPro Sync Service",
            "version": __version__,
            "status": "RUNNING",
            "docs_url": "/docs",
            "health_url": "/api/health",
            "sync_products_url": "/api/sync/products",
            "sync_customers_url": "/api/sync/customers",
            "orders_url": "/api/orders",
            "pending_orders_url": "/api/orders/pending",
        }

    return app


app = create_app()

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    import uvicorn
    cfg = load_config()
    uvicorn.run(
        app,
        host=cfg.server.host,
        port=cfg.server.port,
        reload=False,
    )
