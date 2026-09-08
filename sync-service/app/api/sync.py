"""Master data synchronization endpoints for Android tablets."""

from fastapi import APIRouter, Query, Request
from app.schemas.sync import CustomerSyncResponse, ProductSyncResponse

router = APIRouter(prefix="/api/sync", tags=["Master Data Synchronization"])


@router.get(
    "/products",
    response_model=ProductSyncResponse,
    summary="Synchronize product catalog",
    description="Returns full catalog of items from ITEMMST.DBF joined with COMPMST and TAXMST.",
)
async def sync_products(
    request: Request,
    force_refresh: bool = Query(False, description="Bypass cache and re-read from disk"),
) -> ProductSyncResponse:
    """Stream active products for tablet catalog display."""
    master_service = request.app.state.master_service
    return master_service.get_products_sync(force_refresh=force_refresh)


@router.get(
    "/customers",
    response_model=CustomerSyncResponse,
    summary="Synchronize customer/party accounts",
    description="Returns active customer accounts from NAMEMST.DBF joined with AREAMST.",
)
async def sync_customers(
    request: Request,
    force_refresh: bool = Query(False, description="Bypass cache and re-read from disk"),
) -> CustomerSyncResponse:
    """Stream active customers for tablet checkout & search."""
    master_service = request.app.state.master_service
    return master_service.get_customers_sync(force_refresh=force_refresh)
