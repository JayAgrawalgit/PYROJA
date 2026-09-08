"""Unit tests for the MasterDataService class."""

from pathlib import Path
import pytest

from app.config import AppConfig, FoxproConfig, DatabaseConfig, CacheConfig
from app.db.database import Database
from app.services.master_service import MasterDataService
from tests.conftest import create_synthetic_dbf


def test_master_service_joins(temp_dbf_dir):
    # 1. Create COMPMST.DBF
    create_synthetic_dbf(
        temp_dbf_dir / "COMPMST.DBF",
        [("CODE", "C", 5, 0), ("NAME", "C", 30, 0), ("SR", "N", 5, 0)],
        [
            {"CODE": "1", "NAME": "STANDARD FIREWORKS", "SR": 1},
            {"CODE": "2", "NAME": "CORONATION SPARKLERS", "SR": 2},
        ],
    )

    # 2. Create TAXMST.DBF
    create_synthetic_dbf(
        temp_dbf_dir / "TAXMST.DBF",
        [("CODE", "C", 5, 0), ("SLAB", "C", 15, 0), ("TAX", "N", 5, 2)],
        [
            {"CODE": "T1", "SLAB": "GST 18%", "TAX": 18.00},
            {"CODE": "T2", "SLAB": "GST 12%", "TAX": 12.00},
        ],
    )

    # 3. Create AREAMST.DBF
    create_synthetic_dbf(
        temp_dbf_dir / "AREAMST.DBF",
        [("CODE", "C", 5, 0), ("NAME", "C", 30, 0)],
        [
            {"CODE": "A01", "NAME": "GHATANJI CENTRAL"},
            {"CODE": "A02", "NAME": "YAVATMAL ROAD"},
        ],
    )

    # 4. Create ITEMMST.DBF
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
                "CODE": "00101",
                "CCODE": "1",
                "GCODE": "SPK",
                "NAME": "10 CM SPARKLER RED",
                "PACK": "BOX",
                "NICK": "***",
                "QIB": 10,
                "TAX": 18.00,
                "TCODE": "T1",
                "RTTP": "P",
                "MRP": 45.00,
                "SRATE": 38.00,
                "PRATE": 30.00,
                "CQTY": 500.00,
            }
        ],
    )

    # 5. Create NAMEMST.DBF
    create_synthetic_dbf(
        temp_dbf_dir / "NAMEMST.DBF",
        [
            ("CODE", "C", 5, 0),
            ("NAME", "C", 30, 0),
            ("PLACE", "C", 20, 0),
            ("ADD1", "C", 30, 0),
            ("ADD2", "C", 30, 0),
            ("TIN", "C", 12, 0),
            ("CST", "C", 12, 0),
            ("ACODE", "C", 5, 0),
            ("DAY", "N", 3, 0),
            ("LIMIT", "N", 11, 0),
            ("CONT", "C", 20, 0),
            ("PH", "C", 20, 0),
            ("CB", "N", 11, 2),
            ("DC", "C", 1, 0),
        ],
        [
            {
                "CODE": "00501",
                "NAME": "MAHALAXMI TRADERS",
                "PLACE": "GHATANJI",
                "ADD1": "SHOP 4 BAZAR",
                "ADD2": "DIST YAVATMAL",
                "TIN": "27AABCM1234",
                "CST": "",
                "ACODE": "A01",
                "DAY": 15,
                "LIMIT": 50000,
                "CONT": "RAMESH BHAI",
                "PH": "9876543210",
                "CB": 12500.00,
                "DC": "D",
            },
            {
                "CODE": "99999",
                "NAME": "CASH A/C",
                "PLACE": "",
                "ADD1": "",
                "ADD2": "",
                "TIN": "",
                "CST": "",
                "ACODE": "",
                "DAY": 0,
                "LIMIT": 0,
                "CONT": "",
                "PH": "",
                "CB": 0.00,
                "DC": "D",
            },
        ],
    )

    db_path = temp_dbf_dir / "test_state.sqlite3"
    db = Database(db_path)

    cfg = AppConfig(
        foxpro=FoxproConfig(data_path=temp_dbf_dir, active_fiscal_year="SYNTHETIC"),
        database=DatabaseConfig(path=db_path),
        cache=CacheConfig(ttl_seconds=10, validate_mtime=True),
    )
    svc = MasterDataService(cfg, db=db)

    # Test products sync - Decision 1: CODE is only identifier
    prod_resp = svc.get_products_sync()
    assert prod_resp.total_records == 1
    p = prod_resp.products[0]
    assert p.code == "00101"
    assert not hasattr(p, "display_code") or "display_code" not in p.model_fields
    assert p.company_name == "STANDARD FIREWORKS"
    assert p.tax_percentage == 18.00
    assert p.selling_rate == 38.00
    assert p.stock_on_hand == 500.00

    # Verify SQLite state was recorded
    assert db.get_sync_state("ITEMMST_COUNT") == "1"
    assert db.get_sync_state("ITEMMST_CHECKSUM") is not None

    # Test customers sync
    cust_resp = svc.get_customers_sync()
    assert cust_resp.total_records == 2
    c1 = next(c for c in cust_resp.customers if c.code == "00501")
    assert c1.name == "MAHALAXMI TRADERS"
    assert c1.area_name == "GHATANJI CENTRAL"
    assert c1.credit_days == 15
    assert c1.credit_limit == 50000.00
    assert c1.price_tier == "WHOLESALE"

    cash = next(c for c in cust_resp.customers if c.code == "99999")
    assert cash.name == "CASH A/C"
    assert cash.price_tier == "RETAIL"

    # Verify SQLite state for customers
    assert db.get_sync_state("NAMEMST_COUNT") == "2"

    # Test health check including SQLite
    health = svc.check_health()
    assert health.status == "HEALTHY"
    assert health.database is not None
    assert health.database.is_healthy is True
    assert health.database.journal_mode == "WAL"
    assert len(health.tables) == 5
    assert health.tables["ITEMMST.DBF"].exists is True
    assert health.tables["ITEMMST.DBF"].record_count == 1
