"""Unit tests for OrderExporter and Staging Payload Generation."""

import json
import os
import sqlite3
from pathlib import Path

import pytest
from app.services.exporter import OrderExporter


@pytest.fixture
def setup_test_env(tmp_path):
    """Creates a temporary SQLite database and mock DBF master directory."""
    db_path = str(tmp_path / "test_sync.sqlite3")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE orders (
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
        )
    """)

    cur.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL REFERENCES orders(order_id),
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
        )
    """)

    # Insert test order
    cur.execute("""
        INSERT INTO orders (
            order_id, draft_id, tablet_id, customer_code, customer_name,
            order_date, subtotal, gst, total, status, remarks, created_at, updated_at
        ) VALUES (
            'ord-101', 'TAB01-9999', 'TAB-01', '01149', 'NEW SHIVA BALAJI DASARWAR',
            '2026-09-07', 2600.0, 0.0, 2600.0, 'QUEUED', 'TEST ORDER',
            '2026-09-07T00:00:00', '2026-09-07T00:00:00'
        )
    """)

    cur.execute("""
        INSERT INTO order_items (
            order_id, line_no, item_code, item_name, pack, qty_in_box,
            qty, rate, tax_percentage, tax_amount, line_total
        ) VALUES
        ('ord-101', 1, '06122', '10CM SPARKLERS', 'BOX', 1, 10.0, 110.0, 0.0, 0.0, 1100.0),
        ('ord-101', 2, '02152', 'RING CAPS', 'PKT', 1, 250.0, 6.0, 0.0, 0.0, 1500.0)
    """)

    conn.commit()
    conn.close()

    # Create dummy FoxPro data dir
    fp_dir = tmp_path / "mock_fp"
    fp_dir.mkdir()

    return db_path, str(fp_dir)


def test_order_exporter_creates_valid_json(setup_test_env, tmp_path):
    db_path, fp_dir = setup_test_env
    output_json = str(tmp_path / "out_staging.json")

    exporter = OrderExporter(db_path=db_path, data_dir=fp_dir)
    payload, count = exporter.export_queued_orders(output_file=output_json)

    assert count == 1
    assert payload["version"] == "1.0"
    assert payload["series"] == "E"
    assert len(payload["orders"]) == 1

    order = payload["orders"][0]
    assert order["draft_id"] == "TAB01-9999"
    assert order["customer_code"] == "01149"
    assert order["net_amount"] == 2600.0
    assert order["note"] == "DRAFT:TAB01-9999"
    assert len(order["items"]) == 2

    # Verify output file on disk
    assert os.path.exists(output_json)
    with open(output_json, "r") as f:
        disk_data = json.load(f)
    assert disk_data["orders"][0]["draft_id"] == "TAB01-9999"


def test_order_exporter_prevents_duplicate_imported(setup_test_env):
    db_path, fp_dir = setup_test_env

    # Mark order as already having legacy entry
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE orders SET legacy_entry_no = 135 WHERE order_id = 'ord-101'")
    conn.commit()
    conn.close()

    exporter = OrderExporter(db_path=db_path, data_dir=fp_dir)
    payload, count = exporter.export_queued_orders()

    assert count == 0
    assert len(payload["orders"]) == 0
