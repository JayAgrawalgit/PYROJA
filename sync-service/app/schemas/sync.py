"""Pydantic schemas for synchronization endpoints.

Enforces Decision 1 & 2:
- FoxPro ITEMMST.CODE is the ONLY product identifier everywhere.
- No tablet-specific display codes or aliases.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ProductItem(BaseModel):
    code: str = Field(..., description="5-character FoxPro product code from ITEMMST.CODE (the sole product identifier)")
    name: str = Field(..., description="Product description from ITEMMST.NAME")
    company_code: str = Field(..., description="Manufacturer / company code from ITEMMST.CCODE")
    company_name: str = Field(..., description="Resolved company / brand name from COMPMST.NAME")
    group_code: str = Field(..., description="Group code from ITEMMST.GCODE, e.g. 'MIX'")
    group_name: str = Field(..., description="Resolved group category description")
    pack: str = Field(..., description="Packing description from ITEMMST.PACK, e.g. 'PKT', 'BOX'")
    nick: Optional[str] = Field(None, description="Product nickname from ITEMMST.NICK")
    qty_in_box: int = Field(..., description="Inner unit quantity in box/case from ITEMMST.QIB")
    tax_percentage: float = Field(..., description="Tax percentage from TAXMST.TAX")
    tax_code: str = Field(..., description="Tax slab code from ITEMMST.TCODE, e.g. 'T1'")
    rate_type: str = Field(..., description="Rate type flag from ITEMMST.RTTP ('P' = piece, etc.)")
    mrp: float = Field(..., description="Maximum Retail Price from ITEMMST.MRP")
    selling_rate: float = Field(..., description="Selling price per pack/unit from ITEMMST.SRATE")
    purchase_rate: float = Field(..., description="Purchase price from ITEMMST.PRATE")
    stock_on_hand: float = Field(..., description="Current closing quantity stock from ITEMMST.CQTY")
    is_active: bool = Field(True, description="Whether product is active for billing")


class ProductSyncResponse(BaseModel):
    sync_timestamp: str = Field(..., description="ISO 8601 server timestamp")
    active_fiscal_year: str = Field(..., description="Active fiscal year folder, e.g. 'D2627'")
    dbf_checksum: str = Field(..., description="SHA-256 hash of ITEMMST.DBF for delta change detection")
    total_records: int = Field(..., description="Count of returned products")
    is_delta: bool = Field(False, description="Whether payload represents delta changes")
    products: List[ProductItem] = Field(default_factory=list, description="List of product records")


class CustomerItem(BaseModel):
    code: str = Field(..., description="5-character FoxPro account code from NAMEMST.CODE")
    name: str = Field(..., description="Customer / Account name from NAMEMST.NAME")
    city: str = Field(..., description="City or place from NAMEMST.PLACE")
    address_1: str = Field(..., description="Address line 1 from NAMEMST.ADD1")
    address_2: str = Field(..., description="Address line 2 from NAMEMST.ADD2")
    gstin: str = Field(..., description="TIN / CST / GST identification from NAMEMST.TIN or CST")
    phone: str = Field(..., description="Contact phone number from NAMEMST.PH")
    contact_person: Optional[str] = Field(None, description="Contact person name from NAMEMST.CONT")
    area_code: str = Field(..., description="Area code from NAMEMST.ACODE")
    area_name: str = Field(..., description="Resolved area / district name from AREAMST.NAME")
    credit_days: int = Field(..., description="Allowed credit duration in days from NAMEMST.DAY")
    credit_limit: float = Field(..., description="Credit limit amount from NAMEMST.LIMIT")
    current_balance: float = Field(..., description="Current outstanding balance from NAMEMST.CB")
    balance_type: str = Field(..., description="Debit ('D') or Credit ('C') from NAMEMST.DC")
    price_tier: str = Field(..., description="Assigned wholesale pricing tier ('RETAIL' for 99999, else 'WHOLESALE')")


class CustomerSyncResponse(BaseModel):
    sync_timestamp: str = Field(..., description="ISO 8601 server timestamp")
    active_fiscal_year: str = Field(..., description="Active fiscal year folder, e.g. 'D2627'")
    dbf_checksum: str = Field(..., description="SHA-256 hash of NAMEMST.DBF")
    total_records: int = Field(..., description="Count of returned customers")
    is_delta: bool = Field(False, description="Whether payload represents delta changes")
    customers: List[CustomerItem] = Field(default_factory=list, description="List of customer records")
