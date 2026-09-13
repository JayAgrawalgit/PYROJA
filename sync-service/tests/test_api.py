"""Integration tests for FastAPI endpoints."""

def test_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "PYROJA FoxPro Sync Service"
    assert data["status"] == "RUNNING"
    assert "health_url" in data


def test_health_endpoint(test_client):
    response = test_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["active_fiscal_year"] == "D2627"

    # Verify SQLite database diagnostics
    assert "database" in data
    assert data["database"] is not None
    assert data["database"]["is_healthy"] is True
    assert data["database"]["journal_mode"] == "WAL"

    # Verify FoxPro tables
    assert "ITEMMST.DBF" in data["tables"]
    assert "NAMEMST.DBF" in data["tables"]
    assert data["tables"]["ITEMMST.DBF"]["exists"] is True
    assert data["tables"]["ITEMMST.DBF"]["record_count"] > 3000


def test_sync_products_endpoint(test_client):
    response = test_client.get("/api/sync/products")
    assert response.status_code == 200
    data = response.json()
    assert data["active_fiscal_year"] == "D2627"
    assert len(data["dbf_checksum"]) == 64
    assert data["total_records"] > 1300
    assert len(data["products"]) == data["total_records"]
    # Verify ghost products are excluded while valid products exist
    codes = {p["code"] for p in data["products"]}
    assert "00013" in codes
    assert "02083" not in codes
    assert "02084" not in codes
    assert "04188" not in codes
    assert "04189" not in codes

    # Verify field structure on first product - Decision 1: 'code' is the ONLY product identifier
    first = data["products"][0]
    required_keys = [
        "code",
        "name",
        "company_code",
        "company_name",
        "group_code",
        "group_name",
        "pack",
        "qty_in_box",
        "tax_percentage",
        "tax_code",
        "rate_type",
        "mrp",
        "selling_rate",
        "purchase_rate",
        "stock_on_hand",
        "is_active",
    ]
    for key in required_keys:
        assert key in first

    # Decision 2: Confirm display_code is NOT present
    assert "display_code" not in first


def test_sync_customers_endpoint(test_client):
    response = test_client.get("/api/sync/customers")
    assert response.status_code == 200
    data = response.json()
    assert data["active_fiscal_year"] == "D2627"
    assert len(data["dbf_checksum"]) == 64
    assert data["total_records"] > 800
    assert len(data["customers"]) == data["total_records"]

    # Verify field structure on first customer
    first = data["customers"][0]
    required_keys = [
        "code",
        "name",
        "city",
        "address_1",
        "address_2",
        "gstin",
        "phone",
        "area_code",
        "area_name",
        "credit_days",
        "credit_limit",
        "current_balance",
        "balance_type",
        "price_tier",
    ]
    for key in required_keys:
        assert key in first

    # Check CASH A/C (99999) presence
    cash_customer = next((c for c in data["customers"] if c["code"] == "99999"), None)
    assert cash_customer is not None
    assert cash_customer["price_tier"] == "RETAIL"


def test_sync_categories_endpoint(test_client):
    response = test_client.get("/api/sync/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 53
    assert len(data["categories"]) == 53
    first = data["categories"][0]
    assert first["sr"] == 1
    assert first["name"] == "ROLL AND DOT CAPS"


def test_sync_subcategories_endpoint(test_client):
    response = test_client.get("/api/sync/subcategories")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] >= 8
    subcat_codes = [s["code"] for s in data["subcategories"]]
    for expected in ["PKT", "BOX", "PCS", "BAG", "ROLL", "TIN", "OTHERS"]:
        assert expected in subcat_codes



def test_import_staging_endpoints(test_client, tmp_path):
    out_file = str(tmp_path / "temp_staging.json")
    response = test_client.post("/api/import/stage", json={"output_file": out_file})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "STAGED"
    assert "exported_count" in data
    assert data["output_file"] == out_file

    # Now fetch it via GET /api/import/staging
    get_res = test_client.get(f"/api/import/staging?file_path={out_file}")
    assert get_res.status_code == 200
    staged = get_res.json()
    assert staged["version"] == "1.0"
    assert staged["series"] == "E"

