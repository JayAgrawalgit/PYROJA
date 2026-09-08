"""Order management and queueing endpoints for Phase 2."""

from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Request, Response, status

from app.schemas.order import (
    OrderCreate,
    OrderDeleteResponse,
    OrderListResponse,
    OrderResponse,
    OrderUpdate,
)
from app.services.order_service import OrderNotFoundError, OrderValidationError

router = APIRouter(prefix="/api/orders", tags=["Order Capture & Queueing"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit draft order from tablet",
    description="Validates customer and product codes against FoxPro masters, validates pack multiples, calculates financial totals, and queues order into SQLite.",
)
async def create_order(
    payload: OrderCreate,
    request: Request,
    response: Response,
    idempotency_key_header: Optional[str] = Header(None, alias="Idempotency-Key"),
) -> OrderResponse:
    """Create a new order or return existing order if idempotent submission."""
    order_service = request.app.state.order_service

    # Use header idempotency key if provided and not already in body
    if idempotency_key_header and not payload.idempotency_key:
        payload.idempotency_key = idempotency_key_header

    try:
        order_resp, was_created = order_service.create_order(payload)
        if not was_created:
            # Idempotent match: return 200 OK instead of 201 Created
            response.status_code = status.HTTP_200_OK
        return order_resp
    except OrderValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get(
    "/pending",
    response_model=OrderListResponse,
    summary="List all queued pending orders",
    description="Returns all orders currently in QUEUED status waiting to be imported into FoxPro.",
)
async def get_pending_orders(request: Request) -> OrderListResponse:
    """List all orders waiting in the queue."""
    order_service = request.app.state.order_service
    pending = order_service.get_pending_orders()
    return OrderListResponse(total_records=len(pending), orders=pending)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get order details by ID",
    description="Retrieves full order information including all line items.",
)
async def get_order(order_id: str, request: Request) -> OrderResponse:
    """Retrieve an order by its unique order_id."""
    order_service = request.app.state.order_service
    try:
        return order_service.get_order(order_id)
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order '{order_id}' not found.",
        )


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Update an existing order",
    description="Updates customer, line items, remarks, or status of an existing order in SQLite.",
)
async def update_order(
    order_id: str,
    payload: OrderUpdate,
    request: Request,
) -> OrderResponse:
    """Update order details."""
    order_service = request.app.state.order_service
    try:
        return order_service.update_order(order_id, payload)
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order '{order_id}' not found.",
        )
    except OrderValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.delete(
    "/{order_id}",
    response_model=OrderDeleteResponse,
    summary="Delete / cancel an order",
    description="Removes an order and its associated line items from SQLite.",
)
async def delete_order(order_id: str, request: Request) -> OrderDeleteResponse:
    """Delete an order by ID."""
    order_service = request.app.state.order_service
    try:
        order_service.delete_order(order_id)
        return OrderDeleteResponse(
            success=True,
            message=f"Order '{order_id}' deleted successfully.",
            order_id=order_id,
        )
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order '{order_id}' not found.",
        )
