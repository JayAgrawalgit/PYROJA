# Alpha Pilot Bug Tracker & Defect Management Template
**System:** RAM FATAKA CENTER Billing & POS Integration  
**Pilot Phase:** Alpha Showroom Operational Testing  
**Tracking Scope:** Android Tablet App, Windows Sync Service, FoxPro `IMPORT.PRG`  
**Document Status:** Operational Issue Tracking Log

---

## 1. Severity Classification & SLA Standards

| Severity Level | Definition & Operational Impact | Target Resolution SLA | Pilot Gate Impact |
|---|---|:---:|:---:|
| **P1 - Blocker / Critical** | Data loss, duplicate invoice numbers, FoxPro DBF or `.CDX` corruption, tablet application crash loop, inability to bill customers. | **Immediate (< 2 Hours)** | **Halts Pilot** |
| **P2 - Major** | Order sync failure, pricing discrepancy between tablet and FoxPro, stock balance deduction mismatch, offline outbox failure. | **Same Day (< 6 Hours)** | Must fix before Day 2 live session |
| **P3 - Minor** | UI layout overlap, slow section rendering (> 1s), soft keyboard covering input fields, non-blocking visual glitches. | **< 24 Hours** | Tracked; pilot continues |
| **P4 - Enhancement / UX** | Usability suggestions, button repositioning, contrast tweaks, new quick-stepper increments (`+25`, `+50`). | **Post-Pilot Backlog** | Optional |

---

## 2. Pilot Defect Log & Tracking Register

| Issue ID | Date | Module | Sev | Issue Title / Summary | Reporter | Status | Resolution / Root Cause |
|:---:|:---:|:---:|:---:|---|:---:|:---:|---|
| `BUG-01` | 07/09 | `[TAB-UI]` | `P3` | Long product names (> 35 chars) truncate on 10.1" tablet grid | Operator 1 | **RESOLVED** | Added 2-line title wrapping with CSS `line-clamp: 2`. |
| `BUG-02` | 07/09 | `[SYNC-API]`| `P2` | Customer search fails if party name has single quotes (e.g. `KIDDY'S JOY`) | Operator 2 | **RESOLVED** | Sanitized SQL parameters and JSON escaping in FastAPI router. |
| `BUG-03` | 07/09 | `[VFP-IMP]` | `P1` | `BILLBOOK` timeout if billing clerk leaves FAVWIN edit dialog open | Operator 2 | **RESOLVED** | Implemented 10-retry exponential backoff with `RLOCK()` in `IMPORT.PRG`. |
| `BUG-04` | _____ | `[TAB-CACHE]`| `P_` | | | `OPEN` | |
| `BUG-05` | _____ | `[NET-WIFI]` | `P_` | | | `OPEN` | |
| `BUG-06` | _____ | `[TAB-UI]` | `P_` | | | `OPEN` | |
| `BUG-07` | _____ | `[VFP-IMP]` | `P_` | | | `OPEN` | |
| `BUG-08` | _____ | `[SYNC-API]`| `P_` | | | `OPEN` | |
| `BUG-09` | _____ | `[TAB-UI]` | `P_` | | | `OPEN` | |
| `BUG-10` | _____ | `[TAB-UI]` | `P_` | | | `OPEN` | |

---

## 3. Standard Defect Report Template

When logging an issue, copy and complete this standardized markdown block:

```markdown
### [BUG-XX] Short Descriptive Title of Defect

- **Date / Time Reported:** 2026-09-XX XX:XX AM/PM
- **Reporter:** [ ] Operator 1 (Salesman)  |  [ ] Operator 2 (Billing Clerk)
- **Module:** [ ] Tablet UI  [ ] Tablet Cache  [ ] Sync API  [ ] FoxPro IMPORT  [ ] WiFi/Network
- **Severity:** [ ] P1-Blocker  [ ] P2-Major  [ ] P3-Minor  [ ] P4-Enhancement
- **Environment:** Tablet TAB-01 (Android 13) / Windows 10 Billing PC

#### Steps to Reproduce:
1. Open Tablet POS and select customer '01149'.
2. Navigate to Section 16 (FLOWER POTS).
3. Tap '+10' on item '443- FLOWER POTS SMALL' 3 times (Quantity = 30).
4. Disconnect WiFi.
5. Tap 'Submit Order'.

#### Expected Behavior:
Order should save locally in IndexedDB outbox with status 'QUEUED_OFFLINE' and display an amber toast notification.

#### Actual Behavior:
App displays a red error dialog: "NetworkError: Failed to fetch" and disables the submit button until app is restarted.

#### Evidence / Error Logs:
- Console Error: `Uncaught (in promise) TypeError: Failed to fetch at syncQueue (app.js:184)`
- Screenshot Filename: `bug_XX_network_error.png`

#### Impact & Workaround:
Salesman had to re-enable WiFi and re-enter the 5-item order.
```

---

## 4. Alpha Pilot High-Risk Watchlist

The following high-risk edge cases must be proactively tested and verified during the pilot:

### 4.1 Concurrency Collision on Invoice Numbering
* **Scenario:** Operator 1 submits an order on Tablet while Operator 2 is actively saving a retail invoice in FAVWIN on the PC.
* **Risk:** Collision on `BILLBOOK.ENTRY` leading to duplicate invoice numbers.
* **Verification Check:**
  - Verify that `IMPORT.PRG` uses `RLOCK()` on `BILLBOOK` with retry loops.
  - Check `SALEMST.DBF` to confirm that the tablet order and FAVWIN invoice receive distinct, sequential `ENTRY` numbers.

---

### 4.2 Large Multi-Line Orders (> 40 Line Items)
* **Scenario:** A wholesale village retailer buys across 35 different cracker sections in a single visit.
* **Risk:** Buffer overflow in `IMPORT.PRG` string parsing or JSON truncation.
* **Verification Check:**
  - `IMPORT.PRG` array size for rollback tracking is dimensioned to `laInsertedItems[500, 2]`.
  - Confirm that an order with 45 line items imports completely into `SALETRN.DBF` without dropped lines.

---

### 4.3 Network Interruption During Order Submission
* **Scenario:** Salesman taps "Submit Order" at the exact moment WiFi drops at the boundary of the warehouse.
* **Risk:** HTTP request reaches server, but tablet fails to receive confirmation; tablet re-submits when connection returns, creating a duplicate order.
* **Verification Check:**
  - Gate 1: Tablet client idempotency token prevents double-submission.
  - Gate 2: Sync Service SQLite database enforces `UNIQUE (draft_id)` and idempotency key caching.
  - Result: Second attempt receives original `order_id` with status `ALREADY_EXISTS`. Zero duplicate orders created.

---

### 4.4 Discrepancy Between Selling Rate (`SRATE`) and Cash Invoice
* **Scenario:** Customer negotiates a bulk discount on the showroom floor.
* **Risk:** Salesman changes rates on line items; FoxPro billing clerk overrides with standard price.
* **Verification Check:**
  - Policy: Line items strictly preserve FoxPro `ITEMMST.SRATE`.
  - Negotiated discount is entered exclusively in the `less_amount` header field.
  - In FoxPro `SALEMST`, verify `LESS` equals the negotiated discount, and `T4A` equals the gross price sum.

---

### 4.5 Soft-Deleted Records in Legacy FoxPro Tables
* **Scenario:** An item was previously deleted or replaced in `ITEMMST` or `SALEMST`.
* **Risk:** `IMPORT.PRG` seeks into a deleted record (`0x2A` / `*`).
* **Verification Check:**
  - `IMPORT.PRG` explicitly executes `SET DELETED ON` at startup.
  - Python `DBFReader` skips records with deletion flag `0x2A`.
  - Confirm that deleted items in `ITEMMST` never appear on the tablet catalog.
