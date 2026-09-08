# FoxPro Billing Required Fields & Data Dictionary (Phase 3A)
**System:** RAM FATAKA CENTER Billing System (FAVWIN / Visual FoxPro 6.0)  
**Database Directory:** `legacy-software-extracted/FAVWIN/D2627/`  
**Document Status:** Schema & Field Reference (Read-Only)

---

## 1. Overview & Classification Legend

This document details all fields in the core billing tables required to import an order into the legacy Visual FoxPro database.

### Field Classification:
- **[M] Mandatory:** Must be populated with a valid non-empty value; omitting or leaving empty corrupts application screens or calculations.
- **[A] Auto/Calculated:** Computed programmatically during import from header/line aggregates.
- **[D] Denormalized:** Copied verbatim from master tables (`NAMEMST`, `ITEMMST`, `BILLBOOK`).
- **[O] Optional / Unused:** Present in DBF schema but left empty, zero, or blank by FAVWIN during standard Estimate series operations.

---

## 2. `SALEMST.DBF` (Invoice Header) Field Dictionary

- **Total Fields:** 40 | **Record Length:** 437 bytes

| Field Name | Type | Len | Dec | Class | Source of Data | Default / Example Value | Business Logic & Rules |
|---|:---:|:---:|:---:|:---:|---|---|---|
| `ENTRY` | `N` | 5 | 0 | **[M]** | `BILLBOOK.ENTRY + 1` | `135` | Sequential invoice counter. Must be incremented with record lock. |
| `COME` | `C` | 2 | 0 | **[M]** | Constant | `'E '` | Series identifier. `'E'` = Estimate series. |
| `DATE` | `D` | 8 | 0 | **[M]** | Order Creation Date | `20260907` | Transaction date in `YYYYMMDD` format. |
| `PCODE` | `C` | 5 | 0 | **[M]** | Order Customer Code | `'01149'` | Foreign key to `NAMEMST.CODE`. Zero-padded 5 digits. |
| `SCODE` | `C` | 5 | 0 | **[M]** | Constant | `'SELF '` | Salesman code. Standard retail counter sale is `'SELF'`. |
| `CD` | `C` | 1 | 0 | **[M]** | Constant | `'D'` | Transaction indicator: `'D'` for Debit (Sales). |
| `T1A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 1 (used only for select GST slabs; `0.00` in estimates). |
| `T1B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 1 tax component. |
| `T2A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 2 taxable amount. |
| `T2B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 2 tax component. |
| `T3A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 3 taxable amount. |
| `T3B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 3 tax component. |
| `T4A` | `N` | 11 | 2 | **[A]** | $\sum \text{SALETRN.GAMT}$ | `24200.00` | **Gross Taxable Amount**. Sum of all line item gross amounts. |
| `T4B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Tax tier 4 tax component (0.00 in estimate series). |
| `T5A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 5 taxable amount. |
| `T5B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Sub-tax tier 5 tax component. |
| `X1A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 1. |
| `X1B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 1 amount. |
| `X2A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 2. |
| `X2B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 2 amount. |
| `X3A` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 3. |
| `X3B` | `N` | 11 | 2 | **[O]** | System | `0.00` | Extra tax 3 amount. |
| `CDAMT` | `N` | 11 | 2 | **[O]** | Calculation | `0.00` | Cash discount calculated amount. |
| `SCHEME`| `N` | 11 | 2 | **[O]** | Calculation | `0.00` | Scheme promotion discount. |
| `REMA` | `C` | 25 | 0 | **[O]** | Order Remarks | `'                         '` | Header remark line 1 (space-padded). |
| `REML` | `C` | 25 | 0 | **[O]** | Order Remarks | `'                         '` | Header remark line 2 (space-padded). |
| `ADD` | `N` | 11 | 2 | **[A]** | Order Additions | `0.00` | Additional delivery/packing charges. |
| `LESS` | `N` | 11 | 2 | **[A]** | Order Deductions | `0.00` | Overall bill discount amount deducted from gross total. |
| `ROFF` | `N` | 11 | 2 | **[A]** | Calculation | `0.00` | Round-off adjustment (-0.99 to +0.99) to reach whole rupees. |
| `NAMT` | `N` | 11 | 2 | **[A]** | Calculation | `24200.00` | **Net Grand Total**: `NAMT = T4A + ADD - LESS + ROFF`. |
| `USER` | `C` | 10 | 0 | **[M]** | Current Operator | `'RAM       '` | Login user code in FAVWIN (padded to 10 chars). |
| `PNAME` | `C` | 40 | 0 | **[D]** | `NAMEMST.NAME` | `'NEW SHIVA BALAJI DASARWAR'` | Customer trading name copied from `NAMEMST`. |
| `PRINT` | `C` | 1 | 0 | **[O]** | Constant | `' '` | Print status flag (`' '` = unprinted, `'Y'` = printed). |
| `DUE` | `N` | 2 | 0 | **[O]** | `NAMEMST.DAY` | `0` | Credit payment due days. |
| `APNO` | `N` | 6 | 0 | **[O]** | Constant | `0` | Approval slip reference number. |
| `APDT` | `D` | 8 | 0 | **[O]** | Constant | `'        '` | Approval date. |
| `NOTE` | `C` | 40 | 0 | **[M]** | Tablet Draft ID | `'DRAFT:TAB01-1048          '` | **Traceability field**. Carries the tablet draft UUID / ID. |
| `CASHREC`| `C` | 1 | 0 | **[O]** | Payment Mode | `' '` | `'Y'` if cash receipt collected at billing counter. |
| `DISP` | `N` | 5 | 2 | **[O]** | Order Discount % | `0.00` | Overall discount percentage applied to bill. |
| `VATP` | `N` | 5 | 2 | **[O]** | Constant | `0.00` | Historical VAT percentage (0.00 in current setup). |

---

## 3. `SALETRN.DBF` (Invoice Line Items) Field Dictionary

- **Total Fields:** 33 | **Record Length:** 233 bytes

| Field Name | Type | Len | Dec | Class | Source of Data | Default / Example Value | Business Logic & Rules |
|---|:---:|:---:|:---:|:---:|---|---|---|
| `ENTRY` | `N` | 5 | 0 | **[M]** | `SALEMST.ENTRY` | `135` | Header reference invoice number. |
| `COME` | `C` | 2 | 0 | **[M]** | Constant | `'E '` | Bill book series code. |
| `CD` | `C` | 1 | 0 | **[M]** | Constant | `'D'` | Debit flag. |
| `DATE` | `D` | 8 | 0 | **[M]** | `SALEMST.DATE` | `20260907` | Transaction date matching header. |
| `PCODE` | `C` | 5 | 0 | **[D]** | `SALEMST.PCODE` | `'01149'` | Customer code denormalized on each line item. |
| `ACODE` | `C` | 5 | 0 | **[D]** | `NAMEMST.ACODE` | `'44   '` | Customer geographic area code. |
| `SCODE` | `C` | 5 | 0 | **[M]** | Constant | `'SELF '` | Salesman code. |
| `ICODE` | `C` | 5 | 0 | **[M]** | Order Item Code | `'06122'` | Product item code matching `ITEMMST.CODE`. |
| `GCODE` | `C` | 5 | 0 | **[D]** | `ITEMMST.GCODE` | `'MIX  '` | Product classification group code. |
| `CCODE` | `C` | 5 | 0 | **[D]** | `ITEMMST.CCODE` | `'50   '` | Manufacturer / company brand code. |
| `CASE` | `N` | 9 | 2 | **[O]** | Calculation | `0.00` | Case / carton count (0.00 if sold in loose packets). |
| `QTY` | `N` | 11 | 3 | **[M]** | Order Item Quantity | `15.000` | Units sold. Must be an integer multiple of `ITEMMST.QIB`. |
| `FREE` | `N` | 9 | 2 | **[O]** | Order Promotion | `0.00` | Free sample / bonus quantity. |
| `ACTRT` | `N` | 11 | 2 | **[O]** | `ITEMMST.PRATE` | `0.00` | Actual purchase cost rate (hidden from invoices). |
| `RATE` | `N` | 11 | 3 | **[M]** | Order Item Price | `110.000` | Selling rate per unit (`ITEMMST.SRATE`). |
| `RTTP` | `C` | 1 | 0 | **[D]** | `ITEMMST.RTTP` | `'P'` | Rate type (`'P'` for Piece/Pack, `'D'` for Dozen). |
| `GAMT` | `N` | 11 | 2 | **[A]** | `QTY * RATE` | `1650.00` | Gross line amount. |
| `BATCH` | `C` | 10 | 0 | **[O]** | Constant | `'          '` | Manufacturing batch code (unused for crackers). |
| `MRP` | `N` | 9 | 2 | **[D]** | `ITEMMST.MRP` | `0.00` | Maximum Retail Price printed on package. |
| `EXPDT` | `D` | 8 | 0 | **[O]** | Constant | `'        '` | Expiry date. |
| `SCHP` | `N` | 5 | 2 | **[O]** | Promotion % | `0.00` | Scheme discount percent. |
| `SCHA` | `N` | 11 | 2 | **[O]** | Promotion Amt | `0.00` | Scheme discount amount. |
| `CDP` | `N` | 5 | 2 | **[O]** | Cash Disc % | `0.00` | Cash discount percentage. |
| `CDA` | `N` | 11 | 2 | **[O]** | Cash Disc Amt | `0.00` | Cash discount line amount. |
| `TCODE` | `C` | 5 | 0 | **[D]** | `ITEMMST.TCODE` | `'CST  '` | Tax master reference code. |
| `TAXP` | `N` | 5 | 2 | **[D]** | `ITEMMST.TAX` | `0.00` | Tax percentage. |
| `TAMT` | `N` | 11 | 2 | **[A]** | Calculation | `1650.00` | Taxable amount (`= GAMT - line discounts`). |
| `TAXA` | `N` | 11 | 2 | **[O]** | Calculation | `0.00` | Tax amount calculated on line item. |
| `NAMT` | `N` | 11 | 2 | **[A]** | Calculation | `1650.00` | **Net line total** (`= TAMT + TAXA`). |
| `USER` | `C` | 10 | 0 | **[M]** | Current Operator | `'RAM       '` | Operator username. |
| `SELECT`| `C` | 1 | 0 | **[O]** | Constant | `' '` | Grid selection marker. |
| `SUBCODE`| `C` | 5 | 0 | **[O]** | Constant | `'     '` | Sub-account code. |
| `UNIT` | `C` | 5 | 0 | **[D]** | `ITEMMST.PACK` | `'BOX  '` | Packaging unit (`'BOX'`, `'PKT'`, `'PCS'`). |

---

## 4. `BILLBOOK.DBF` (Invoice Series Counter)

- **Total Fields:** 3 | **Record Length:** 33 bytes

| Field Name | Type | Len | Dec | Class | Value | Notes |
|---|:---:|:---:|:---:|:---:|---|---|
| `CODE` | `C` | 2 | 0 | **[M]** | `'E '` | Estimate Series Key. |
| `NAME` | `C` | 25 | 0 | **[M]** | `'ESTIMATE                 '` | Series description. |
| `ENTRY` | `N` | 5 | 0 | **[M]** | `134` (Increment to `135`) | High-water sequential bill counter. |

---

## 5. `LEDGER.DBF` (Double-Entry Financial Journal)

When an invoice of amount $A$ is created for Customer $P$ with Series `'E'` and Invoice Number $E$:

### 5.1 Debtor Debit Entry:
| Field Name | Type | Len | Dec | Value | Description |
|---|:---:|:---:|:---:|---|---|
| `ENTRY` | `N` | 5 | 0 | `lnEntry` (e.g. `135`) | Invoice reference. |
| `COME` | `C` | 2 | 0 | `'E '` | Series code. |
| `DATE` | `D` | 8 | 0 | `dDate` | Invoice date. |
| `DCODE` | `C` | 5 | 0 | `customer.PCODE` (e.g. `'01149'`) | **Debtor Account** (Customer charged). |
| `CCODE` | `C` | 5 | 0 | `'     '` | Blank for debtor leg. |
| `NHEAD` | `C` | 5 | 0 | `'S0   '` | Opposite account (Sales Control Account). |
| `AMOUNT` | `N` | 15 | 2 | `SALEMST.NAMT` | Net bill grand total debited to customer. |
| `NARA1` | `C` | 40 | 0 | `'INV.NO.E /  135                         '` | Standard invoice narration. |
| `IND` | `C` | 2 | 0 | `'SL'` | Sub-ledger tag: `'SL'` = Sales Ledger. |
| `USER` | `C` | 10 | 0 | `'RAM       '` | Operator username. |

### 5.2 Sales Account Credit Entry:
| Field Name | Type | Len | Dec | Value | Description |
|---|:---:|:---:|:---:|---|---|
| `ENTRY` | `N` | 5 | 0 | `lnEntry` (e.g. `135`) | Invoice reference. |
| `COME` | `C` | 2 | 0 | `'E '` | Series code. |
| `DATE` | `D` | 8 | 0 | `dDate` | Invoice date. |
| `DCODE` | `C` | 5 | 0 | `'     '` | Blank for credit leg. |
| `CCODE` | `C` | 5 | 0 | `'S4   '` | **Creditor Account** (Sales Revenue Account). |
| `NHEAD` | `C` | 5 | 0 | `customer.PCODE` | Opposite account (Customer). |
| `AMOUNT` | `N` | 15 | 2 | `SALEMST.NAMT` | Revenue credited. |
| `NARA1` | `C` | 40 | 0 | `'INV.NO.E /  135                         '` | Standard invoice narration. |
| `IND` | `C` | 2 | 0 | `'SL'` | Sub-ledger tag: `'SL'`. |
| `USER` | `C` | 10 | 0 | `'RAM       '` | Operator username. |

---

## 6. `ITEMMST.DBF` (Stock Balance Updates)

For each line item $i$ in `SALETRN`:
- Seek `ITEMMST.CODE == ICODE`
- Perform in-place field updates:
  ```foxpro
  REPLACE SQTY WITH SQTY + saletrn.qty, ;
          CQTY WITH CQTY - saletrn.qty
  ```
- **Validation Rule:**
  $$\text{CQTY} = \text{OQTY} + \text{PQTY} - \text{SQTY}$$

---

## 7. Formatting & Data Sanitization Rules

To prevent binary parsing errors in Visual FoxPro 6:

1. **Fixed-Length String Padding:**
   Visual FoxPro strings are fixed-width and space-padded (`ASCII 0x20`), **not null-terminated**.
   - A `C(5)` field containing `'1149'` must be stored as `'01149'`.
   - A `C(10)` field containing `'RAM'` must be stored as `'RAM       '`.
   - A `C(40)` field containing `'BOX'` must be stored as `'BOX                                     '`.
2. **Date Format:**
   Dates are stored as 8 ASCII digits in `YYYYMMDD` format without hyphens (e.g., `'20260907'`). Blank dates are 8 space characters (`'        '`).
3. **Numeric Decimal Alignment:**
   - Amounts with 2 decimal places (`N(11,2)`) are stored right-aligned with 2 decimal digits: `'   24200.00'`.
   - Quantities with 3 decimal places (`N(11,3)`) are stored right-aligned: `'     15.000'`.
4. **Traceability in `NOTE`:**
   The `SALEMST.NOTE` field (`C(40)`) must be formatted as:
   ```
   DRAFT:TAB01-1048
   ```
   Left-aligned and padded to 40 characters with spaces.
