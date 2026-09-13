"""Order Queue to Staging JSON Exporter for Visual FoxPro Ingestion.

Extracts validated orders from SQLite state store, performs master data
denormalization against FoxPro master tables (NAMEMST and ITEMMST), validates
against duplicate import constraints, and outputs import_staging.json for IMPORT.PRG.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.config import load_config
from app.dbf.reader import DBFReader

logger = logging.getLogger("sync_service.exporter")


class OrderExporter:
    """Service to export queued orders into staging payload for FoxPro import."""

    def __init__(self, db_path: Optional[str] = None, data_dir: Optional[str] = None) -> None:
        config = load_config()
        self.db_path = db_path or str(config.database.path)
        self.data_dir = data_dir or str(config.foxpro.data_path)

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _load_customer_areas(self) -> Dict[str, str]:
        """Loads mapping of customer_code -> ACODE from NAMEMST.DBF."""
        path = os.path.join(self.data_dir, "NAMEMST.DBF")
        area_map: Dict[str, str] = {}
        if not os.path.exists(path):
            logger.warning("NAMEMST.DBF not found at %s", path)
            return area_map

        reader = DBFReader(path)
        for rec in reader.iter_records():
            code = str(rec.get("CODE", "")).strip()
            if code:
                acode = str(rec.get("ACODE", "")).strip()
                area_map[code] = acode
        return area_map

    def _load_item_master_details(self) -> Dict[str, Dict[str, Any]]:
        """Loads denormalized classification codes from ITEMMST.DBF."""
        path = os.path.join(self.data_dir, "ITEMMST.DBF")
        item_map: Dict[str, Dict[str, Any]] = {}
        if not os.path.exists(path):
            logger.warning("ITEMMST.DBF not found at %s", path)
            return item_map

        reader = DBFReader(path)
        for rec in reader.iter_records():
            code = str(rec.get("CODE", "")).strip()
            if code:
                item_map[code] = {
                    "gcode": str(rec.get("GCODE", "")).strip() or "MIX",
                    "ccode": str(rec.get("CCODE", "")).strip(),
                    "pack": str(rec.get("PACK", "")).strip() or "PKT",
                    "rttp": str(rec.get("RTTP", "")).strip() or "P",
                    "tcode": str(rec.get("TCODE", "")).strip() or "CST",
                    "tax": float(rec.get("TAX", 0.0) or 0.0),
                }
        return item_map

    def _get_existing_imported_draft_ids(self) -> set[str]:
        """Scans SALEMST.DBF to identify draft IDs already imported into FoxPro."""
        path = os.path.join(self.data_dir, "SALEMST.DBF")
        imported_drafts: set[str] = set()
        if not os.path.exists(path):
            return imported_drafts

        reader = DBFReader(path)
        for rec in reader.iter_records():
            note = str(rec.get("NOTE", "")).strip()
            if note.startswith("DRAFT:"):
                draft_id = note[6:].strip()
                if draft_id:
                    imported_drafts.add(draft_id)
        return imported_drafts

    def export_queued_orders(
        self,
        output_file: Optional[str] = None,
        order_ids: Optional[List[str]] = None,
        operator_user: str = "RAM",
        salesman_code: str = "SELF",
    ) -> Tuple[Dict[str, Any], int]:
        """Fetches queued orders from SQLite, enriches them with DBF masters, and writes staging JSON.

        Returns:
            Tuple of (staging_dict, count_exported)
        """
        customer_areas = self._load_customer_areas()
        item_masters = self._load_item_master_details()
        existing_imported = self._get_existing_imported_draft_ids()

        conn = self._get_connection()
        try:
            cur = conn.cursor()
            if order_ids:
                placeholders = ",".join("?" for _ in order_ids)
                query = f"""
                    SELECT * FROM orders
                    WHERE order_id IN ({placeholders})
                    ORDER BY created_at ASC
                """
                cur.execute(query, order_ids)
            else:
                query = """
                    SELECT * FROM orders
                    WHERE status IN ('QUEUED', 'COMPLETED')
                    AND (legacy_entry_no IS NULL OR legacy_entry_no = 0)
                    ORDER BY created_at ASC
                """
                cur.execute(query)

            order_rows = cur.fetchall()
            staged_orders: List[Dict[str, Any]] = []

            for row in order_rows:
                draft_id = row["draft_id"]

                # Duplicate protection check against FoxPro SALEMST.NOTE
                if draft_id in existing_imported:
                    logger.warning("Order draft %s is already in SALEMST.NOTE! Skipping duplicate.", draft_id)
                    cur.execute(
                        "UPDATE orders SET status = 'IMPORTED', error_message = 'Already present in FoxPro' WHERE order_id = ?",
                        (row["order_id"],),
                    )
                    continue

                # Query line items
                cur.execute(
                    """
                    SELECT * FROM order_items
                    WHERE order_id = ?
                    ORDER BY line_no ASC
                    """,
                    (row["order_id"],),
                )
                item_rows = cur.fetchall()
                if not item_rows:
                    logger.warning("Order %s has no line items. Skipping.", row["order_id"])
                    continue

                # Prepare Date in YYYYMMDD
                raw_date = row["order_date"]
                try:
                    if "-" in raw_date:
                        clean_date = raw_date.replace("-", "")
                    else:
                        clean_date = raw_date
                except Exception:
                    clean_date = datetime.now().strftime("%Y%m%d")

                cust_code = str(row["customer_code"]).strip().zfill(5)
                area_code = customer_areas.get(cust_code, "").ljust(5)

                staged_items: List[Dict[str, Any]] = []
                calc_gross = 0.0

                for item in item_rows:
                    icode = str(item["item_code"]).strip().zfill(5)
                    master = item_masters.get(icode, {})
                    qty = float(item["qty"])
                    rate = float(item["rate"])
                    gross = round(qty * rate, 2)
                    calc_gross += gross

                    gcode = master.get("gcode", "MIX").ljust(5)
                    ccode = master.get("ccode", "").ljust(5)
                    unit = (master.get("pack") or item["pack"] or "PKT").ljust(5)
                    rttp = master.get("rttp", "P")
                    tcode = master.get("tcode", "CST").ljust(5)
                    tax_pct = float(master.get("tax", 0.0))

                    staged_items.append({
                        "line_no": int(item["line_no"]),
                        "item_code": icode,
                        "item_name": str(item["item_name"])[:40],
                        "group_code": gcode,
                        "company_code": ccode,
                        "unit": unit,
                        "rate_type": rttp,
                        "quantity": qty,
                        "rate": rate,
                        "gross_amount": gross,
                        "tax_code": tcode,
                        "tax_percent": tax_pct,
                        "taxable_amount": gross,
                        "tax_amount": 0.0,
                        "net_amount": gross,
                    })

                calc_gross = round(calc_gross, 2)
                subtotal = float(row["subtotal"])
                total = float(row["total"])
                roff = round(total - calc_gross, 2)

                staged_order = {
                    "order_id": row["order_id"],
                    "draft_id": draft_id,
                    "tablet_id": row["tablet_id"],
                    "customer_code": cust_code,
                    "customer_name": str(row["customer_name"])[:40],
                    "order_date": clean_date,
                    "area_code": area_code,
                    "series": "E",
                    "gross_amount": calc_gross,
                    "add_amount": 0.0,
                    "less_amount": 0.0,
                    "round_off": roff,
                    "net_amount": total,
                    "user": operator_user.ljust(10),
                    "salesman": salesman_code.ljust(5),
                    "note": f"DRAFT:{draft_id}",
                    "remarks": (row["remarks"] or "")[:50],
                    "items": staged_items,
                }
                staged_orders.append(staged_order)

            payload = {
                "version": "1.0",
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "environment": os.path.basename(os.path.normpath(self.data_dir)),
                "series": "E",
                "default_user": operator_user,
                "default_salesman": salesman_code,
                "orders": staged_orders,
            }

            conn.commit()

            if output_file:
                out_path = Path(output_file)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2)
                logger.info("Exported %d orders to %s", len(staged_orders), output_file)

            return payload, len(staged_orders)

        finally:
            conn.close()
