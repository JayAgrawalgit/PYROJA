"""Import and staging management API endpoints."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.exporter import OrderExporter

router = APIRouter(prefix="/api/import", tags=["import"])


class StageRequest(BaseModel):
    user: str = "RAM"
    salesman: str = "SELF"
    output_file: Optional[str] = "import_staging.json"


class StageResponse(BaseModel):
    status: str
    exported_count: int
    output_file: str
    exported_at: str


@router.post("/stage", response_model=StageResponse)
def stage_orders_for_import(req: StageRequest) -> StageResponse:
    """Exports queued orders from SQLite into the FoxPro import_staging.json payload."""
    exporter = OrderExporter()
    payload, count = exporter.export_queued_orders(
        output_file=req.output_file,
        operator_user=req.user,
        salesman_code=req.salesman,
    )
    return StageResponse(
        status="STAGED",
        exported_count=count,
        output_file=req.output_file or "import_staging.json",
        exported_at=payload.get("exported_at", ""),
    )


@router.get("/staging")
def get_current_staging_payload(file_path: str = Query("import_staging.json")) -> Dict[str, Any]:
    """Retrieves current staging JSON payload if it exists."""
    p = Path(file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Staging payload file not found")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read staging payload: {e}")


@router.get("/results")
def get_import_results(file_path: str = Query("import_result.json")) -> Dict[str, Any]:
    """Retrieves execution results from the latest IMPORT.PRG run."""
    p = Path(file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Import result file not found. IMPORT.PRG has not run yet.")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read import results: {e}")
