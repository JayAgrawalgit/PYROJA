"""Pydantic schemas for Phase 2: Order Capture & Queueing."""

from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    QUEUED = "QUEUED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OrderLineItem(BaseModel):
    item_code: str = Field(..., description="5-character FoxPro product code from ITEMMST.CODE")
    item_name: Optional[str] = Field(None, description="Product description (auto-resolved if omitted)")
    pack: Optional[str] = Field(None, description="Packing description, e.g. 'PKT', 'BOX'")
    qty_in_box: Optional[int] = Field(None, description="Units per box/case from ITEMMST.QIB")
    qty: float = Field(..., gt=0, description="Quantity ordered (must be greater than 0)")
    rate: float = Field(..., ge=0, description="Selling price per unit/pack")
    tax_percentage: Optional[float] = Field(None, description="GST rate percentage (auto-resolved if omitted)")
    tax_amount: Optional[float] = Field(None, description="Computed GST amount")
    line_total: Optional[float] = Field(None, description="Gross/net line total")


class OrderBase(BaseModel):
    draft_id: str = Field(..., min_length=1, description="Unique tablet draft identifier, e.g. 'TAB01-1048'")
    tablet_id: Optional[str] = Field("TABLET-01", description="Identifier of submitting POS tablet")
    customer_code: str = Field(..., description="5-character FoxPro account code from NAMEMST.CODE")
    customer_name: Optional[str] = Field(None, description="Customer name (auto-resolved if omitted)")
    order_date: Optional[str] = Field(None, description="Order date YYYY-MM-DD (defaults to today)")
    remarks: Optional[str] = Field(None, description="Order notes / dispatch remarks")
    status: Optional[OrderStatus] = Field(OrderStatus.QUEUED, description="Initial order status (QUEUED or DRAFT)")
    line_items: List[OrderLineItem] = Field(..., min_length=1, description="List of items in order")


class OrderCreate(OrderBase):
    idempotency_key: Optional[str] = Field(None, description="Unique UUID/token to prevent duplicate submissions")


class OrderUpdate(BaseModel):
    customer_code: Optional[str] = Field(None, description="Updated customer code")
    customer_name: Optional[str] = Field(None, description="Updated customer name")
    remarks: Optional[str] = Field(None, description="Updated order notes")
    status: Optional[OrderStatus] = Field(None, description="Updated status")
    line_items: Optional[List[OrderLineItem]] = Field(None, min_length=1, description="Updated list of items")


class OrderResponse(BaseModel):
    order_id: str = Field(..., description="Unique generated order ID, e.g. 'ORD-20260907-001'")
    draft_id: str = Field(..., description="Tablet draft ID, e.g. 'TAB01-1048'")
    tablet_id: str = Field(..., description="Submitting tablet ID")
    customer_code: str = Field(..., description="FoxPro customer code")
    customer_name: str = Field(..., description="Customer name")
    order_date: str = Field(..., description="Order date (YYYY-MM-DD)")
    subtotal: float = Field(..., description="Taxable line items sum")
    gst: float = Field(..., description="Total GST amount")
    total: float = Field(..., description="Grand total payable")
    status: OrderStatus = Field(..., description="Current lifecycle status")
    remarks: Optional[str] = Field(None, description="Order remarks")
    idempotency_key: Optional[str] = Field(None, description="Idempotency key")
    legacy_entry_no: Optional[int] = Field(None, description="Allocated FoxPro invoice # when completed")
    created_at: str = Field(..., description="Creation ISO 8601 timestamp")
    updated_at: str = Field(..., description="Last update ISO 8601 timestamp")
    line_items: List[OrderLineItem] = Field(..., description="Detailed line items")


class OrderListResponse(BaseModel):
    total_records: int = Field(..., description="Number of orders returned")
    orders: List[OrderResponse] = Field(default_factory=list, description="List of order records")


class OrderDeleteResponse(BaseModel):
    success: bool = True
    message: str
    order_id: str
