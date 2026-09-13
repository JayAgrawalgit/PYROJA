"""End-to-end integration tests simulating Android tablet client ↔ Sync Service."""

import pytest
from app.main import create_app
from app.schemas.order import OrderStatus
from fastapi.testclient import TestClient


def test_tablet_master_data_bootstrap(test_client):
    """Tablet powers on and downloads product catalog + customer list."""
    # 1. Check health
    health_res = test_client.get("/api/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "HEALTHY"

    # 2. Pull products
    prod_res = test_client.get("/api/sync/products")
    assert prod_res.status_code == 200
    products = prod_res.json()["products"]
    assert len(products) > 1300
    assert not any(p["code"] in ("02083", "02084", "04188", "04189") for p in products)
    assert any(p["code"] == "00013" for p in products)
    assert all("code" in p and "name" in p and "selling_rate" in p for p in products[:20])

    # 3. Pull customers
    cust_res = test_client.get("/api/sync/customers")
    assert cust_res.status_code == 200
    customers = cust_res.json()["customers"]
    assert len(customers) > 800
    assert any(c["code"] == "99999" and c["price_tier"] == "RETAIL" for c in customers)


def test_tablet_offline_order_queue_and_upload(test_client):
    """Simulate tablet creating orders while offline and uploading upon reconnection."""
    # Order 1: Created on showroom floor
    order_payload_1 = {
        "draft_id": "TAB01-OFFLINE-001",
        "tablet_id": "TABLET-01",
        "customer_code": "00688",
        "idempotency_key": "tablet-uuid-offline-001",
        "remarks": "Warehouse Bay 3 Dispatch",
        "line_items": [
            {"item_code": "00013", "qty": 10.0, "rate": 48.0},
            {"item_code": "01989", "qty": 2.0, "rate": 80.0},
        ],
    }

    # Order 2: Created for Cash Counter
    order_payload_2 = {
        "draft_id": "TAB01-OFFLINE-002",
        "tablet_id": "TABLET-01",
        "customer_code": "99999",
        "idempotency_key": "tablet-uuid-offline-002",
        "remarks": "Counter Cash Sale",
        "line_items": [
            {"item_code": "00080", "qty": 5.0, "rate": 55.0},
        ],
    }

    # Batch upload simulation
    res1 = test_client.post("/api/orders", json=order_payload_1)
    assert res1.status_code == 201
    order1 = res1.json()
    assert order1["status"] == OrderStatus.QUEUED.value
    assert order1["draft_id"] == "TAB01-OFFLINE-001"

    res2 = test_client.post("/api/orders", json=order_payload_2)
    assert res2.status_code == 201
    order2 = res2.json()
    assert order2["status"] == OrderStatus.QUEUED.value
    assert order2["customer_code"] == "99999"

    # Verify both exist in pending queue
    pending_res = test_client.get("/api/orders/pending")
    assert pending_res.status_code == 200
    pending_ids = [o["order_id"] for o in pending_res.json()["orders"]]
    assert order1["order_id"] in pending_ids
    assert order2["order_id"] in pending_ids


def test_tablet_reconnection_idempotency_retry(test_client):
    """Simulate tablet WiFi dropping and retrying upload with same Idempotency-Key."""
    idemp_key = "tablet-flaky-wifi-token-777"
    order_payload = {
        "draft_id": "TAB01-FLAKY-001",
        "tablet_id": "TABLET-01",
        "customer_code": "00688",
        "idempotency_key": idemp_key,
        "line_items": [{"item_code": "00013", "qty": 5.0, "rate": 48.0}],
    }

    # First attempt: connection succeeds on server, client drops socket
    res1 = test_client.post("/api/orders", json=order_payload)
    assert res1.status_code == 201
    server_order_id = res1.json()["order_id"]

    # Second attempt: client reconnects and retries with header
    res2 = test_client.post(
        "/api/orders",
        json=order_payload,
        headers={"Idempotency-Key": idemp_key},
    )
    assert res2.status_code == 200  # Idempotent match returns 200 OK
    assert res2.json()["order_id"] == server_order_id
    assert res2.json()["status"] == OrderStatus.QUEUED.value


def test_tablet_order_validation_error_and_correction(test_client):
    """Simulate tablet submitting an order that violates rules, receiving 422, and fixing it."""
    # Attempt 1: Negative quantity
    bad_payload = {
        "draft_id": "TAB01-FIX-001",
        "customer_code": "00688",
        "line_items": [{"item_code": "00013", "qty": -5.0, "rate": 48.0}],
    }
    res_bad = test_client.post("/api/orders", json=bad_payload)
    assert res_bad.status_code == 422

    # Attempt 2: Corrected positive quantity
    good_payload = {
        "draft_id": "TAB01-FIX-001",
        "customer_code": "00688",
        "line_items": [{"item_code": "00013", "qty": 5.0, "rate": 48.0}],
    }
    res_good = test_client.post("/api/orders", json=good_payload)
    assert res_good.status_code == 201
    assert res_good.json()["status"] == OrderStatus.QUEUED.value
