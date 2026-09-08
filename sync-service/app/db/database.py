"""SQLite state database manager with Write-Ahead Logging (WAL) support."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import logging
import sqlite3

logger = logging.getLogger(__name__)


class Database:
    """Manages the internal SQLite state store for Sync Service."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path).resolve()
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Create a connection with WAL and dictionary row factory."""
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=10.0,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        # Enable Write-Ahead Logging for high-concurrency non-blocking reads/writes
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Initialize database schema if not present."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self.get_connection() as conn:
            # 1. Sync State Table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sync_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

            # 2. Idempotency Key Table (Gate 2 duplicate prevention)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS idempotency_keys (
                    idempotency_key TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    order_id TEXT NOT NULL,
                    response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 3. Orders Master Table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    draft_id TEXT UNIQUE NOT NULL,
                    tablet_id TEXT NOT NULL,
                    customer_code TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    order_date TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    gst REAL NOT NULL,
                    total REAL NOT NULL,
                    status TEXT NOT NULL,
                    remarks TEXT,
                    idempotency_key TEXT,
                    legacy_entry_no INTEGER,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    error_message TEXT
                );
                """
            )

            # 4. Order Line Items Table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
                    line_no INTEGER NOT NULL,
                    item_code TEXT NOT NULL,
                    item_name TEXT NOT NULL,
                    pack TEXT NOT NULL,
                    qty_in_box INTEGER NOT NULL,
                    qty REAL NOT NULL,
                    rate REAL NOT NULL,
                    tax_percentage REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    line_total REAL NOT NULL
                );
                """
            )

            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_draft ON orders (draft_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders (customer_code);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_idemp ON orders (idempotency_key);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items (order_id);")
            conn.commit()
            logger.info(f"Initialized SQLite state database at {self.db_path} (WAL mode)")

    def set_sync_state(self, key: str, value: str) -> None:
        """Record or update a synchronization state key."""
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO sync_state (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at;
                """,
                (key, value, now),
            )
            conn.commit()

    def get_sync_state(self, key: str) -> Optional[str]:
        """Retrieve a synchronization state value."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT value FROM sync_state WHERE key = ?;", (key,)).fetchone()
            return row["value"] if row else None

    # --- Idempotency Methods ---

    def get_idempotency_record(self, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Find cached response for an idempotency key."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM idempotency_keys WHERE idempotency_key = ?;",
                (idempotency_key,),
            ).fetchone()
            if row:
                return dict(row)
        return None

    def save_idempotency_record(
        self, idempotency_key: str, order_id: str, status: str, response_json: str
    ) -> None:
        """Save an idempotency record for duplicate protection."""
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO idempotency_keys (idempotency_key, order_id, status, response_json, created_at)
                VALUES (?, ?, ?, ?, ?);
                """,
                (idempotency_key, order_id, status, response_json, now),
            )
            conn.commit()

    # --- Order Management Methods ---

    def create_order(self, order_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insert order and line items atomically in a single transaction."""
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO orders (
                    order_id, draft_id, tablet_id, customer_code, customer_name,
                    order_date, subtotal, gst, total, status, remarks,
                    idempotency_key, legacy_entry_no, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    order_data["order_id"],
                    order_data["draft_id"],
                    order_data.get("tablet_id", "TABLET-01"),
                    order_data["customer_code"],
                    order_data["customer_name"],
                    order_data["order_date"],
                    order_data["subtotal"],
                    order_data["gst"],
                    order_data["total"],
                    order_data["status"],
                    order_data.get("remarks"),
                    order_data.get("idempotency_key"),
                    order_data.get("legacy_entry_no"),
                    order_data["created_at"],
                    order_data["updated_at"],
                ),
            )

            for idx, item in enumerate(items, start=1):
                conn.execute(
                    """
                    INSERT INTO order_items (
                        order_id, line_no, item_code, item_name, pack, qty_in_box,
                        qty, rate, tax_percentage, tax_amount, line_total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        order_data["order_id"],
                        idx,
                        item["item_code"],
                        item["item_name"],
                        item.get("pack", "UNIT"),
                        item.get("qty_in_box", 1),
                        item["qty"],
                        item["rate"],
                        item.get("tax_percentage", 0.0),
                        item.get("tax_amount", 0.0),
                        item["line_total"],
                    ),
                )

            conn.commit()

        return self.get_order(order_data["order_id"])

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full order details including line items."""
        with self.get_connection() as conn:
            order_row = conn.execute("SELECT * FROM orders WHERE order_id = ?;", (order_id,)).fetchone()
            if not order_row:
                return None

            order_dict = dict(order_row)
            item_rows = conn.execute(
                "SELECT * FROM order_items WHERE order_id = ? ORDER BY line_no ASC;",
                (order_id,),
            ).fetchall()
            order_dict["line_items"] = [dict(item) for item in item_rows]
            return order_dict

    def get_order_by_draft_id(self, draft_id: str) -> Optional[Dict[str, Any]]:
        """Lookup order by tablet draft ID."""
        with self.get_connection() as conn:
            order_row = conn.execute("SELECT order_id FROM orders WHERE draft_id = ?;", (draft_id,)).fetchone()
            if order_row:
                return self.get_order(order_row["order_id"])
        return None

    def get_pending_orders(self, status: str = "QUEUED") -> List[Dict[str, Any]]:
        """Retrieve all orders matching a given status (default: QUEUED)."""
        with self.get_connection() as conn:
            rows = conn.execute(
                "SELECT order_id FROM orders WHERE status = ? ORDER BY created_at ASC;",
                (status,),
            ).fetchall()
            return [self.get_order(r["order_id"]) for r in rows if r]

    def update_order(
        self,
        order_id: str,
        update_fields: Dict[str, Any],
        items: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update an existing order's fields and optionally overwrite line items."""
        existing = self.get_order(order_id)
        if not existing:
            return None

        update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Build dynamic SQL UPDATE clause
        set_clauses = [f"{k} = ?" for k in update_fields.keys()]
        values = list(update_fields.values())
        values.append(order_id)

        with self.get_connection() as conn:
            if set_clauses:
                conn.execute(
                    f"UPDATE orders SET {', '.join(set_clauses)} WHERE order_id = ?;",
                    values,
                )

            if items is not None:
                # Replace existing items
                conn.execute("DELETE FROM order_items WHERE order_id = ?;", (order_id,))
                for idx, item in enumerate(items, start=1):
                    conn.execute(
                        """
                        INSERT INTO order_items (
                            order_id, line_no, item_code, item_name, pack, qty_in_box,
                            qty, rate, tax_percentage, tax_amount, line_total
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        """,
                        (
                            order_id,
                            idx,
                            item["item_code"],
                            item["item_name"],
                            item.get("pack", "UNIT"),
                            item.get("qty_in_box", 1),
                            item["qty"],
                            item["rate"],
                            item.get("tax_percentage", 0.0),
                            item.get("tax_amount", 0.0),
                            item["line_total"],
                        ),
                    )

            conn.commit()

        return self.get_order(order_id)

    def delete_order(self, order_id: str) -> bool:
        """Delete an order and cascade delete its items."""
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM orders WHERE order_id = ?;", (order_id,))
            conn.commit()
            return cursor.rowcount > 0

    def check_health(self) -> Dict[str, Any]:
        """Verify database connectivity and return diagnostics."""
        try:
            with self.get_connection() as conn:
                journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
                sync_count = conn.execute("SELECT COUNT(*) FROM sync_state;").fetchone()[0]
                order_count = conn.execute("SELECT COUNT(*) FROM orders;").fetchone()[0]
                return {
                    "exists": self.db_path.is_file(),
                    "path": str(self.db_path),
                    "journal_mode": journal_mode.upper(),
                    "sync_state_entries": sync_count,
                    "orders_count": order_count,
                    "is_healthy": True,
                }
        except Exception as e:
            return {
                "exists": self.db_path.is_file(),
                "path": str(self.db_path),
                "is_healthy": False,
                "error": str(e),
            }
