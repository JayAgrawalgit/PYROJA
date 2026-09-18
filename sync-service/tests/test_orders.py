"""Unit and integration tests for Phase 2: Order Capture & Queueing."""

import pytest
from app.config import AppConfig, CacheConfig, DatabaseConfig, FoxproConfig
from app.db.database import Database
from app.main import create_app
from app.schemas.order import OrderStatus
from fastapi.testclient import TestClient
from tests.conftest import create_synthetic_dbf


def test_create_valid_order(test_client):
    payload = {
        "draft_id": "TAB01-DRAFT-101",
        "tablet_id": "TABLET-01",
        "customer_code": "00688",
        "remarks": "Diwali Advance Delivery",
        "line_items": [
            {"item_code": "00013", "qty": 10.0, "rate": 48.0},
            {"item_code": "01989", "qty": 5.0, "rate": 80.0},
        ],
    }
    response = test_client.post("/api/orders", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["draft_id"] == "TAB01-DRAFT-101"
    assert data["customer_code"] == "00688"
    assert "ISMAIL IBRAHIM" in data["customer_name"]
    assert data["status"] == OrderStatus.QUEUED.value
    assert len(data["line_items"]) == 2

    # Verify calculation:
    # 00013: 10 * 48 = 480.0
    # 01989: 5 * 80 = 400.0
    # Subtotal = 880.0
    assert data["subtotal"] == 880.0
    assert data["total"] >= 880.0


def test_idempotency_protection(test_client):
    idempotency_token = "idemp-uuid-unique-999"
    payload = {
        "draft_id": "TAB01-DRAFT-102",
        "tablet_id": "TABLET-01",
        "customer_code": "00688",
        "idempotency_key": idempotency_token,
        "line_items": [{"item_code": "00013", "qty": 2.0, "rate": 48.0}],
    }

    # First request: 201 Created
    res1 = test_client.post("/api/orders", json=payload)
    assert res1.status_code == 201
    order_id_1 = res1.json()["order_id"]

    # Second request with exact same idempotency key: 200 OK, same order_id
    res2 = test_client.post(
        "/api/orders",
        json=payload,
        headers={"Idempotency-Key": idempotency_token},
    )
    assert res2.status_code == 200
    order_id_2 = res2.json()["order_id"]
    assert order_id_1 == order_id_2


def test_duplicate_draft_id_protection(test_client):
    payload = {
        "draft_id": "TAB01-DRAFT-103",
        "customer_code": "00688",
        "line_items": [{"item_code": "00013", "qty": 1.0, "rate": 48.0}],
    }
    res1 = test_client.post("/api/orders", json=payload)
    assert res1.status_code == 201

    # Second attempt with same draft_id: returns existing order
    res2 = test_client.post("/api/orders", json=payload)
    assert res2.status_code == 200
    assert res2.json()["order_id"] == res1.json()["order_id"]


def test_invalid_customer_rejected(test_client):
    payload = {
        "draft_id": "TAB01-DRAFT-104",
        "customer_code": "INVALID_CUST",
        "line_items": [{"item_code": "00013", "qty": 5.0, "rate": 48.0}],
    }
    response = test_client.post("/api/orders", json=payload)
    assert response.status_code == 422
    assert "does not exist in FoxPro NAMEMST master" in response.json()["detail"]


def test_invalid_product_rejected(test_client):
    payload = {
        "draft_id": "TAB01-DRAFT-105",
        "customer_code": "00688",
        "line_items": [{"item_code": "INVALID_ITEM", "qty": 5.0, "rate": 48.0}],
    }
    response = test_client.post("/api/orders", json=payload)
    assert response.status_code == 422
    assert "does not exist in FoxPro ITEMMST master" in response.json()["detail"]


def test_quantity_zero_or_negative_rejected(test_client):
    payload_zero = {
        "draft_id": "TAB01-DRAFT-106A",
        "customer_code": "00688",
        "line_items": [{"item_code": "00013", "qty": 0.0, "rate": 48.0}],
    }
    res_zero = test_client.post("/api/orders", json=payload_zero)
    assert res_zero.status_code == 422

    payload_neg = {
        "draft_id": "TAB01-DRAFT-106B",
        "customer_code": "00688",
        "line_items": [{"item_code": "00013", "qty": -10.0, "rate": 48.0}],
    }
    res_neg = test_client.post("/api/orders", json=payload_neg)
    assert res_neg.status_code == 422


def test_pack_multiple_rule_enforcement(temp_dbf_dir):
    """Test pack multiple validation using synthetic DBFs with QIB = 10."""
    # 1. Create ITEMMST with QIB = 10
    create_synthetic_dbf(
        temp_dbf_dir / "ITEMMST.DBF",
        [
            ("CODE", "C", 5, 0),
            ("CCODE", "C", 5, 0),
            ("GCODE", "C", 5, 0),
            ("NAME", "C", 30, 0),
            ("PACK", "C", 10, 0),
            ("NICK", "C", 10, 0),
            ("QIB", "N", 5, 0),
            ("TAX", "N", 5, 2),
            ("TCODE", "C", 5, 0),
            ("RTTP", "C", 1, 0),
            ("MRP", "N", 11, 2),
            ("SRATE", "N", 10, 2),
            ("PRATE", "N", 11, 2),
            ("CQTY", "N", 11, 2),
        ],
        [
            {
                "CODE": "90001",
                "CCODE": "1",
                "GCODE": "SPK",
                "NAME": "SUPER ROCKET 10PCS",
                "PACK": "BOX",
                "NICK": "***",
                "QIB": 10,  # Pack size 10
                "TAX": 0.0,
                "TCODE": "T1",
                "RTTP": "P",
                "MRP": 100.0,
                "SRATE": 85.0,
                "PRATE": 60.0,
                "CQTY": 500.0,
            }
        ],
    )

    # 2. Create NAMEMST, COMPMST, TAXMST, AREAMST
    create_synthetic_dbf(
        temp_dbf_dir / "NAMEMST.DBF",
        [("CODE", "C", 5, 0), ("NAME", "C", 30, 0)],
        [
            {"CODE": "C0001", "NAME": "TEST WHOLESALE CUSTOMER"},
            {"CODE": "99999", "NAME": "CASH A/C"},
        ],
    )
    create_synthetic_dbf(temp_dbf_dir / "COMPMST.DBF", [("CODE", "C", 5, 0), ("NAME", "C", 20, 0)], [])
    create_synthetic_dbf(temp_dbf_dir / "TAXMST.DBF", [("CODE", "C", 5, 0), ("SLAB", "C", 20, 0), ("TAX", "N", 5, 2)], [])
    create_synthetic_dbf(temp_dbf_dir / "AREAMST.DBF", [("CODE", "C", 5, 0), ("NAME", "C", 20, 0)], [])

    db_file = temp_dbf_dir / "test_orders.sqlite3"
    cfg = AppConfig(
        foxpro=FoxproConfig(data_path=temp_dbf_dir, active_fiscal_year="SYNTHETIC"),
        database=DatabaseConfig(path=db_file),
        cache=CacheConfig(ttl_seconds=10, validate_mtime=True),
    )
    app = create_app(cfg)
    client = TestClient(app)

    # Case A: Wholesale Customer + Qty = 20 (Multiple of 10) -> Should succeed
    res_valid = client.post(
        "/api/orders",
        json={
            "draft_id": "DRAFT-QIB-01",
            "customer_code": "C0001",
            "line_items": [{"item_code": "90001", "qty": 20.0, "rate": 85.0}],
        },
    )
    assert res_valid.status_code == 201

    # Case B: Wholesale Customer + Qty = 15 (NOT a multiple of 10) -> Must fail with 422
    res_invalid = client.post(
        "/api/orders",
        json={
            "draft_id": "DRAFT-QIB-02",
            "customer_code": "C0001",
            "line_items": [{"item_code": "90001", "qty": 15.0, "rate": 85.0}],
        },
    )
    assert res_invalid.status_code == 422
    detail = res_invalid.json()["detail"]
    assert "Pack multiple rule violation" in detail
    assert "must be a multiple of 10" in detail

    # Case C: Cash Customer 99999 + Qty = 15 (Non-multiple) -> Must SUCCEED (Retail bypass)
    res_cash_15 = client.post(
        "/api/orders",
        json={
            "draft_id": "DRAFT-CASH-15",
            "customer_code": "99999",
            "line_items": [{"item_code": "90001", "qty": 15.0, "rate": 85.0}],
        },
    )
    assert res_cash_15.status_code == 201

    # Case D: Cash Customer 99999 + Qty = 1 (Single unit loose purchase) -> Must SUCCEED
    res_cash_1 = client.post(
        "/api/orders",
        json={
            "draft_id": "DRAFT-CASH-01",
            "customer_code": "99999",
            "line_items": [{"item_code": "90001", "qty": 1.0, "rate": 85.0}],
        },
    )
    assert res_cash_1.status_code == 201


def test_get_order_and_pending_orders(test_client):
    # Create order
    res = test_client.post(
        "/api/orders",
        json={
            "draft_id": "TAB01-DRAFT-107",
            "customer_code": "00688",
            "line_items": [{"item_code": "00013", "qty": 5.0, "rate": 48.0}],
        },
    )
    assert res.status_code == 201
    order_id = res.json()["order_id"]

    # Test GET by ID
    get_res = test_client.get(f"/api/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json()["order_id"] == order_id

    # Test GET non-existent
    not_found_res = test_client.get("/api/orders/ORD-NONEXISTENT")
    assert not_found_res.status_code == 404

    # Test GET pending
    pending_res = test_client.get("/api/orders/pending")
    assert pending_res.status_code == 200
    order_ids = [o["order_id"] for o in pending_res.json()["orders"]]
    assert order_id in order_ids


def test_update_order(test_client):
    # Create order
    res = test_client.post(
        "/api/orders",
        json={
            "draft_id": "TAB01-DRAFT-108",
            "customer_code": "00688",
            "line_items": [{"item_code": "00013", "qty": 2.0, "rate": 48.0}],
        },
    )
    order_id = res.json()["order_id"]

    # Update remarks and items
    update_res = test_client.put(
        f"/api/orders/{order_id}",
        json={
            "remarks": "Express Dispatch",
            "line_items": [{"item_code": "00013", "qty": 4.0, "rate": 48.0}],
        },
    )
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["remarks"] == "Express Dispatch"
    assert updated_data["subtotal"] == 4.0 * 48.0

    # PUT non-existent order
    bad_put = test_client.put("/api/orders/ORD-NONEXISTENT", json={"remarks": "test"})
    assert bad_put.status_code == 404


def test_delete_order(test_client):
    # Create order
    res = test_client.post(
        "/api/orders",
        json={
            "draft_id": "TAB01-DRAFT-109",
            "customer_code": "00688",
            "line_items": [{"item_code": "00013", "qty": 1.0, "rate": 48.0}],
        },
    )
    order_id = res.json()["order_id"]

    # Delete order
    del_res = test_client.delete(f"/api/orders/{order_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Subsequent GET returns 404
    get_res = test_client.get(f"/api/orders/{order_id}")
    assert get_res.status_code == 404

    # Delete again returns 404
    del_again = test_client.delete(f"/api/orders/{order_id}")
    assert del_again.status_code == 404
