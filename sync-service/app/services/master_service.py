"""Service responsible for reading, joining, and caching master data from FoxPro DBF tables."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import time

from app.config import AppConfig
from app.db.database import Database
from app.dbf.reader import DBFReader
from app.schemas.health import DatabaseHealth, HealthResponse, TableHealth
from app.schemas.sync import (
    CategoryItem,
    CategorySyncResponse,
    CustomerItem,
    CustomerSyncResponse,
    ProductItem,
    ProductSyncResponse,
)

logger = logging.getLogger(__name__)


class MasterDataService:
    """Orchestrates read-only access to FoxPro master tables."""

    REQUIRED_TABLES = [
        "ITEMMST.DBF",
        "NAMEMST.DBF",
        "COMPMST.DBF",
        "AREAMST.DBF",
        "TAXMST.DBF",
    ]

    def __init__(self, config: AppConfig, db: Optional[Database] = None):
        self.config = config
        self.data_dir = config.foxpro.data_path
        self.db = db

        # In-memory caches: (timestamp, checksum, data)
        self._cached_products: Optional[Tuple[float, str, List[ProductItem]]] = None
        self._cached_customers: Optional[Tuple[float, str, List[CustomerItem]]] = None
        self._cached_categories: Optional[Tuple[float, str, List[CategoryItem]]] = None

    def get_table_path(self, filename: str) -> Path:
        """Resolve path to a DBF table in the active data directory."""
        direct = self.data_dir / filename
        if direct.exists():
            return direct
        lower = self.data_dir / filename.lower()
        if lower.exists():
            return lower
        if self.data_dir.is_dir():
            for p in self.data_dir.iterdir():
                if p.name.upper() == filename.upper():
                    return p
        return direct

    def _read_table_records(self, filename: str) -> Tuple[List[Dict], str, float]:
        """Read all active records and return (records, checksum, mtime)."""
        table_path = self.get_table_path(filename)
        reader = DBFReader(table_path)
        checksum = reader.compute_checksum()
        mtime = reader.get_mtime()
        records = reader.read_all_records()
        return records, checksum, mtime

    def get_companies_map(self) -> Dict[str, str]:
        """Load company/brand lookup map (CODE -> NAME)."""
        try:
            records, _, _ = self._read_table_records("COMPMST.DBF")
            return {
                str(r.get("CODE", "")).strip(): str(r.get("NAME", "")).strip()
                for r in records
                if r.get("CODE")
            }
        except Exception as e:
            logger.warning(f"Failed to read COMPMST.DBF: {e}")
            return {}

    def get_areas_map(self) -> Dict[str, str]:
        """Load area lookup map (CODE -> NAME)."""
        try:
            records, _, _ = self._read_table_records("AREAMST.DBF")
            return {
                str(r.get("CODE", "")).strip(): str(r.get("NAME", "")).strip()
                for r in records
                if r.get("CODE")
            }
        except Exception as e:
            logger.warning(f"Failed to read AREAMST.DBF: {e}")
            return {}

    def get_taxes_map(self) -> Dict[str, Tuple[str, float]]:
        """Load tax slab lookup map (CODE -> (SLAB, TAX_PERCENTAGE))."""
        try:
            records, _, _ = self._read_table_records("TAXMST.DBF")
            tax_map = {}
            for r in records:
                code = str(r.get("CODE", "")).strip()
                if code:
                    slab = str(r.get("SLAB", "")).strip()
                    tax_val = float(r.get("TAX", 0.0) or 0.0)
                    tax_map[code] = (slab, tax_val)
            return tax_map
        except Exception as e:
            logger.warning(f"Failed to read TAXMST.DBF: {e}")
            return {}

    def get_products_sync(self, force_refresh: bool = False) -> ProductSyncResponse:
        """Fetch joined product records using FoxPro ITEMMST.CODE as the sole identifier."""
        item_path = self.get_table_path("ITEMMST.DBF")
        if not item_path.is_file():
            raise FileNotFoundError(f"Product master table not found: {item_path}")

        now = time.time()
        current_mtime = item_path.stat().st_mtime

        # Check cache validity
        if not force_refresh and self._cached_products is not None:
            cached_time, cached_checksum, cached_items = self._cached_products
            if now - cached_time < self.config.cache.ttl_seconds:
                if not self.config.cache.validate_mtime or current_mtime <= cached_time:
                    return ProductSyncResponse(
                        sync_timestamp=datetime.now(timezone.utc).isoformat(),
                        active_fiscal_year=self.config.foxpro.active_fiscal_year,
                        dbf_checksum=cached_checksum,
                        total_records=len(cached_items),
                        is_delta=False,
                        products=cached_items,
                    )

        # Cache miss or expired: read and assemble
        t0 = time.time()
        companies = self.get_companies_map()
        taxes = self.get_taxes_map()
        item_records, checksum, _ = self._read_table_records("ITEMMST.DBF")

        products: List[ProductItem] = []
        for r in item_records:
            code = str(r.get("CODE", "")).strip()
            if not code:
                continue

            ccode = str(r.get("CCODE", "")).strip()
            company_name = companies.get(ccode, f"Brand {ccode}" if ccode else "General")

            tcode = str(r.get("TCODE", "")).strip()
            tax_info = taxes.get(tcode)
            if tax_info:
                tax_slab, tax_pct = tax_info
            else:
                tax_pct = float(r.get("TAX", 0.0) or 0.0)
                tax_slab = tcode if tcode else f"{tax_pct:.1f}%"

            gcode = str(r.get("GCODE", "")).strip()
            name = str(r.get("NAME", "")).strip()
            pack = str(r.get("PACK", "")).strip() or "UNIT"
            nick = str(r.get("NICK", "")).strip() or None
            qib = int(r.get("QIB", 1) or 1)
            rate_type = str(r.get("RTTP", "P")).strip() or "P"
            mrp = float(r.get("MRP", 0.0) or 0.0)
            srate = float(r.get("SRATE", 0.0) or 0.0)
            prate = float(r.get("PRATE", 0.0) or 0.0)
            cqty = float(r.get("CQTY", 0.0) or 0.0)

            products.append(
                ProductItem(
                    code=code,  # Single product identifier everywhere
                    name=name,
                    company_code=ccode,
                    company_name=company_name,
                    group_code=gcode,
                    group_name=gcode or "General",
                    pack=pack,
                    nick=nick,
                    qty_in_box=qib,
                    tax_percentage=tax_pct,
                    tax_code=tcode or "DEFAULT",
                    rate_type=rate_type,
                    mrp=mrp,
                    selling_rate=srate,
                    purchase_rate=prate,
                    stock_on_hand=cqty,
                    is_active=True,
                )
            )

        duration_ms = (time.time() - t0) * 1000
        logger.info(f"Loaded {len(products)} products from ITEMMST.DBF in {duration_ms:.1f}ms")

        # Update in-memory cache and SQLite state
        self._cached_products = (now, checksum, products)
        if self.db:
            self.db.set_sync_state("ITEMMST_CHECKSUM", checksum)
            self.db.set_sync_state("ITEMMST_COUNT", str(len(products)))

        return ProductSyncResponse(
            sync_timestamp=datetime.now(timezone.utc).isoformat(),
            active_fiscal_year=self.config.foxpro.active_fiscal_year,
            dbf_checksum=checksum,
            total_records=len(products),
            is_delta=False,
            products=products,
        )

    def get_customers_sync(self, force_refresh: bool = False) -> CustomerSyncResponse:
        """Fetch joined customer/party records from FoxPro NAMEMST.DBF."""
        name_path = self.get_table_path("NAMEMST.DBF")
        if not name_path.is_file():
            raise FileNotFoundError(f"Customer master table not found: {name_path}")

        now = time.time()
        current_mtime = name_path.stat().st_mtime

        # Check cache validity
        if not force_refresh and self._cached_customers is not None:
            cached_time, cached_checksum, cached_items = self._cached_customers
            if now - cached_time < self.config.cache.ttl_seconds:
                if not self.config.cache.validate_mtime or current_mtime <= cached_time:
                    return CustomerSyncResponse(
                        sync_timestamp=datetime.now(timezone.utc).isoformat(),
                        active_fiscal_year=self.config.foxpro.active_fiscal_year,
                        dbf_checksum=cached_checksum,
                        total_records=len(cached_items),
                        is_delta=False,
                        customers=cached_items,
                    )

        # Cache miss or expired: read and assemble
        t0 = time.time()
        areas = self.get_areas_map()
        name_records, checksum, _ = self._read_table_records("NAMEMST.DBF")

        customers: List[CustomerItem] = []
        for r in name_records:
            code = str(r.get("CODE", "")).strip()
            name = str(r.get("NAME", "")).strip()
            if not code or not name:
                continue

            acode = str(r.get("ACODE", "")).strip()
            area_name = areas.get(acode, f"Area {acode}" if acode else "Local")

            city = str(r.get("PLACE", "")).strip()
            add1 = str(r.get("ADD1", "")).strip()
            add2 = str(r.get("ADD2", "")).strip()
            tin = str(r.get("TIN", "")).strip()
            cst = str(r.get("CST", "")).strip()
            gstin = tin or cst or ""
            phone = str(r.get("PH", "")).strip()
            cont = str(r.get("CONT", "")).strip() or None
            days = int(r.get("DAY", 0) or 0)
            limit = float(r.get("LIMIT", 0.0) or 0.0)
            cb = float(r.get("CB", 0.0) or 0.0)
            dc = str(r.get("DC", "D")).strip().upper() or "D"

            price_tier = "RETAIL" if code == "99999" else "WHOLESALE"

            customers.append(
                CustomerItem(
                    code=code,
                    name=name,
                    city=city,
                    address_1=add1,
                    address_2=add2,
                    gstin=gstin,
                    phone=phone,
                    contact_person=cont,
                    area_code=acode,
                    area_name=area_name,
                    credit_days=days,
                    credit_limit=limit,
                    current_balance=cb,
                    balance_type=dc,
                    price_tier=price_tier,
                )
            )

        duration_ms = (time.time() - t0) * 1000
        logger.info(f"Loaded {len(customers)} customers from NAMEMST.DBF in {duration_ms:.1f}ms")

        # Update cache and SQLite state
        self._cached_customers = (now, checksum, customers)
        if self.db:
            self.db.set_sync_state("NAMEMST_CHECKSUM", checksum)
            self.db.set_sync_state("NAMEMST_COUNT", str(len(customers)))

        return CustomerSyncResponse(
            sync_timestamp=datetime.now(timezone.utc).isoformat(),
            active_fiscal_year=self.config.foxpro.active_fiscal_year,
            dbf_checksum=checksum,
            total_records=len(customers),
            is_delta=False,
            customers=customers,
        )

    def get_categories_sync(self, force_refresh: bool = False) -> CategorySyncResponse:
        """Fetch showroom categories/sections from COMPMST.DBF sorted by sequence number SR."""
        comp_path = self.get_table_path("COMPMST.DBF")
        if not comp_path.is_file():
            raise FileNotFoundError(f"Category master table not found: {comp_path}")

        now = time.time()
        current_mtime = comp_path.stat().st_mtime

        # Check cache
        if not force_refresh and self._cached_categories is not None:
            cached_time, cached_checksum, cached_items = self._cached_categories
            if now - cached_time < self.config.cache.ttl_seconds:
                if not self.config.cache.validate_mtime or current_mtime <= cached_time:
                    return CategorySyncResponse(
                        sync_timestamp=datetime.now(timezone.utc).isoformat(),
                        active_fiscal_year=self.config.foxpro.active_fiscal_year,
                        dbf_checksum=cached_checksum,
                        total_records=len(cached_items),
                        categories=cached_items,
                    )

        t0 = time.time()
        comp_records, checksum, _ = self._read_table_records("COMPMST.DBF")

        # Compute active item counts per CCODE from ITEMMST
        item_counts = {}
        try:
            item_records, _, _ = self._read_table_records("ITEMMST.DBF")
            for r in item_records:
                if r.get("CODE"):
                    cc = str(r.get("CCODE", "")).strip()
                    item_counts[cc] = item_counts.get(cc, 0) + 1
        except Exception as e:
            logger.warning(f"Could not compute item counts for categories: {e}")

        categories: List[CategoryItem] = []
        for r in comp_records:
            code = str(r.get("CODE", "")).strip()
            if not code:
                continue
            name = str(r.get("NAME", "")).strip()
            sr = int(r.get("SR", 0) or 0)
            categories.append(
                CategoryItem(
                    code=code,
                    name=name,
                    sr=sr,
                    item_count=item_counts.get(code, 0),
                )
            )

        # Sort primarily by SR sequence (1..43..), secondarily by code
        categories.sort(key=lambda c: (c.sr if c.sr > 0 else 9999, c.code))

        duration_ms = (time.time() - t0) * 1000
        logger.info(f"Loaded {len(categories)} categories from COMPMST.DBF in {duration_ms:.1f}ms")

        self._cached_categories = (now, checksum, categories)
        if self.db:
            self.db.set_sync_state("COMPMST_CHECKSUM", checksum)
            self.db.set_sync_state("COMPMST_COUNT", str(len(categories)))

        return CategorySyncResponse(
            sync_timestamp=datetime.now(timezone.utc).isoformat(),
            active_fiscal_year=self.config.foxpro.active_fiscal_year,
            dbf_checksum=checksum,
            total_records=len(categories),
            categories=categories,
        )

    def check_health(self) -> HealthResponse:
        """Examine table availability and health status."""
        tables_health: Dict[str, TableHealth] = {}
        all_ok = True

        for table_name in self.REQUIRED_TABLES:
            path = self.get_table_path(table_name)
            if not path.is_file():
                all_ok = False
                tables_health[table_name] = TableHealth(
                    name=table_name,
                    path=str(path),
                    exists=False,
                    record_count=0,
                    error="File does not exist",
                )
                continue

            try:
                reader = DBFReader(path)
                hdr = reader.header
                mtime_str = datetime.fromtimestamp(reader.get_mtime(), tz=timezone.utc).isoformat()
                checksum = reader.compute_checksum()

                tables_health[table_name] = TableHealth(
                    name=table_name,
                    path=str(path),
                    exists=True,
                    record_count=hdr.num_records,
                    checksum=checksum[:16] + "...",
                    last_modified=mtime_str,
                )
            except Exception as e:
                all_ok = False
                tables_health[table_name] = TableHealth(
                    name=table_name,
                    path=str(path),
                    exists=True,
                    record_count=0,
                    error=str(e),
                )

        db_health = None
        if self.db:
            db_status = self.db.check_health()
            if not db_status.get("is_healthy", False):
                all_ok = False
            db_health = DatabaseHealth(
                exists=db_status.get("exists", False),
                path=db_status.get("path", ""),
                journal_mode=db_status.get("journal_mode"),
                is_healthy=db_status.get("is_healthy", False),
                error=db_status.get("error"),
            )

        return HealthResponse(
            status="HEALTHY" if all_ok else "DEGRADED",
            version="1.0.0",
            timestamp=datetime.now(timezone.utc).isoformat(),
            active_fiscal_year=self.config.foxpro.active_fiscal_year,
            data_path=str(self.data_dir),
            database=db_health,
            tables=tables_health,
        )
