"""Pydantic schemas for service health and diagnostics."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class TableHealth(BaseModel):
    name: str = Field(..., description="Table name, e.g. 'ITEMMST.DBF'")
    path: str = Field(..., description="Resolved absolute path")
    exists: bool = Field(..., description="Whether file exists on disk")
    record_count: int = Field(0, description="Header total record count")
    checksum: Optional[str] = Field(None, description="SHA-256 digest")
    last_modified: Optional[str] = Field(None, description="Last modification timestamp")
    error: Optional[str] = Field(None, description="Error message if table could not be read")


class DatabaseHealth(BaseModel):
    exists: bool = Field(..., description="Whether SQLite state database file exists")
    path: str = Field(..., description="Path to SQLite database file")
    journal_mode: Optional[str] = Field(None, description="SQLite journal mode (e.g. 'WAL')")
    is_healthy: bool = Field(..., description="Whether SQLite database is operational")
    error: Optional[str] = Field(None, description="Error if database is unavailable")


class HealthResponse(BaseModel):
    status: str = Field(..., description="'HEALTHY' or 'DEGRADED'")
    version: str = Field(..., description="Sync service software version")
    timestamp: str = Field(..., description="Current server ISO 8601 timestamp")
    active_fiscal_year: str = Field(..., description="Configured fiscal year directory")
    data_path: str = Field(..., description="Configured FoxPro data path")
    database: Optional[DatabaseHealth] = Field(None, description="SQLite state database diagnostics")
    tables: Dict[str, TableHealth] = Field(default_factory=dict, description="Diagnostics per DBF table")
