"""Order validation, pricing calculation, and lifecycle management service."""

from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import json
import logging
import uuid

from app.db.database import Database
from app.schemas.order import (
    OrderCreate,
    OrderLineItem,
    OrderResponse,
    OrderStatus,
    OrderUpdate,
)
from app.services.master_service import MasterDataService

logger = logging.getLogger(__name__)


class OrderValidationError(ValueError):
    """Raised when an order fails business validation rules."""
    pass


class OrderNotFoundError(KeyError):
    """Raised when an order is not found by ID."""
    pass


class OrderService:
    """Manages order creation, validation against FoxPro master data, and queueing."""

    def __init__(self, db: Database, master_service: MasterDataService):
        self.db = db
        self.master_service = master_service

    def _generate_order_id(self) -> str:
        """Generate a sequential/chronological order ID."""
        today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        short_id = uuid.uuid4().hex[:6].upper()
        return f"ORD-{today_str}-{short_id}"

    def validate_and_compute_order(
        self,
        customer_code: str,
        customer_name: Optional[str],
        line_items: List[OrderLineItem],
        order_date: Optional[str] = None,
    ) -> Tuple[str, str, List[Dict[str, Any]], float, float, float]:
        """Validate order against FoxPro masters and calculate financial totals.

        Returns:
            (customer_code, customer_name, enriched_items, subtotal, gst, total)
        """
        # 1. Validate Customer Exists
        cust_resp = self.master_service.get_customers_sync()
        cust_map = {c.code: c for c in cust_resp.customers}

        customer_code = str(customer_code).strip()
        if customer_code not in cust_map:
            raise OrderValidationError(
                f"Customer code '{customer_code}' does not exist in FoxPro NAMEMST master."
            )

        matched_customer = cust_map[customer_code]
        resolved_customer_name = customer_name or matched_customer.name

        # 2. Validate Products & Pack Multiples
        prod_resp = self.master_service.get_products_sync()
        prod_map = {p.code: p for p in prod_resp.products}

        if not line_items:
            raise OrderValidationError("Order must contain at least one line item.")

        enriched_items: List[Dict[str, Any]] = []
        subtotal = 0.0
        gst_total = 0.0

        for idx, item in enumerate(line_items, start=1):
            item_code = str(item.item_code).strip()
            if item_code not in prod_map:
                raise OrderValidationError(
                    f"Line {idx}: Product code '{item_code}' does not exist in FoxPro ITEMMST master."
                )

            master_product = prod_map[item_code]

            # Quantity validation
            if item.qty <= 0:
                raise OrderValidationError(
                    f"Line {idx}: Quantity for item '{item_code}' must be greater than 0 (got {item.qty})."
                )

            # Pack multiple validation rule (strictly enforced on wholesale accounts, bypassed for retail Cash A/C 99999)
            is_wholesale = matched_customer.code != "99999" and matched_customer.price_tier.upper() != "RETAIL"
            qib = master_product.qty_in_box
            if is_wholesale and qib and qib > 1:
                # Modulo with floating point tolerance
                remainder = item.qty % qib
                if abs(remainder) > 1e-4 and abs(remainder - qib) > 1e-4:
                    raise OrderValidationError(
                        f"Line {idx}: Pack multiple rule violation for item '{item_code}' ({master_product.name}). "
                        f"Units per box is {qib} ({master_product.pack}). Requested quantity {item.qty} must be a multiple of {qib}."
                    )

            # Auto-resolve fields if not explicitly specified
            item_name = item.item_name or master_product.name
            pack = item.pack or master_product.pack
            rate = item.rate if item.rate is not None and item.rate > 0 else master_product.selling_rate
            tax_pct = item.tax_percentage if item.tax_percentage is not None else master_product.tax_percentage

            line_taxable = round(item.qty * rate, 2)
            line_tax = round(line_taxable * (tax_pct / 100.0), 2)
            line_total = round(line_taxable + line_tax, 2)

            subtotal += line_taxable
            gst_total += line_tax

            enriched_items.append(
                {
                    "item_code": item_code,
                    "item_name": item_name,
                    "pack": pack,
                    "qty_in_box": qib or 1,
                    "qty": item.qty,
                    "rate": rate,
                    "tax_percentage": tax_pct,
                    "tax_amount": line_tax,
                    "line_total": line_total,
                }
            )

        subtotal = round(subtotal, 2)
        gst_total = round(gst_total, 2)
        total = round(subtotal + gst_total, 2)

        return (
            customer_code,
            resolved_customer_name,
            enriched_items,
            subtotal,
            gst_total,
            total,
        )

    def create_order(self, payload: OrderCreate) -> Tuple[OrderResponse, bool]:
        """Create a new order in SQLite with idempotency check.

        Returns:
            (OrderResponse, was_created: bool)
        """
        # Idempotency check: if key provided and already processed, return stored order
        if payload.idempotency_key:
            existing_idemp = self.db.get_idempotency_record(payload.idempotency_key)
            if existing_idemp:
                logger.info(f"Idempotent hit for key: {payload.idempotency_key} -> Order {existing_idemp['order_id']}")
                existing_order = self.db.get_order(existing_idemp["order_id"])
                if existing_order:
                    return OrderResponse(**existing_order), False

        # Draft ID check: draft_id must be unique across orders
        existing_draft = self.db.get_order_by_draft_id(payload.draft_id)
        if existing_draft:
            logger.info(f"Duplicate draft_id submitted: {payload.draft_id} -> returning existing order {existing_draft['order_id']}")
            return OrderResponse(**existing_draft), False

        # Validate master data, quantities, and calculate totals
        (
            cust_code,
            cust_name,
            enriched_items,
            subtotal,
            gst,
            total,
        ) = self.validate_and_compute_order(
            customer_code=payload.customer_code,
            customer_name=payload.customer_name,
            line_items=payload.line_items,
            order_date=payload.order_date,
        )

        now = datetime.now(timezone.utc).isoformat()
        order_id = self._generate_order_id()
        order_date_val = payload.order_date or date.today().isoformat()
        status_val = (payload.status or OrderStatus.QUEUED).value

        order_data = {
            "order_id": order_id,
            "draft_id": payload.draft_id,
            "tablet_id": payload.tablet_id or "TABLET-01",
            "customer_code": cust_code,
            "customer_name": cust_name,
            "order_date": order_date_val,
            "subtotal": subtotal,
            "gst": gst,
            "total": total,
            "status": status_val,
            "remarks": payload.remarks,
            "idempotency_key": payload.idempotency_key,
            "legacy_entry_no": None,
            "created_at": now,
            "updated_at": now,
        }

        created_order_dict = self.db.create_order(order_data, enriched_items)
        response = OrderResponse(**created_order_dict)

        # Record idempotency key if provided
        if payload.idempotency_key:
            self.db.save_idempotency_record(
                idempotency_key=payload.idempotency_key,
                order_id=order_id,
                status=status_val,
                response_json=response.model_dump_json(),
            )

        logger.info(f"Successfully created order {order_id} (Draft: {payload.draft_id}, Total: ₹{total})")
        return response, True

    def get_order(self, order_id: str) -> OrderResponse:
        """Retrieve order by order_id."""
        order_dict = self.db.get_order(order_id)
        if not order_dict:
            raise OrderNotFoundError(f"Order '{order_id}' not found.")
        return OrderResponse(**order_dict)

    def get_pending_orders(self) -> List[OrderResponse]:
        """Retrieve all orders in QUEUED status waiting for import."""
        orders_list = self.db.get_pending_orders(status=OrderStatus.QUEUED.value)
        return [OrderResponse(**o) for o in orders_list]

    def update_order(self, order_id: str, payload: OrderUpdate) -> OrderResponse:
        """Update an existing order with re-validation if line items or customer changed."""
        existing = self.db.get_order(order_id)
        if not existing:
            raise OrderNotFoundError(f"Order '{order_id}' not found.")

        update_fields: Dict[str, Any] = {}
        enriched_items: Optional[List[Dict[str, Any]]] = None

        target_customer = payload.customer_code or existing["customer_code"]
        target_name = payload.customer_name or existing["customer_name"]

        # If items or customer changed, recompute totals
        if payload.line_items is not None or payload.customer_code is not None:
            items_to_validate = (
                payload.line_items
                if payload.line_items is not None
                else [OrderLineItem(**it) for it in existing["line_items"]]
            )

            (
                cust_code,
                cust_name,
                enriched_items,
                subtotal,
                gst,
                total,
            ) = self.validate_and_compute_order(
                customer_code=target_customer,
                customer_name=target_name,
                line_items=items_to_validate,
            )

            update_fields["customer_code"] = cust_code
            update_fields["customer_name"] = cust_name
            update_fields["subtotal"] = subtotal
            update_fields["gst"] = gst
            update_fields["total"] = total
        else:
            if payload.customer_name is not None:
                update_fields["customer_name"] = payload.customer_name

        if payload.remarks is not None:
            update_fields["remarks"] = payload.remarks

        if payload.status is not None:
            update_fields["status"] = payload.status.value

        updated_dict = self.db.update_order(order_id, update_fields, items=enriched_items)
        logger.info(f"Successfully updated order {order_id}")
        return OrderResponse(**updated_dict)

    def delete_order(self, order_id: str) -> bool:
        """Delete an order from SQLite."""
        existing = self.db.get_order(order_id)
        if not existing:
            raise OrderNotFoundError(f"Order '{order_id}' not found.")

        deleted = self.db.delete_order(order_id)
        logger.info(f"Deleted order {order_id}")
        return deleted
