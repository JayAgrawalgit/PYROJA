# Visual FoxPro Product Catalog Mapping & Gap Analysis Report
**System:** RAM FATAKA CENTER Billing System (FAVWIN / Visual FoxPro 6.0)  
**Database Evaluated:** `legacy-software-extracted/FAVWIN/D2627/ITEMMST.DBF` (and related masters `COMPMST`, `GROUPMST`, `GROUPSUB`, `TAXMST`)  
**Total Records Analyzed:** 3,019 physical records (1,314 active named products)  
**Document Status:** Production Catalog Feasibility Report

---

## 1. Executive Summary

This report provides an empirical analysis of product catalog fields in FoxPro's `ITEMMST.DBF` to determine whether modern retail/wholesale POS catalog features (Category, Subcategory, Brand, Display Order, Pack Quantity, GST, and Search Aliases) can be sourced directly from the legacy database or if they must be augmented from an external Excel master catalog.

### Verdict Table

| # | Catalog Dimension | Field in `ITEMMST.DBF` | Population in FoxPro | Data Quality in FoxPro | Action Required |
|:---:|---|---|:---:|:---:|:---:|
| 1 | **Category** | `GCODE`, `CCODE` $\to$ `COMPMST` | 100% | ⚠️ **Crude / Unstandardized** | **Import from Excel** (or overlay clean taxonomy) |
| 2 | **Subcategory** | `SUBCODE` | 0.03% (1/3019) | ❌ **Completely Missing** | **Must Import from Excel** |
| 3 | **Brand** | None (`CCODE` repurposed) | 0% structured | ❌ **Embedded in Name text** | **Must Import from Excel** |
| 4 | **Display Order** | None | 0% | ❌ **Completely Missing** | **Must Import from Excel** |
| 5 | **Pack Quantity** | `QIB`, `FACTOR`, `PACK` | `QIB` = 1 (100%) | ❌ **Defective (Always 1)** | **Must Import from Excel** |
| 6 | **GST & HSN** | `TAX`, `TCODE` | 0.00% (100%) | ❌ **Pre-GST VAT Slabs (0%)** | **Must Import from Excel** |
| 7 | **Search Aliases** | `NICK` | 5.1% (`'***'`) | ❌ **Completely Missing** | **Must Import from Excel** |

**Conclusion:**  
While `ITEMMST.DBF` is the authoritative source for **Product Code (`CODE`)**, **Product Name (`NAME`)**, **Wholesale Selling Rate (`SRATE`)**, and **Stock Balance (`CQTY`)**, it is completely inadequate for modern tablet catalog browsing, category filtering, brand selection, case-pack rules, and search. A hybrid overlay architecture is recommended where the Sync Service merges FoxPro master data with an Excel Catalog enrichment file.

---

## 2. In-Depth Analysis of the 7 Catalog Dimensions

### 2.1 Category
- **FoxPro Schema Fields:**
  - `ITEMMST.GCODE` `C(5)`: 100% of records contain `'MIX'`. `GROUPMST.DBF` has only 1 row (`CODE='MIX', NAME='MIX'`). Provides zero categorization.
  - `ITEMMST.CCODE` `C(5)`: References `COMPMST.DBF` (50 distinct values in use).
- **Current Data Quality:**
  - `COMPMST.DBF` was intended for "Company Master", but was repurposed by the shop as a hybrid category / rate-list table.
  - Some entries represent valid physical categories (e.g. `1: ROLL AND DOT CAPS`, `4: SERPANTS & NAGGOLI`, `5: 9 CM SPARKLERS`, `25: GROUND CHAKKAR BIG`, `32: ATOM BOMB`, `34: SHOTS & MULTISHOTS`).
  - Other entries represent seasonal administrative lists (e.g. `50: OFF SEASON LIST 2025-26`, `52: NEW RATE LIST 2024`, `53: NEW RATE LIST 2025-2026`, `43: NO GUARRANTY & NO WARRANTY`, `44: KIRANA 2023-24`).
- **Impact on Tablet App:**
  - Filtering by `CCODE` creates cluttered, non-intuitive navigation tabs on Android tablets (e.g. a category named "OFF SEASON LIST 2025-26").
- **Recommendation:**
  - Standardize into clean retail fireworks categories in Excel: `SPARKLERS`, `GROUND CHAKKARS`, `FLOWER POTS`, `ROCKETS`, `SOUND CRACKERS / BOMBS`, `MULTISHOT CAKES`, `GARLANDS / LAR`, `NOVELTIES`.

---

### 2.2 Subcategory
- **FoxPro Schema Fields:**
  - `ITEMMST.SUBCODE` `C(5)`
  - `GROUPSUB.DBF` (`CODE`, `UCODE`, `FACT`, `NAME`)
- **Current Data Quality:**
  - `ITEMMST.SUBCODE` is populated in exactly **1 out of 3,019 records** (0.03%, value `'PCS'`).
  - `GROUPSUB.DBF` contains exactly **1 row** (`CODE='PKT', FACT=1`).
- **Impact on Tablet App:**
  - Browsing broad categories like "Sparklers" or "Shots" cannot be subdivided into "Electric Sparklers", "Colour Sparklers", "12-Shot Cakes", "30-Shot Cakes", "120-Shot Cakes".
- **Recommendation:**
  - Completely missing in FoxPro; must be imported from the Excel catalog.

---

### 2.3 Brand / Manufacturer
- **FoxPro Schema Fields:**
  - No dedicated `BRAND` field exists.
- **Current Data Quality:**
  - Brand names are **embedded as free text inside `ITEMMST.NAME`**.
  - Examples from active database:
    - `00013`: `111- ROLL CAPS AGNI` $\to$ Brand: **AGNI**
    - `00079`: `119- ASST CARTOON(10 PCS)DURGESH (1P)` $\to$ Brand: **DURGESH**
    - `00080`: `120- ASST CARTOON BEN TEN(25P)AYYANAR 4P` $\to$ Brand: **AYYANAR**
    - `00082`: `124- BIG NAGGOLI PANDYAN BLACK(100X1=1 B` $\to$ Brand: **PANDYAN**
    - `00441`: `520- TRI COL FOUNTAIN COCK (5 P)` $\to$ Brand: **COCK**
    - `00442`: `521- TRI COL FOUNTAIN S.T.D (5 P)` $\to$ Brand: **STANDARD (S.T.D)**
    - `00440`: `519- TRI COL FOUNTAIN MERCURY (10 P)` $\to$ Brand: **MERCURY**
    - `00453`: `533- CRACKLING FOUNTAIN SIVASAKTHI(3 P)` $\to$ Brand: **SIVASAKTHI**
    - `00458`: `537- CAN SHOWER TIN DABBA SRI HARI(1P)1B` $\to$ Brand: **SRI HARI**
- **Impact on Tablet App:**
  - Customers and salesmen frequently ask: *"Show me all Standard brand crackers"* or *"Filter by Cock brand"*. This cannot be filtered via FoxPro columns.
- **Recommendation:**
  - Extract and normalize Brand names into an explicit `brand` column in the Excel catalog.

---

### 2.4 Display Order / Sorting Sequence
- **FoxPro Schema Fields:**
  - None (`DISP_ORDER`, `SORT_ORDER`, `SEQ` do not exist).
- **Current Data Quality:**
  - Items are sorted either by internal code (`00013`, `00079`) or alphabetically by `NAME`.
  - Item names start with legacy paper catalog numbers (`111-`, `119-`, `519-`, `1117-`).
  - In string sorting, `"1117-"` sorts before `"120-"`, creating an erratic sequence on tablet screens.
- **Impact on Tablet App:**
  - Showroom tablets need high-margin, high-velocity items (fast-moving sparklers, popular flower pots) displayed first.
- **Recommendation:**
  - Introduce an integer `display_order` column in Excel (e.g. `10, 20, 30...`).

---

### 2.5 Pack Quantity (Wholesale Case Multiples / Box Packs)
- **FoxPro Schema Fields:**
  - `ITEMMST.PACK` `C(10)`: Contains string description (`'PKT'`, `'BOX'`, `'PCS'`, `'BUNDLE'`).
  - `ITEMMST.QIB` `N(5,0)`: "Quantity in Box".
  - `ITEMMST.FACTOR` `N(11,3)`: Packaging conversion factor.
- **Current Data Quality:**
  - **`QIB` is hardcoded to `1` across 100% of all 3,019 records in `ITEMMST.DBF`.**
  - **`FACTOR` is `0.00` across 100% of records.**
  - The real wholesale packaging rules are buried in text inside `ITEMMST.NAME`:
    - `(10 PCS)` $\to$ Pack Multiple = 10
    - `(25P)` $\to$ Pack Multiple = 25
    - `(100X1=1 B)` $\to$ Pack Multiple = 100
    - `(10 P)` $\to$ Pack Multiple = 10
    - `(5 P)` $\to$ Pack Multiple = 5
- **Impact on Tablet App:**
  - The tablet POS must enforce wholesale pack rules (preventing a customer from ordering 7 packets when the box minimum is 10 or 25). Relying on FoxPro's `QIB = 1` breaks wholesale packaging validation.
- **Recommendation:**
  - Extract and clean true integer `pack_quantity` in the Excel catalog.

---

### 2.6 GST Rates & HSN Codes
- **FoxPro Schema Fields:**
  - `ITEMMST.TAX` `N(5,2)`
  - `ITEMMST.TCODE` `C(5)`
  - `TAXMST.DBF` (`CODE`, `SLAB`, `TAX`)
- **Current Data Quality:**
  - `ITEMMST.TAX` is `0.00` in 100% of records.
  - `TAXMST.DBF` contains outdated pre-2017 VAT slabs (`T1=0%`, `T2=4%`, `T3=5%`, `T4=12.5%`, `T5=20%`).
  - `HSN` code is entirely absent from the schema.
  - Fireworks in India fall under HSN `3604` (`3604 10 00` for fireworks; standard GST rate 18%).
- **Impact on Tablet App:**
  - If tax invoices or GST breakdowns are displayed on tablets or customer quotes, the DBF provides zero GST data.
- **Recommendation:**
  - Supply default GST rate (18%) and HSN code (`36041000`) in the Excel catalog.

---

### 2.7 Search Aliases & Colloquial Keywords
- **FoxPro Schema Fields:**
  - `ITEMMST.NICK` `C(10)`
- **Current Data Quality:**
  - `NICK` is populated in only 155 records (5.1%).
  - 100% of populated values contain only `'***'` (used historically as a star/bookmark flag).
  - No search aliases, phonetic spellings, Marathi/Hindi colloquial names, or abbreviations exist.
  - Examples of real-world buyer search terms not found in FoxPro names:
    - *"Chakri"* or *"Zamin Chakkar"* for Ground Chakkars
    - *"Anar"* or *"Koti"* for Flower Pots
    - *"Phulbatti"* for Sparklers
    - *"Ladi"* or *"Lar"* for Garlands
    - *"Rassi Bomb"* or *"Sutli Bomb"* for Atom Bombs
    - *"Bijli"* for Red Bijali Crackers
    - *"Pencil"* for Color Torches
- **Impact on Tablet App:**
  - Salesmen typing colloquial customer requests into the tablet search bar fail to find items whose official DBF name is in English (e.g. `GROUND CHAKKAR BIG ASHOKA`).
- **Recommendation:**
  - Add a comma-separated `search_aliases` column in Excel.

---

## 3. Recommended Excel Catalog Master Schema

To bridge these gaps without breaking FoxPro compatibility (preserving Decision 1: `ITEMMST.CODE` as the sole primary key), the Excel catalog should contain the following schema:

| Column Name | Type | Mandatory? | Sample Value | Description & Purpose |
|---|:---:|:---:|---|---|
| **`foxpro_code`** | `String(5)` | **YES (PK)** | `'00441'` | Exact 5-character key matching `ITEMMST.CODE`. Used for joining. |
| **`display_name`** | `String(60)` | No | `Tri-Color Fountain 5 Pcs (Cock)` | Clean, readable customer-facing name without cryptic codes. |
| **`category`** | `String(30)` | **YES** | `Flower Pots` | Standardized top-level category for tablet tabs. |
| **`subcategory`** | `String(30)` | No | `Color Fountains` | Secondary drill-down category. |
| **`brand`** | `String(30)` | **YES** | `Cock` | Normalized manufacturer / brand name for brand filter chips. |
| **`display_order`** | `Integer` | No | `120` | Manual sort priority for showroom ranking. |
| **`pack_quantity`**| `Integer` | **YES** | `5` | Case/box minimum order multiple (replaces defective `QIB=1`). |
| **`unit_of_measure`**| `String(10)`| **YES** | `PKT` | Wholesale pack unit (`PKT`, `BOX`, `PCS`, `BUNDLE`). |
| **`gst_rate`** | `Decimal` | **YES** | `18.0` | Applicable GST percentage (default 18%). |
| **`hsn_code`** | `String(10)` | **YES** | `36041000` | Statutory HSN classification code. |
| **`search_aliases`**| `String(255)`| No | `anar, fountain, tri color, koti, cock anar` | Comma-separated colloquial search keywords. |
| **`image_filename`**| `String(100)`| No | `00441_cock_tricolor.jpg` | High-res product photograph for tablet gallery. |
| **`is_featured`** | `Boolean` | No | `TRUE` | Pins popular festival items to the tablet home screen. |

---

## 4. Architectural Integration & Sync Pipeline

```
┌───────────────────────────────┐        ┌───────────────────────────────┐
│       FoxPro ITEMMST.DBF      │        │      Excel Master Catalog     │
│   (Live ERP Billing Master)   │        │     (Marketing & Taxonomy)    │
│  - CODE (PK: "00441")         │        │  - foxpro_code ("00441")      │
│  - SRATE (Price: ₹297.00)     │        │  - category ("Flower Pots")   │
│  - CQTY (Stock: 150)          │        │  - brand ("Cock")             │
│  - Raw NAME                   │        │  - pack_quantity (5)          │
│                               │        │  - search_aliases ("anar")    │
└───────────────┬───────────────┘        └───────────────┬───────────────┘
                │                                        │
                └───────────────────┬────────────────────┘
                                    │
                                    ▼
                 ┌───────────────────────────────────────┐
                 │          Windows Sync Service         │
                 │      (GET /api/sync/products)         │
                 │                                       │
                 │ - Joins on ITEMMST.CODE               │
                 │ - Takes Price & Stock from FoxPro     │
                 │ - Takes Category, Brand, Aliases,     │
                 │   and Pack Rules from Excel           │
                 └──────────────────┬────────────────────┘
                                    │
                                    ▼
                 ┌───────────────────────────────────────┐
                 │           Android Tablet POS          │
                 │                                       │
                 │ - Rich Category Navigation            │
                 │ - Instant Brand Filtering             │
                 │ - Smart Search on Aliases             │
                 │ - Pack Multiple Enforcement           │
                 │ - Live FoxPro Stock & Pricing         │
                 └───────────────────────────────────────┘
```

### Key Architectural Advantages:
1. **Zero FoxPro DBF Schema Changes:** FoxPro's 25-year-old table structure remains completely untouched.
2. **Real-Time Prices & Stock:** Selling rates (`SRATE`) and stock on hand (`CQTY`) continue to be pulled live from `ITEMMST.DBF`.
3. **Rich Tablet Experience:** The Android app receives clean categories, brands, images, and search aliases without burdening the FoxPro billing operator.
4. **Resilience:** If the Excel file is absent or an item is unmapped in Excel, the Sync Service falls back gracefully to `ITEMMST.NAME` and `COMPMST.NAME`.
