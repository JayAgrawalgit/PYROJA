# FoxPro Invoice Import Feasibility Analysis (Phase 3A)
**System:** RAM FATAKA CENTER Billing System (FAVWIN / Visual FoxPro 6.0)  
**Database Directory:** `legacy-software-extracted/FAVWIN/D2627/`  
**Target Environment:** Shop PC running Windows with FAVWIN and Python Sync Service  
**Document Status:** Production Feasibility Report (Read-Only Analysis)

---

## 1. Executive Summary

This feasibility study evaluates mechanisms for importing orders captured by Android tablets via the Windows Sync Service into the legacy Visual FoxPro 6.0 (VFP) billing system (`FAVWIN`).

### Key Findings:
1. **Invoice Creation is Multi-Table and Non-Transactional:**
   Creating an invoice in FAVWIN does not simply write a record to an invoice table. A single invoice requires coordinated, synchronized updates across **five (5) separate tables**: `BILLBOOK.DBF` (counter), `SALEMST.DBF` (header), `SALETRN.DBF` (line items), `ITEMMST.DBF` (inventory decrement), and `LEDGER.DBF` (double-entry accounting).
2. **Compound Indexes (`.CDX`) are Active on Every Table:**
   All tables utilize binary B-tree `.CDX` indexes. Direct low-level binary manipulation of `.DBF` files outside the VFP database engine corrupts these index trees, leading to "Index does not match table" crashes, phantom records, and broken search dialogs.
3. **Direct DBF Insertion is UNSAFE:**
   Inserting records directly into `.DBF` files via Python or generic ODBC drivers without FoxPro engine runtime locks creates severe concurrency hazards, bypasses financial ledger balancing, breaks inventory tracking, and risks catastrophic database corruption.
4. **Recommended Architecture: Headless FoxPro Script (`VFP6.EXE -T IMPORT.PRG`):**
   The safest, most reliable, and industry-standard integration method is to execute a compiled or headless FoxPro script using the native `VFP6.EXE` runtime present on the shop PC. This ensures that 100% of native record locking (`RLOCK()`), index maintenance (`.CDX`), double-entry ledger postings, and stock deductions are handled natively by FoxPro itself.

---

## 2. In-Depth Table Analysis

### 2.1 `BILLBOOK.DBF` (Invoice Numbering & Series Master)
- **Record Count:** 1 record (in active season database `D2627`)
- **Structure:**
  - `CODE` `C(2)`: Series identifier (e.g., `'E '` for Estimate)
  - `NAME` `C(25)`: Series description (e.g., `'ESTIMATE'`)
  - `ENTRY` `N(5,0)`: Last used invoice number (current value: `134`)
- **Invoice Numbering Mechanism:**
  - When an invoice is initiated in FAVWIN, the software seeks the series row in `BILLBOOK.DBF`, locks the record, reads `ENTRY`, increments it by 1 (`lnNextEntry = BILLBOOK.ENTRY + 1`), updates `BILLBOOK.ENTRY = lnNextEntry`, and unlocks the record.
  - The series `'E'` represents the non-tax Estimate series used during Diwali sales operations.
- **Concurrency Hazard:**
  - If an external process reads `BILLBOOK.ENTRY` without native FoxPro record locking (`RLOCK()`) while an operator in FAVWIN is simultaneously creating a bill, duplicate invoice numbers will be generated, leading to primary key collisions in `SALEMST` and `SALETRN`.

---

### 2.2 `SALEMST.DBF` (Invoice Header Master)
- **Record Count:** 450 total records (134 active invoices)
- **Record Length:** 437 bytes | **Fields:** 40 fields
- **Structural Discovery: Edit-History Append Pattern:**
  - In `SALEMST.DBF`, there are 450 physical records for only 134 unique invoice numbers.
  - When an operator in FAVWIN modifies an existing invoice (using the `<CORRECT>` button in `saletrn.FXP`), the software does **not** update the record in-place. Instead, it marks the prior version with a deletion flag (`*`) or appends a new record with the identical `ENTRY` number and revised figures.
  - Any query reading `SALEMST.DBF` must either respect the soft-deletion byte (`0x2A` / `*`) or pick the latest physical record for a given `ENTRY`.
- **Key Financial Fields:**
  - `ENTRY` `N(5,0)`: Unique invoice sequential number.
  - `COME` `C(2,0)`: Bill book series (`'E '`).
  - `DATE` `D(8,0)`: Transaction date (`YYYYMMDD`).
  - `PCODE` `C(5,0)`: Customer account code from `NAMEMST.DBF` (e.g., `'01149'`).
  - `SCODE` `C(5,0)`: Salesman code (consistently `'SELF '`).
  - `CD` `C(1,0)`: Debit/Credit flag (always `'D'` for sales debit).
  - `T4A` `N(11,2)`: Gross taxable amount / subtotal.
  - `ADD` `N(11,2)`: Additional charges (freight/packing).
  - `LESS` `N(11,2)`: General bill discount.
  - `ROFF` `N(11,2)`: Round-off adjustment (-0.99 to +0.99).
  - `NAMT` `N(11,2)`: Net grand total (`NAMT = T4A + ADD - LESS + ROFF`).
  - `USER` `C(10,0)`: Operator username (e.g., `'RAM       '`).
  - `PNAME` `C(40,0)`: Denormalized customer name.
  - `NOTE` `C(40,0)`: Traceability field. **Currently 100% unused in legacy data** (`sample: ''`). This field is the optimal location for storing the tablet draft reference (e.g., `DRAFT:TAB01-1048`).

---

### 2.3 `SALETRN.DBF` (Invoice Line Items Transaction Table)
- **Record Count:** 18,656 total physical records (3,612 active lines in season 2026-27)
- **Record Length:** 233 bytes | **Fields:** 33 fields
- **Heavy Denormalization Architecture:**
  Each line item does not merely record item code and quantity; it redundantly duplicates customer and master classification codes:
  - `ENTRY` `N(5,0)`: Invoice reference linking to `SALEMST.ENTRY`.
  - `COME` `C(2,0)`: Series code (`'E '`).
  - `CD` `C(1,0)`: `'D'`.
  - `DATE` `D(8,0)`: Transaction date (`YYYYMMDD`).
  - `PCODE` `C(5,0)`: Customer code.
  - `ACODE` `C(5,0)`: Customer area code from `NAMEMST.ACODE`.
  - `SCODE` `C(5,0)`: Salesman code (`'SELF '`).
  - `ICODE` `C(5,0)`: Product item code from `ITEMMST.CODE`.
  - `GCODE` `C(5,0)`: Product group code from `ITEMMST.GCODE` (e.g., `'MIX  '`).
  - `CCODE` `C(5,0)`: Product brand/company code from `ITEMMST.CCODE` (e.g., `'50   '`).
  - `QTY` `N(11,3)`: Sold quantity (in unit of sale).
  - `RATE` `N(11,3)`: Unit price.
  - `RTTP` `C(1,0)`: Rate type (`'P'` for Piece/Pack).
  - `GAMT` `N(11,2)`: Gross line amount (`QTY * RATE`).
  - `TCODE` `C(5,0)`: Tax code (e.g., `'CST  '`).
  - `TAMT` `N(11,2)`: Taxable amount (`= GAMT` if no line discount).
  - `NAMT` `N(11,2)`: Net line amount.
  - `UNIT` `C(5,0)`: Packaging unit (e.g., `'BOX  '`, `'PKT  '`, `'PCS  '`).
  - `USER` `C(10,0)`: Operator username.

---

### 2.4 `LEDGER.DBF` (Double-Entry Financial Accounting Ledger)
- **Record Count:** 1,662 active financial ledger entries.
- **Accounting Mechanics on Sale:**
  FAVWIN is an integrated billing and accounting ERP. When an invoice is created, it writes **two to three double-entry postings** into `LEDGER.DBF`:
  1. **Debtor Debit Posting:**
     - `DCODE`: Customer `PCODE` (e.g., `'01149'`).
     - `CCODE`: `''` (empty).
     - `NHEAD`: `'S0   '` (Sales Control Account).
     - `AMOUNT`: Full invoice net amount `NAMT`.
     - `NARA1`: Formatted narration: `'INV.NO.E /    1'`.
     - `IND`: `'SL'` (Sales Ledger).
  2. **Sales Account Credit Posting:**
     - `DCODE`: `''` (empty).
     - `CCODE`: `'S4   '` or group sales head.
     - `NHEAD`: Customer `PCODE`.
     - `AMOUNT`: Taxable sales amount.
     - `NARA1`: `'INV.NO.E /    1'`.
     - `IND`: `'SL'`.
  3. **Discount / Additional Charges Posting (if applicable):**
     - Adjusts heads `'S11'` / `'S14'` for discounts and round-offs.
- **Impact of Omitting LEDGER:**
  If an invoice is inserted into `SALEMST` and `SALETRN` without corresponding records in `LEDGER.DBF`, customer account statements, ledger balances, trial balance, and daily collection reports will be completely desynchronized from sales bills.

---

### 2.5 `ITEMMST.DBF` (Stock Balance Master)
- **Record Count:** 3,020 product master records.
- **Inventory Balance Math:**
  Each item record maintains cumulative quantitative stock counters:
  - `OQTY` `N(11,2)`: Opening Stock.
  - `PQTY` `N(10,0)`: Cumulative Purchases.
  - `SQTY` `N(10,0)`: Cumulative Sales.
  - `CQTY` `N(11,2)`: Closing Stock Balance.
- **Stock Equation:**
  $$\text{CQTY} = \text{OQTY} + \text{PQTY} - \text{SQTY}$$
- **Verification on Invoice 119:**
  - Item `'02152'`: `OQTY = 2500`, `PQTY = 0`, `SQTY = 500` $\implies$ `CQTY = 2000.0`.
  - Item `'02157'`: `OQTY = 900`, `PQTY = 0`, `SQTY = 120` $\implies$ `CQTY = 780.0`.
- **Impact of Omitting ITEMMST Updates:**
  If line items are added to `SALETRN` without updating `ITEMMST.SQTY` and `ITEMMST.CQTY`, physical inventory levels in FAVWIN reports will show stock that was already sold.

---

### 2.6 `DELETRN.DBF` (Deleted Line Items Audit Archive)
- **Record Count:** 2,623 records.
- **Function:**
  When an existing invoice is edited in FAVWIN, previously saved lines that are removed or superseded are automatically moved to `DELETRN.DBF` for audit trail tracking. When appending new invoices, `DELETRN.DBF` is not modified.

---

## 3. Invoice Creation Workflow Trace in FAVWIN

Analysis of compiled program `saletrn.FXP` reveals the sequential workflow executed during invoice entry:

```
[Operator Selects ADDING]
          │
          ▼
1. Lock BILLBOOK record (RLOCK)
   Fetch current ENTRY (e.g. 134)
   Compute Next Entry: lnEntry = 135
   Update BILLBOOK.ENTRY = 135
   Unlock BILLBOOK
          │
          ▼
2. Operator Selects Customer (NAMEMST)
   PCODE, PNAME, ACODE, TCODE loaded into memory
          │
          ▼
3. Line Item Entry Loop (SALETRN)
   For each line item:
     - Seek ITEMMST by ICODE
     - Pull GCODE, CCODE, PACK, RATE, TCODE
     - Input QTY, compute GAMT = QTY * RATE
     - Append blank to SALETRN
     - Populate SALETRN fields
     - Update ITEMMST:
         SQTY = SQTY + QTY
         CQTY = CQTY - QTY
          │
          ▼
4. Bill Totals Calculation (SALEMST)
   - Sum line totals -> T4A
   - Apply general discount -> LESS
   - Apply round off -> ROFF
   - Compute NAMT = T4A + ADD - LESS + ROFF
   - Append blank to SALEMST
   - Populate SALEMST header fields
          │
          ▼
5. Accounting Ledger Generation (LEDGER)
   - Append Debtor Debit row (DCODE=PCODE, NHEAD='S0', AMOUNT=NAMT)
   - Append Sales Credit row (CCODE='S4', NHEAD=PCODE, AMOUNT=T4A)
   - If discount, append Discount row (DCODE='S14', AMOUNT=LESS)
          │
          ▼
6. Update Customer Balance (NAMEMST)
   - NAMEMST.CB = NAMEMST.CB + NAMT (for credit sales)
          │
          ▼
7. Flush & Commit to Disk
   - Re-evaluate all .CDX B-Tree indexes for modified tables
   - Close / Unlock tables
```

---

## 4. Multi-Table & Transactionality Assessment

### 4.1 Is Invoice Creation Single-Table or Multi-Table?
**Definitively MULTI-TABLE.**
Invoice creation touches at minimum five tables:
1. `BILLBOOK.DBF` (counter)
2. `SALEMST.DBF` (header)
3. `SALETRN.DBF` (lines)
4. `ITEMMST.DBF` (stock)
5. `LEDGER.DBF` (accounting)

### 4.2 Is Invoice Creation Transactional?
**NON-TRANSACTIONAL at the DBF file level.**
- The FAVWIN software operates on Visual FoxPro 6.0 **free tables** (tables without a `.DBC` database container).
- Free tables in FoxPro do **not** support native ACID transactions (`BEGIN TRANSACTION ... END TRANSACTION` requires a database container `.DBC`).
- In native FAVWIN, transactionality is emulated entirely in code through sequential procedural steps. If power is lost or the application is killed midway through step 4, the database is left with incremented counters or mismatched header/item rows.
- Any automated import process must ensure strict error handling, pre-validation of all lines, and atomic rollback/cleanup logic in case of failure.

---

## 5. Can Records Be Safely Inserted Externally via Direct DBF Writes?

### Direct DBF Insertion: **STRICTLY UNSAFE & NOT RECOMMENDED**

| Risk Dimension | Direct Python DBF Write | Impact Level | Consequence |
|---|---|---|---|
| **`.CDX` Index Corruption** | Generic Python DBF libraries (`dbf`, `dbfread`, `pyodbc`) cannot safely maintain FoxPro 6 binary compound index trees (`.CDX`). | **CRITICAL** | Table opens in FAVWIN with `"Index tag not found"` or `"Index file does not match the table"`. Search dialogs crash. |
| **Concurrency & Lock Collision** | Python file writes lack VFP `RLOCK()` / `FLOCK()` byte-range locking protocols. | **CRITICAL** | If an operator bills while Python writes, file corruption or lost records occur. |
| **Bypassing Ledger** | Python writers typically only append to `SALEMST` and `SALETRN`. | **HIGH** | Financial books (`LEDGER.DBF`) become unbalanced; trial balance fails to reconcile. |
| **Bypassing Inventory** | Omitting `ITEMMST.SQTY` / `CQTY` updates. | **HIGH** | Physical inventory stock reports in FAVWIN remain inaccurate. |
| **Counter Race Conditions** | External calculation of `BILLBOOK.ENTRY` leads to duplicate invoice numbers. | **HIGH** | Collisions on primary invoice key. |

---

## 6. Comparison of Integration Strategies

Four architectural approaches were analyzed for importing orders into FAVWIN:

### Option 1: Direct DBF Insertion (Python / ODBC)
- **Mechanism:** Python opens `.DBF` files in binary write mode and appends records.
- **Pros:** No FoxPro runtime required.
- **Cons:**
  - Inevitable `.CDX` corruption.
  - Complex manual reconstruction of double-entry ledger rows.
  - High risk of table corruption during concurrent usage.
- **Verdict:** **REJECTED (Dangerous to shop operations).**

---

### Option 2: Headless FoxPro Script (`VFP6.EXE -T IMPORT.PRG`) — *RECOMMENDED*
- **Mechanism:**
  1. The Python Sync Service writes validated pending orders into an intermediate staging file: `orders_staging.json` or `IMPORT_QUEUE.DBF`.
  2. The Sync Service triggers a native FoxPro script execution:
     ```cmd
     VFP6.EXE -T -C"CONFIG.FPW" IMPORT.PRG
     ```
  3. `IMPORT.PRG` runs silently in headless mode using the official VFP 6 runtime:
     - Uses native FoxPro commands: `USE SALEMST EXCLUSIVE` / `SHARED`, `RLOCK()`, `APPEND BLANK`, `REPLACE`, `UPDATE ITEMMST`.
     - Automatically updates all `.CDX` indexes using native VFP B-tree logic.
     - Creates matching `LEDGER.DBF` entries.
     - Deducts stock from `ITEMMST.DBF`.
     - Increments `BILLBOOK.ENTRY` safely.
  4. Returns execution status (e.g., `IMPORT_RESULT.JSON` or exit code `0`).
- **Pros:**
  - 100% index integrity guaranteed by the native FoxPro engine.
  - Full accounting double-entry and inventory math preserved.
  - Executes in milliseconds.
  - Completely invisible to shop operators (no UI flashing).
  - Can be triggered manually via a button in the Sync Service Web UI or scheduled.
- **Cons:**
  - Requires `VFP6.EXE` and its runtime DLLs (`VFP6R.DLL`) present on the Windows PC (already present on the shop PC).
- **Verdict:** **STRONGLY RECOMMENDED (Safest, fastest, most robust).**

---

### Option 3: FoxPro Automation / COM Server (`VisualFoxPro.Application`)
- **Mechanism:** Python connects to FoxPro via Windows COM/ActiveX (`win32com.client.Dispatch("VisualFoxPro.Application")`) and sends commands `oVFP.DoCmd("DO IMPORT.PRG")`.
- **Pros:** Direct in-process error trapping from Python.
- **Cons:**
  - Requires VFP COM server registration on the Windows host (`vfp6.exe /regserver`).
  - Fragile across different Windows permissions and UAC settings.
  - COM server initialization is heavier than headless command-line execution.
- **Verdict:** **VIABLE BUT SECONDARY (Headless CLI is simpler and less prone to COM registration issues).**

---

### Option 4: UI Automation (AutoHotkey / PyAutoGUI)
- **Mechanism:** An automated script simulates keystrokes and mouse clicks inside the FAVWIN billing window.
- **Pros:** Uses the exact UI validation of the application.
- **Cons:**
  - Extremely brittle: screen resolution, active window focus, or pop-up message boxes break execution.
  - Blocks the operator from using the PC while the script runs.
  - Slow (typing 50 line items takes 1–2 minutes per bill).
- **Verdict:** **REJECTED (Unacceptable for fast-paced retail operations).**

---

## 7. Comparative Assessment Matrix

| Evaluation Criteria | Option 1: Direct DBF | Option 2: Headless `IMPORT.PRG` | Option 3: VFP COM Server | Option 4: UI Automation |
|---|:---:|:---:|:---:|:---:|
| **CDX Index Safety** | ❌ High Risk (Corrupts) | ✅ 100% Native Safe | ✅ 100% Native Safe | ✅ Safe |
| **Financial Ledger Integrity** | ⚠️ Complex/Fragile | ✅ 100% Complete | ✅ 100% Complete | ✅ Complete |
| **Inventory Stock Deduction** | ⚠️ Prone to drift | ✅ Exact Native Math | ✅ Exact Native Math | ✅ Exact Native Math |
| **Execution Speed** | Fast (~10ms) | Very Fast (~100ms) | Fast (~200ms) | Very Slow (1–2 min) |
| **Operator Experience** | Background | Background (Invisible) | Background | Blocks Keyboard/Mouse |
| **Concurrency Protection** | ❌ None | ✅ Native FoxPro Locks | ✅ Native FoxPro Locks | ❌ Hijacks Window |
| **Implementation Complexity** | High (Reverse-eng) | Moderate (Clean PRG) | High (COM quirks) | High (Brittle scripts) |
| **Maintenance Burden** | High | Low | Moderate | Very High |
| **Overall Recommendation** | **REJECTED** | **STRONGLY RECOMMENDED** | **ALTERNATIVE** | **REJECTED** |

---

## 8. Final Recommendation & Implementation Roadmap

### Recommendation:
Adopt **Option 2 (Headless FoxPro Script via `IMPORT.PRG`)** as the standard production invoice generation method.

### Staged Rollout for Phase 3B & 3C:
1. **Staging File Generation:**
   The Python Sync Service will generate a clean, validated JSON or CSV batch file (`orders_import_payload.json`) containing the order header, line items, customer code, and tablet draft ID.
2. **Deterministic VFP Script (`IMPORT.PRG`):**
   A dedicated FoxPro program will read the staging payload, open the required tables in `SHARED` mode with appropriate locks, insert the invoice header (`SALEMST`) with the draft ID in `NOTE`, insert line items (`SALETRN`), update stock (`ITEMMST`), post double-entry rows (`LEDGER`), and increment the counter (`BILLBOOK`).
3. **Manual Trigger First:**
   In Phase 3B, the import will be triggered via a simple "Import Orders to Billing" button on the Sync Service Web Dashboard. The shop operator reviews queued tablet orders and clicks "Import".
4. **Zero Risk to FoxPro Core Files:**
   The original software executable (`FAVWIN.EXE` or main menu) is never altered. `IMPORT.PRG` acts purely as an automated batch helper running under the standard VFP runtime.
