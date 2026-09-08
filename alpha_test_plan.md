# Alpha Pilot Test Plan: Showroom Floor Operations
**System:** RAM FATAKA CENTER Billing & POS Integration  
**Environment:** Shop LAN / WiFi, 2 Android Tablets, 1 Windows Billing PC  
**Data Scope:** 100% Native Visual FoxPro 6.0 Data (`COMPMST`, `ITEMMST`, `NAMEMST`)  
**Duration:** 2 Days (Pre-Festival Simulated & Controlled Live Sessions)  
**Document Status:** Production Operational Test Plan

---

## 1. Pilot Objectives & Test Scope

The objective of the Alpha Pilot is to validate the tablet-assisted ordering workflow on the showroom floor under real operating conditions, verifying that:
1. Salesmen can navigate all 42 showroom sections (`COMPMST.SR`) without paper clipboards.
2. Orders are captured accurately with FoxPro product codes (`ITEMMST.CODE`), wholesale rates (`SRATE`), and quantities.
3. Orders sync seamlessly over local WiFi to the Windows Sync Service.
4. The billing clerk on the main PC can review queued drafts and verify exact mathematical and inventory alignment with FAVWIN.

---

## 2. Operator Profiles & Responsibilities

The pilot involves **two primary operators** reflecting the division of labor in the shop:

```
┌────────────────────────────────────────────────────────┐
│ 📱 OPERATOR 1: Showroom Floor Salesman (Tablet POS)    │
│ - Hardware: Android Tablet 10.1" on Shop WiFi          │
│ - Tasks: Customer selection, walking aisles with       │
│   buyers, section navigation, quick-stepping quantities│
│   order review, and draft submission.                  │
└──────────────────────────┬─────────────────────────────┘
                           │ (Local WiFi / HTTP REST)
                           ▼
┌────────────────────────────────────────────────────────┐
│ 🖥️ OPERATOR 2: Billing Clerk / Counter Operator (PC)   │
│ - Hardware: Windows Shop Billing PC running FAVWIN     │
│ - Tasks: Monitoring Sync Service dashboard, validating │
│   incoming draft totals, staging payloads, executing   │
│   IMPORT.PRG, verifying DBF ledger & stock updates.    │
└────────────────────────────────────────────────────────┘
```

### Operator 1: Showroom Floor Salesman (Tablet)
* **Profile:** Experienced counter salesman familiar with paper catalog numbering (`111-`, `178-`, `443-`).
* **Test Focus:**
  * Speed of switching between sections (`COMPMST.SR` 1 to 43).
  * Ergonomics of quick-stepper buttons (`+1`, `+5`, `+10`).
  * Accuracy of full-text brand search (e.g. typing `"COCK"` or `"STD"`).
  * Vernacular search behavior (e.g. typing `"anar"`, `"chakri"`, `"ladi"`).
  * Handling out-of-stock items (`CQTY <= 0`).
  * Offline order creation during WiFi dead zones in back warehouse.

### Operator 2: Billing Clerk / Counter Operator (PC)
* **Profile:** Operator running FAVWIN billing and daily cash collections.
* **Test Focus:**
  * Real-time visibility of queued tablet drafts on `http://localhost:8080`.
  * Verifying customer party balance (`NAMEMST.CB`) matches tablet display.
  * Triggering staging (`POST /api/import/stage`).
  * Running headless `VFP6.EXE -T IMPORT.PRG` and checking `import_result.json`.
  * Verifying invoice header in `SALEMST` (Entry sequence, `NOTE` carrying `DRAFT:TAB01-XXXX`, Net Total).
  * Verifying double-entry ledger postings in `LEDGER` and stock deduction in `ITEMMST`.

---

## 3. Real-World Testing Checklist

### Phase A: Morning Readiness & Master Data Sync (Day 1, 09:00 - 10:00)
- [ ] **A1. Windows Sync Service Online:** Service running on PC; `GET /api/health` returns `HEALTHY` and verifies all 5 DBF tables.
- [ ] **A2. Tablet Connectivity:** Tablets connect to shop private WiFi SSID; verify tablet ping to PC IP (`192.168.1.X:8080`).
- [ ] **A3. Initial Catalog Sync:** Tablet opens; pulls 1,091 active items across 42 sections. Verify zero crash on startup.
- [ ] **A4. Customer Master Verification:** Search customer `00276` (`BUTLE FATAKA`) and `01149` (`NEW SHIVA BALAJI`); verify city and balance match FoxPro.
- [ ] **A5. Cash Account Available:** Verify counter customer account `99999` (`CASH A/C`) is pinned at top.

---

### Phase B: Simulated Workflow Test Battery (Day 1, 10:00 - 14:00)

#### Scenario 1: Fast Small Retail Order (Counter Walk-in)
* **Customer:** Cash Counter (`99999`).
* **Checklist:**
  - [ ] Start draft $\to$ Auto-generated draft ID (e.g. `TAB01-1001`).
  - [ ] Jump to Section 5 (`9 CM SPARKLERS`) $\to$ Add 2 PKT `178- 9 CM PLAIN INDRA` (₹38.00).
  - [ ] Jump to Section 16 (`FLOWER POTS`) $\to$ Add 2 PKT `443- FLOWER POTS SMALL (10 P)` (₹50.00).
  - [ ] Jump to Section 23 (`GROUND CHAKKAR`) $\to$ Add 1 PKT `588- G C BIG T/MEENA` (₹120.00).
  - [ ] Review Order $\to$ Verify gross subtotal is ₹296.00.
  - [ ] Submit Order $\to$ Confirm order appears as `QUEUED` in Sync Service.

#### Scenario 2: Wholesale Bulk Order with Section Hopping
* **Customer:** `01149` (`NEW SHIVA BALAJI DASARWAR`).
* **Checklist:**
  - [ ] Open Section 7 (`CLASSIC SPARKLERS`) $\to$ Add 50 PKT of `221- 10 CM PLAIN CLASSIC`.
  - [ ] Tap "Skip to Next Section" $\to$ Verify screen jumps sequentially without freezing.
  - [ ] Jump directly via left sidebar to Section 30 (`ATOM BOMB`) $\to$ Add 20 PKT `735- BULLET BOMB MINI`.
  - [ ] Jump to Section 32 (`SHOTS & MULTISHOTS`) $\to$ Use search bar: type `"30"` $\to$ Add 5 boxes of `30 SHOTS`.
  - [ ] Apply negotiated bill discount: enter ₹200.00 in `less_amount`.
  - [ ] Verify net total = Gross - 200.
  - [ ] Submit Order.

#### Scenario 3: Offline Resiliency & Warehouse Dead-Zone Test
* **Goal:** Verify that a salesman walking into the tin-roof warehouse without WiFi can continue taking orders.
* **Checklist:**
  - [ ] Disable tablet WiFi (Airplane mode on).
  - [ ] Create 5-item order for customer `00394` (`QAYUM KHAN`).
  - [ ] Confirm item steppers work with zero latency using local IndexedDB/SQLite cache.
  - [ ] Tap "Submit Order" $\to$ App alerts: `"Saved Offline to Outbox"`.
  - [ ] Re-enable WiFi $\to$ Background worker auto-detects network and uploads draft.
  - [ ] Confirm draft status transitions from `QUEUED_OFFLINE` $\to$ `SYNCED`.

#### Scenario 4: Out-of-Stock Item Handling
* **Goal:** Verify behavior on items where `ITEMMST.CQTY <= 0`.
* **Checklist:**
  - [ ] Locate item `00079` (`119- ASST CARTOON`, stock -27).
  - [ ] Verify card shows clear **Amber/Red "Out of Stock" (CQTY: 0)** badge.
  - [ ] Confirm salesman can override with warning if customer confirms godown stock exists.

---

### Phase C: End-to-End FoxPro Ingestion Verification (Day 1, 14:00 - 17:00)
- [ ] **C1. Stage Orders:** Operator 2 executes `POST /api/import/stage`; inspects `import_staging.json`.
- [ ] **C2. Headless Import Execution:** Run `VFP6.EXE -T -C"CONFIG.FPW" IMPORT.PRG`.
- [ ] **C3. Counter Integrity:** Verify `BILLBOOK.ENTRY` incremented by exact count of processed orders.
- [ ] **C4. Header Verification (`SALEMST`):** Open `SALEMST.DBF` in FAVWIN; verify:
  - `ENTRY` matches assigned counter.
  - `NOTE` contains `"DRAFT:TAB01-XXXX"`.
  - `PCODE` and `PNAME` match customer.
  - `NAMT` matches tablet order total.
- [ ] **C5. Line Items (`SALETRN`):** Verify lines exist with correct `ICODE`, `QTY`, `RATE`, and `GAMT`.
- [ ] **C6. Ledger Postings (`LEDGER`):** Verify Debtor Debit and Sales Revenue Credit rows exist and balance to ₹0.00.
- [ ] **C7. Stock Deduction (`ITEMMST`):** Verify `SQTY` increased and `CQTY` decreased by sold quantities.
- [ ] **C8. Gate 4 Duplicate Protection:** Re-run `IMPORT.PRG` on the same staging payload; verify all orders skipped as `"DUPLICATE_SKIPPED"` and `BILLBOOK.ENTRY` does not increment.

---

### Phase D: Live Assisted-Selling Shadow Pilot (Day 2, Full Day)
- [ ] **D1. Live Shadowing:** Operator 1 shadows paper clipboard with tablet for 20 real walk-in customer interactions.
- [ ] **D2. Order Timing:** Time order creation from customer entrance to final total.
- [ ] **D3. End of Day Reconciliation:** Compare tablet orders against physical paper slips. Target: 100% agreement.

---

## 4. Success Metrics & Acceptance Criteria

| Metric | Baseline (Paper & Manual Billing) | Alpha Pilot Target | Minimum Acceptable Threshold |
|---|:---:|:---:|:---:|
| **Order Entry Time (10 Items)** | 6 – 8 minutes | **< 2.0 minutes** | < 3.5 minutes |
| **Section Switch Latency** | 5 – 10 seconds (flipping pages) | **< 200 ms (Instant tap)**| < 500 ms |
| **Catalog Search Retrieval** | 15 – 30 seconds | **< 300 ms** | < 1.0 second |
| **Sync Success Rate** | N/A | **100%** | 99.5% (Zero lost orders) |
| **Duplicate Prevention** | ~2% paper duplicate bills | **0.0% (Zero duplicates)**| 0.0% |
| **FoxPro Import Fidelity** | 100% manual typing | **100% automated match** | 100% exact math match |
| **Offline Recovery** | Manual rewrite | **100% auto-upload** | 100% auto-upload |
| **Operator Usability Score** | N/A | **$\ge$ 4.5 / 5.0** | $\ge$ 3.8 / 5.0 |

---

## 5. Rollback & Contingency Protocol

If any blocking defect occurs during Day 2 live shadowing:
1. **Immediate Fallback:** Sales staff reverts instantly to traditional paper order pads.
2. **Zero DBF Impact:** Because tablet orders reside in SQLite until explicitly staged and imported, corrupt or unverified drafts have zero effect on FoxPro files.
3. **Data Preservation:** Tablet local IndexedDB preserves all entered order drafts for post-mortem debugging.
