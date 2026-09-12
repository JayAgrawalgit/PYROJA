# PYROJA ↔ Visual FoxPro 6 Windows Sync Service

High-performance, zero-locking Windows Sync Service connecting **PYROJA** Android tablet POS apps to legacy **Visual FoxPro 6.0** billing systems (`FAVWIN`).

---

## Architectural Decisions Implemented

1. **Single Product Identifier (`ITEMMST.CODE`):** The FoxPro 5-character string `ITEMMST.CODE` (e.g. `"01989"`) is the **only product identifier** used across FoxPro, the Sync Service, and Android tablets.
2. **No Tablet-Specific Display Codes:** Product display codes, aliases, and shortcodes are eliminated. Items are identified directly by `code` and `name`.
3. **Manual Import Trigger Initially:** Invoice import into FoxPro will be executed via manual trigger (`POST /api/import/trigger` / tray app button) once Phase 3 is deployed.
4. **Stock Deduction Only After Invoice Creation:** Tablet stock displays reflect FoxPro's actual closing quantity (`CQTY`). No optimistic inventory deductions occur on draft order creation.
5. **Estimate (`E`) Series Only:** All tablet orders use the Estimate series (`BILLBOOK.CODE == "E "`).
6. **Tablet Draft ID in `SALEMST.NOTE`:** Stored as `"DRAFT:TAB01-1048"` for end-to-end traceability and Gate 4 deduplication.
7. **Python FastAPI Sync Service:** Asynchronous FastAPI server backed by an internal SQLite database in Write-Ahead Logging (WAL) mode.
8. **Autonomous Implementation:** Complete system provided without requiring a FoxPro developer.

---

## Key Features

- **Phase 1: Zero-Locking Master Data Sync:**
  - Pure-Python binary reader decoding FoxPro tables without external C-extensions.
  - Non-locking read access ensuring active billing in `FAVWIN` is never blocked.
  - Full relational joins for brands (`COMPMST.DBF`), tax slabs (`TAXMST.DBF`), and areas (`AREAMST.DBF`).
- **Phase 2: Order Capture & Queueing:**
  - **SQLite-Only Storage:** Orders stored safely in `sync_service.sqlite3` (`orders` and `order_items` tables) operating in WAL mode.
  - **Validation Engine:** Strict pre-flight validation verifying customer exists, products exist, quantities $> 0$, and pack multiple rules (`qty % qty_in_box == 0`).
  - **Multi-Status Lifecycle:** `DRAFT`, `QUEUED`, `COMPLETED`, `FAILED`.
  - **Idempotency Protection:** Double-click and network retry deduplication via `Idempotency-Key` header / field and unique `draft_id`.
  - **Full Order CRUD API:** `POST /api/orders`, `GET /api/orders/{id}`, `GET /api/orders/pending`, `PUT /api/orders/{id}`, `DELETE /api/orders/{id}`.
- **Diagnostics & OpenAPI:**
  - Continuous health reporting via `GET /api/health`.
  - Interactive Swagger UI at `http://localhost:8080/docs`.
  - Exported static OpenAPI specification at [`docs/openapi.json`](docs/openapi.json).
- **Data Safety:** Zero writes or modifications to any FoxPro `.DBF` or `.CDX` files.

---

## Directory Structure

```text
sync-service/
├── .venv/                         # Virtual environment
├── requirements.txt               # Pinned production dependencies
├── config.yaml                    # Service configuration
├── pytest.ini                     # Pytest configuration
├── README.md                      # This manual
├── sync_service.sqlite3           # SQLite state store in WAL mode
├── docs/
│   └── openapi.json               # Exported OpenAPI 3.1.0 specification
├── scripts/
│   ├── start_server.bat           # One-click Windows launch script
│   └── run_tests.bat              # One-click Windows test runner
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application, CORS, and request logging
│   ├── config.py                  # Pydantic Settings & YAML loader
│   ├── logging_config.py          # Structured file and console logging
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py            # SQLite state store (WAL mode, transactions, cascading deletes)
│   ├── dbf/
│   │   ├── __init__.py
│   │   └── reader.py              # Pure-Python binary DBF parser
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── sync.py                # Product & Customer JSON schemas
│   │   ├── order.py               # Order schemas (Create, Update, Response, Line Items)
│   │   └── health.py              # Health check schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── master_service.py      # Master data joins, caching, and health verification
│   │   └── order_service.py       # Order business logic, validations, and calculations
│   └── api/
│       ├── __init__.py
│       ├── health.py              # GET /api/health
│       ├── sync.py                # GET /api/sync/products, GET /api/sync/customers
│       └── orders.py              # Order CRUD & queue endpoints
└── tests/
    ├── __init__.py
    ├── conftest.py                # Pytest fixtures and synthetic DBF generator
    ├── test_dbf_reader.py         # DBF parser unit tests
    ├── test_master_service.py     # Join & cache unit tests
    ├── test_api.py                # Sync API integration tests
    └── test_orders.py             # Order CRUD, validation, and idempotency tests
```

---

## API Reference

### 1. Order Endpoints (Phase 2)

#### `POST /api/orders` — Create & Queue Order
Submits a draft order from an Android tablet. Validates customer code, product codes, quantities ($> 0$), and pack multiples. Calculates `subtotal`, `gst`, and `total`.

- **Headers:** `Idempotency-Key` (optional, recommended: UUIDv4)
- **Request Body:**
  ```json
  {
    "draft_id": "TAB01-1048",
    "tablet_id": "TABLET-01",
    "customer_code": "00688",
    "remarks": "Diwali Advance Consignment",
    "status": "QUEUED",
    "line_items": [
      {
        "item_code": "00013",
        "qty": 10.0,
        "rate": 48.0
      },
      {
        "item_code": "01989",
        "qty": 5.0,
        "rate": 80.0
      }
    ]
  }
  ```
- **Response (`201 Created` / `200 OK` if duplicate idempotency key):**
  ```json
  {
    "order_id": "ORD-20260907-C32B26",
    "draft_id": "TAB01-1048",
    "tablet_id": "TABLET-01",
    "customer_code": "00688",
    "customer_name": "ISMAIL IBRAHIM (HIGHANGHAT) SHUNID BHAI",
    "order_date": "2026-09-07",
    "subtotal": 880.0,
    "gst": 0.0,
    "total": 880.0,
    "status": "QUEUED",
    "remarks": "Diwali Advance Consignment",
    "idempotency_key": null,
    "legacy_entry_no": null,
    "created_at": "2026-09-06T19:35:12.123456+00:00",
    "updated_at": "2026-09-06T19:35:12.123456+00:00",
    "line_items": [
      {
        "item_code": "00013",
        "item_name": "111- ROLL CAPS AGNI",
        "pack": "PKT",
        "qty_in_box": 1,
        "qty": 10.0,
        "rate": 48.0,
        "tax_percentage": 0.0,
        "tax_amount": 0.0,
        "line_total": 480.0
      },
      {
        "item_code": "01989",
        "item_name": "112- ROLL CAPS S.T.D.",
        "pack": "PKT",
        "qty_in_box": 1,
        "qty": 5.0,
        "rate": 80.0,
        "tax_percentage": 0.0,
        "tax_amount": 0.0,
        "line_total": 400.0
      }
    ]
  }
  ```

#### `GET /api/orders/pending` — List Queued Orders
Returns all orders currently in `QUEUED` status waiting for invoice generation.
- **Response (`200 OK`):**
  ```json
  {
    "total_records": 1,
    "orders": [ ... ]
  }
  ```

#### `GET /api/orders/{order_id}` — Get Order Details
Retrieves order details by `order_id`. Returns `404 Not Found` if the order does not exist.

#### `PUT /api/orders/{order_id}` — Update Order
Updates customer, items, remarks, or status of an existing order. Re-validates all business rules and recalculates financial totals.

#### `DELETE /api/orders/{order_id}` — Cancel / Delete Order
Permanently removes the order and cascades delete to all associated line items.

---

### 2. Synchronization Endpoints (Phase 1)
- `GET /api/sync/products` — Full product catalog with stock and prices.
- `GET /api/sync/customers` — Full customer directory with credit limits and balances.
- `GET /api/health` — SQLite and FoxPro table diagnostic status.

---

## Running Tests

Execute the complete test suite:
```bash
.venv/bin/pytest -v
```

All 19 test cases pass covering:
- Master data DBF reading, parsing, and caching.
- Product and customer joins.
- Order creation, price calculation, and tax computation.
- Idempotency protection and duplicate `draft_id` handling.
- Business rule validations (missing customer, missing product, zero quantity, pack multiple violations).
- Order retrieval, pending queue listing, updating, and deleting.
