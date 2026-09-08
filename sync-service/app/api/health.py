"""Health check and diagnostics API routes."""

from fastapi import APIRouter, Depends, Request
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["Health & Diagnostics"])


@router.get("/health", response_model=HealthResponse, summary="Service health status")
async def get_health(request: Request) -> HealthResponse:
    """Check connectivity to FoxPro DBF tables and report system health."""
    master_service = request.app.state.master_service
    return master_service.check_health()
