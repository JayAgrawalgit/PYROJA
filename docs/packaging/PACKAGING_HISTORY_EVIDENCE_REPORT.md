# PYROJA Packaging Rules Historical Sales Evidence & Recommendation Report

**Document Version:** 2.0.0 (Strengthened Rigorous Audit)  
**Date Generated:** September 19, 2026  
**Active Fiscal Year Dataset:** `legacy-software-extracted/FAVWIN/D2627` (2026-04-05 to 2026-08-29)  
**Total Scope Analyzed:** All 439 Packaging Rule Candidates (32 Currently Enforced Overlays + 407 Heuristic Candidates > 1)  
**Audit Integrity:** 100% Read-Only DBF Inspection. Zero database, stock, or code modifications. Strict 100.0% divisibility policy applied.  

---

## 1. Executive Summary

In FoxPro `ITEMMST.DBF`, the `QIB` (Quantity In Box) field is `1` across all 3,019 products and `PACK` represents the FoxPro billed unit of measure (`PKT`, `BOX`, `BUNDLE`, `BAG`), not the wholesale dispatch case multiple. Enforcing pack restrictions directly from unverified regex heuristics creates severe commercial risks, including false positives (e.g. multi-shot cake tube counts, garland cracker counts, matchbox master bundles) that would block legitimate wholesale orders with `422 Unprocessable Entity` errors.

To determine which pack multiples are safe and commercially justified, we audited the complete sales order history in `SALETRN.DBF` (3,612 transactions across 134 invoices and 60 distinct customer accounts) against all 439 candidate products. Under our strengthened audit protocol:
- **Eligible Wholesale Definition**: Transactions were filtered using customer master (`NAMEMST.DBF` `TCODE == 'SDEB'`) and invoice header (`SALEMST.DBF` `CD == 'D'`) validation, explicitly isolating walk-in cash retail (`99999`).
- **Strict 100.0% Divisibility Requirement**: A 95% threshold is strictly prohibited. `RECOMMEND_APPROVE` requires 100.0% divisibility across $\ge 2$ distinct wholesale customers, $\ge 3$ lines, and $\ge 2$ invoices.
- **Evidence-Based Divisor Analysis**: Alternate multiples are never chosen merely because a smaller number divides observed quantities. The Greatest Common Divisor (GCD) and all plausible common divisors are reported. Any ambiguity in physical packaging meaning results in `NEEDS_MANUAL_INVESTIGATION`.

### Key Audit Findings & Summary Matrix

| Recommendation Category | Total Count | % of Candidates | Empirical Validation Basis | Primary Operational Directive |
| :--- | :---: | :---: | :--- | :--- |
| **`RECOMMEND_APPROVE`** | **146** | **33.3%** | Strictly 100.0% wholesale divisibility across $\ge 2$ customers, $\ge 3$ lines, $\ge 2$ invoices | Eligible for business owner sign-off to enforce in `catalog_pack_rules.json` |
| **`RECOMMEND_CHANGE`** | **11** | **2.5%** | 100.0% compliance with an unambiguous alternate multiple supported by description and UOM | Adopt proven alternate multiple (4 for Cartoon 4P; 10 bags for Gold Bijali; 80 for Dhaga) |
| **`RECOMMEND_REJECT`** | **81** | **18.5%** | Wholesale dispatches frequently contain loose units (1, 2, 3, etc.) with GCD=1 | Reject multiple; keep enforced multiple at `1` to prevent blocking wholesale orders |
| **`INSUFFICIENT_HISTORY`** | **158** | **36.0%** | Zero sales (96 items) or single-customer/low-volume data (62 items) in D2627 | Maintain safe default `1`; monitor during Diwali peak season |
| **`NEEDS_MANUAL_INVESTIGATION`** | **43** | **9.8%** | Observed orders fail suggested multiple but have common divisor GCD > 1 not confirmed by text | Business owner must inspect physical packaging before setting multiple |
| **Total Candidates** | **439** | **100.0%** | Comprehensive audit across all active candidates | Business owner sign-off required prior to activation |

---

## 2. Eligible Wholesale Transaction Definition & Master Data Validation

To prevent non-wholesale, cancelled, or distorting transactions from skewing the audit:

### A. Customer Master Validation (`NAMEMST.DBF`)
- **Trade Debtor Account Standard**: Only customers with `TCODE == 'SDEB'` (Sundry Debtors) were treated as commercial wholesale accounts. In D2627, 59 distinct customers have `TCODE == 'SDEB'` (fireworks dealers, general stores, hardware centers across Maharashtra and Telangana).
- **Cash Counter Exclusion**: Customer `99999` (`CASH A/C`, `TCODE == '99999'`) was explicitly excluded (22 lines across 4 invoices: entries 19, 24, 104, 106). Because walk-in cash retail buyers are permitted to purchase loose units, excluding them prevents retail counter sales from polluting wholesale case-pack rules.
- **Non-Debtor Accounts**: Accounts with `TCODE` of `SCRE` (creditors/suppliers), `PURC` (purchases), `PAYA` (payables), `SALE` (sales ledger), `PLEX` (P&L expenses), `OSTO` (opening stock), and `DEXP` (direct expenses) had zero records in `SALETRN.DBF`.

### B. Invoice Header Reconciliation (`SALEMST.DBF`)
- Every one of the 3,612 sales lines in `SALETRN.DBF` was joined to `SALEMST.DBF` by `ENTRY`.
- **Zero Orphan Lines**: All 134 invoice entries in `SALETRN` exist in `SALEMST`. There are 0 orphan lines.
- **Header Verification**: All 134 invoice headers have `CD == 'D'` (Debit sales) and positive net amounts (`NAMT > 0` and `T4A > 0`). There are zero voided, cancelled, or zero-amount invoices.
- **Mathematical Reconciliation**: Line item sums mathematically reconcile with invoice headers (`sum(NAMT) - CDAMT = T4A` and `NAMT = T4A - LESS + ROFF`).
- **Customer & Date Integrity**: Line customer (`PCODE`) and date (`DATE`) matched header customer and date in 100.0% of records.

### C. Returns, Credit Notes & Deleted Entries
- **Sales Returns**: FoxPro records returns in `SALEMSTR.DBF` (headers) and `SALETRNR.DBF` (lines). In fiscal year D2627, both tables contain **0 records**. No sales returns occurred in this period.
- **Deleted Records**: Deleted FoxPro records are purged into `DELETRN.DBF` (2,623 historical records). `SALETRN.DBF` contains strictly active, valid transaction records.

### D. Documented Categories That Cannot Be Reliably Identified
1. **On-Account Showroom Samples**: If a wholesale trade customer visited the showroom counter and purchased an individual sample box on their trade credit account (`SDEB`), FoxPro records it as a normal invoice line under that customer. Master data fields cannot distinguish whether an order was an urgent single sample or an intended dispatch.
2. **Off-Invoice Bonus / Replacement Units**: If an item was given as a free promotional unit or replacement, but recorded at standard rate with an offsetting manual discount applied at the invoice header level (`LESS` or `CDAMT`), the individual line item appears as a standard sale.

---

## 3. Revised Strict Approval Policy (100.0% Requirement)

Under our hardened commercial rules:
1. **100.0% Divisibility Required**: Every single eligible wholesale sale must be strictly divisible by the candidate multiple ($Q_i \pmod M == 0$). A 95% threshold is strictly prohibited because even a single legitimate non-divisible wholesale order proves that FoxPro allowed that quantity, and enforcing the multiple would cause future `422 Unprocessable Entity` rejections.
2. **Volume Thresholds**: `RECOMMEND_APPROVE` requires:
   - At least 3 eligible wholesale invoice lines ($L_{ws} \ge 3$)
   - At least 2 distinct eligible wholesale customers ($C_{ws} \ge 2$)
   - At least 2 distinct eligible invoices ($I_{ws} \ge 2$)
3. **Non-Divisible Sales Action**: Any non-divisible eligible historical sale automatically leads to `RECOMMEND_REJECT` (if GCD=1) or `NEEDS_MANUAL_INVESTIGATION` (if GCD>1), **never approval**.

---

## 4. Revised Alternate-Multiple Selection Logic (GCD & Divisor Evidence)

In the prior audit, an automated divisor search picked smaller numbers if they divided observed quantities. This created a false-positive risk of adopting coincidental divisors (e.g. picking 5 when an item is sold loose in 5, 10, 15).

Under the strengthened logic:
1. **No Automatic Smaller Multiples**: A smaller multiple is never recommended merely because it mathematically divides observed quantities.
2. **Evidence Reporting**: The Greatest Common Divisor (GCD) and all plausible common divisors are reported as empirical evidence.
3. **Unambiguous Standard for `RECOMMEND_CHANGE` (11 Products)**: A change is recommended ONLY when the sellable packaging unit is **completely unambiguous** from product UOM, description, and transaction history:
   - `00080` & `00081` (Cartoon Sparklers): Description explicitly specifies `4P` (`ASST CARTOON BEN TEN (25P)... 4P`). 100.0% of wholesale orders across 7 and 8 customers are multiples of 4 packets. Recommended: `4`.
   - `00610` & `00611` (G C Big Sparklers): Description explicitly specifies `(4P)`. 100.0% of orders across 5 and 7 customers are multiples of 4 packets. Recommended: `4`.
   - `04309` - `04317` (Gold Bijali, 6 products): Descriptions note `(100 PCS)` cracker count, but billing UOM is `BAG` and 100.0% of wholesale orders across 3 to 11 customers are in multiples of 10 bags, exactly matching the approved Red Bijali overlay standard of 10 bags. Recommended: `10`.
   - `04042` (`DHAGA (80 DABBI)`): Current overlay enforces 1, but billing UOM is `PKT` at ₹6.00 and 100.0% of wholesale orders across 6 customers are in multiples of 80 packets (₹480/bundle). Recommended: `80`.
4. **`NEEDS_MANUAL_INVESTIGATION` Standard (43 Products)**: All other items with GCD > 1 where the description does not explicitly corroborate the smaller multiple are marked as `NEEDS_MANUAL_INVESTIGATION`. For example:
   - `00109` (`9 CM PLAIN INDRA (10 DABBI=1BOX)`): Orders are multiples of 5, but description says `(10 DABBI=1BOX)`. Does an inner pack of 5 exist, or did customers order half boxes? Requires physical inventory check.
   - `02152` & `02153` (`RING CAPS (1OOPKT= 1 BOX)`): Orders are multiples of 50 packets (half-boxes). Business owner must decide whether to allow half-boxes (50) or require full boxes (100).
   - `05402` & `05403` (`FLOWER POTS SUP DLX (2 P)`): Orders are multiples of 5, contradicting the description tag `(2 P)`. Requires verification.

---

## 5. Audit of the 32 Currently Active Overlay Rules

A dedicated risk audit was performed on all 32 rules currently active in `catalog_pack_rules.json` (see [`ACTIVE_RULE_RISK_REGISTER.md`](./ACTIVE_RULE_RISK_REGISTER.md)):

1. **`SAFE_FOR_PILOT` (21 Rules)**: Verified with strictly 100.0% divisibility across $\ge 2$ customers and $\ge 3$ lines in D2627:
   - Red/Stripped Bijali 10-bag outer packs: `00178`, `00181`, `00183`, `00184`, `04301`, `04303`, `04305`.
   - Chorsa 50-packet bundles: `00223`, `00224`, `00225`.
   - Bundle items billed per bundle (enforcing 1): `00082`, `00083`, `00186`, `03088`.
   - Loose-pack fancy items (enforcing 1): `00079`, `00455`, `00456`, `02157`, `04613`, `04616`, `04625`.

2. **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF` (11 Rules)**:
   - **Rule `04042` (`DHAGA (80 DABBI)`)**: Currently enforces 1, but wholesale dispatches are strictly in multiples of 80 packets (₹480/bundle). Changing to 80 required.
   - **Zero-Sales Rules (6 items)**: `00180`, `00182`, `00185`, `04192`, `05933`, `06106`.
   - **Low-Volume Rules (4 items)**: `00187` (2 lines), `02905` (2 lines), `04302` (2 lines), `04306` (1 line).

---

## 6. Complete 439-Product Decision Reference Tables

The complete dataset is exported to [`PACKAGING_RULE_DECISIONS.csv`](./PACKAGING_RULE_DECISIONS.csv). Below are the reference tables grouped by recommendation category:

### Category 1: RECOMMEND_APPROVE (146 Products)
*Strictly 100.0% wholesale divisibility across >= 2 customers, >= 3 lines, >= 2 invoices.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | GCD | Plausible Divisors | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00079` | 119- ASST CARTOON(10 PCS)DUR | `PKT` | ₹13.50 | 1 | 1 | 3 | 3 | 100.0% | 4 | `[2, 4]` | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical wholesale sales across 3 customers confirm single... |
| `00082` | 124- BIG NAGGOLI PANDYAN BLA | `BUNDLE` | ₹150.00 | 1 | 1 | 15 | 15 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 15 customers confirm singl... |
| `00083` | 125- BIG NAGGOLI PANDYAN RED | `BUNDLE` | ₹155.00 | 1 | 1 | 6 | 6 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 6 customers confirm single... |
| `00110` | 179- 9 CM COL INDRA (10 DABB | `BOX` | ₹69.50 | 10 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00132` | 221- 10 CM PLAIN CLASSIC (5  | `PKT` | ₹12.50 | 5 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00133` | 222- 10 CM COL CLASSIC (5 P) | `PKT` | ₹13.50 | 5 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00134` | 223- 10 CM GREEN CLASSIC (5  | `PKT` | ₹13.00 | 5 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00136` | 224- 10 CM RED CLASSIC(5 P) | `PKT` | ₹13.50 | 5 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00137` | 225- 10 CM 2 IN 1 CLASSIC(5  | `PKT` | ₹13.50 | 5 | 1 | 13 | 13 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 13 customers are divisible... |
| `00138` | 226- 12 CM PLAIN LX CLASSIC  | `PKT` | ₹14.50 | 5 | 1 | 11 | 11 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00139` | 227- 12 CM COL LX CLASSIC (5 | `PKT` | ₹15.50 | 5 | 1 | 12 | 12 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `00140` | 228- 12 CM PLAIN DLX CLASSIC | `PKT` | ₹16.50 | 5 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00142` | 229- 12 CM COL DLX CLASSIC ( | `PKT` | ₹17.50 | 5 | 1 | 3 | 3 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00143` | 230- 12 CM GREEN LX CLASSIC  | `PKT` | ₹14.75 | 5 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00178` | 148- RED BIJALI ROSE (100 P | `BAG` | ₹17.50 | 10 | 10 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 10 customers confirm 100.0... |
| `00181` | 150- RED BIJALI AYYANAR (100 | `BAG` | ₹30.00 | 10 | 10 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 7 customers confirm 100.0%... |
| `00183` | 152- RED BIJALI S.T.D.(100 P | `BAG` | ₹53.00 | 10 | 10 | 12 | 12 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 12 customers confirm 100.0... |
| `00184` | 153- RED BIJALI SONY (100 PC | `BAG` | ₹60.00 | 10 | 10 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | Historical wholesale sales across 3 customers confirm 100.0%... |
| `00186` | 290- 10 CHORASA MUNNA DURGES | `BUNDLE` | ₹335.00 | 1 | 1 | 7 | 7 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 7 customers confirm single... |
| `00223` | 293- 16 CHORSA B GROUP (50P= | `PKT` | ₹7.25 | 50 | 50 | 9 | 9 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **50** | HIGH | Historical wholesale sales across 9 customers confirm 100.0%... |
| `00224` | 294- 28 CHORSA K.R.K (50P= 1 | `PKT` | ₹12.00 | 50 | 50 | 15 | 15 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **50** | HIGH | Historical wholesale sales across 15 customers confirm 100.0... |
| `00225` | 295- 28 CHORSA TAJ  T/MEENA  | `PKT` | ₹13.25 | 50 | 50 | 3 | 3 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **50** | MEDIUM | Historical wholesale sales across 3 customers confirm 100.0%... |
| `00250` | 308- 20 DLX KING GANESH DURA | `PKT` | ₹25.50 | 10 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00252` | 310- 24 DLX RAGURAM ( 10 P) | `PKT` | ₹30.00 | 10 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00253` | 311- 24 DLX GANESH DURAI( 10 | `PKT` | ₹32.00 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00255` | 313- 28 DLX RAGURAM(10 P) | `PKT` | ₹37.50 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00256` | 314- 32 DLX KICK SHOT BALAJI | `PKT` | ₹65.00 | 5 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00257` | 315- 48 DLX RAGURAM ( 5 P) | `PKT` | ₹50.00 | 5 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00288` | 329- 2' PARROT AYYANAR (25 P | `PKT` | ₹5.00 | 25 | 1 | 3 | 3 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00289` | 330- 2 3/4 KURVI DURGESH (25 | `PKT` | ₹6.50 | 25 | 1 | 7 | 7 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `00291` | 331- 2 3/4 KURVI VELVAN (10  | `PKT` | ₹7.50 | 10 | 1 | 5 | 5 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00292` | 332- 2 3/4 KURVI GEMS (25 P) | `PKT` | ₹7.75 | 25 | 1 | 5 | 5 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00293` | 333- 2 3/4 GREEN PARROT PONM | `PKT` | ₹9.50 | 25 | 1 | 4 | 4 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00297` | 337- 3 1/2 BEN TEN DURGESH/J | `PKT` | ₹9.50 | 15 | 1 | 4 | 4 | 100.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `RECOMMEND_APPROVE` | **15** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00298` | 338- 3 1/2 JOKER SADA BAJAJI | `PKT` | ₹10.75 | 10 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00299` | 339- 3 1/2 MIX LABEL SADA AY | `PKT` | ₹13.50 | 10 | 1 | 6 | 6 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00300` | 340- 3 1/2 GREEN PARROT PONM | `PKT` | ₹14.00 | 10 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `00301` | 341- 3 1/2 ELEPHANT I.N(10 P | `PKT` | ₹14.50 | 10 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00325` | 399- 2 SOUND DHAMAKA RAJHARI | `PKT` | ₹22.00 | 10 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00326` | 400- 2 SOUND DHAMAKA NM JYOT | `PKT` | ₹25.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00328` | 402- 2 SOUND DHAMAKA I.N. (1 | `PKT` | ₹30.00 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00427` | 444- FLOWER POTS SMALL RAJLA | `PKT` | ₹38.00 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `00455` | 534- JADUGAR UV.BOX AYYAN (4 | `PKT` | ₹260.00 | 1 | 1 | 9 | 9 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 9 customers confirm single... |
| `00456` | 535- MANORANJAN U.V.BOX AYYA | `PKT` | ₹260.00 | 1 | 1 | 7 | 7 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 7 customers confirm single... |
| `00491` | 550- SADA MATKA ANAR OTHER ( | `PCS` | ₹15.00 | 100 | 1 | 6 | 6 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `RECOMMEND_APPROVE` | **100** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00536` | 591- G C BIG W MERCURY(10 P) | `PKT` | ₹44.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00565` | 708- 18 T STAR SRIPATHI(10P) | `PKT` | ₹16.00 | 10 | 1 | 6 | 6 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00567` | 710- 48 T STAR (10P) SRIPATH | `PKT` | ₹50.00 | 10 | 1 | 12 | 12 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `00614` | 735- BULLET BOMB MINI SRI AT | `PKT` | ₹14.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00615` | 736- MINI BULLET BOMB T/MEEN | `PKT` | ₹16.50 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00616` | 737- BULLET BOMB MINI SRIPAT | `PKT` | ₹18.00 | 10 | 1 | 6 | 6 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00617` | 738- BULLET BOMB MEDIUM T/ME | `PKT` | ₹21.00 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00618` | 739- BULLET BOMB MEDIUM APPL | `PKT` | ₹21.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00621` | 742- BULLET BOMB BIG DLX T/M | `PKT` | ₹32.50 | 10 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00630` | 751- SOLDIER BOMB GREEN W/G  | `PKT` | ₹75.00 | 10 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00707` | 138- GANGA JAMUNA SRI PATHI( | `PKT` | ₹45.00 | 5 | 1 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `00769` | 600- G C ASOKA W MERCURY(10  | `PKT` | ₹67.50 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00848` | 231- 12 CM RED LX CLASSIC (5 | `PKT` | ₹17.50 | 5 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `01167` | 139- GANGA JAMUNA OVEETA(5P) | `PKT` | ₹52.00 | 5 | 1 | 7 | 7 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `01176` | 141- GANGA JAMUNA MERCURY( 5 | `PKT` | ₹65.00 | 5 | 1 | 4 | 3 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `02154` | 1119- RING CAPS (1OOPKT= 1 B | `PKT` | ₹7.00 | 100 | 1 | 3 | 3 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `RECOMMEND_APPROVE` | **100** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `02157` | 1121- MISSILE SIREN(127X1)TI | `PKT` | ₹65.00 | 1 | 1 | 13 | 13 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 13 customers confirm singl... |
| `02660` | 666- BABY ROCKET RAJ LAXMI ( | `PKT` | ₹30.00 | 10 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `02676` | 667- COLOUR ROCKET AYYANAR ( | `PKT` | ₹48.50 | 10 | 1 | 6 | 6 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `02680` | 671- ROCKET BOMB (10P) 5P AY | `PKT` | ₹55.00 | 5 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `02681` | 672- ROCKET BOMB (10P) 5P GA | `PKT` | ₹58.00 | 5 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `02756` | 606- G C SPL (10 P) VENKATES | `PKT` | ₹36.00 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `02765` | 232- 12 CM 2 IN 1 CLASSIC(5  | `PKT` | ₹17.00 | 5 | 1 | 13 | 13 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 13 customers are divisible... |
| `02852` | 607- G C SPL (10 P) T/MEENA | `PKT` | ₹56.00 | 10 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `03088` | 114- R & G MATCH BOX SHANTHI | `BUNDLE` | ₹500.00 | 1 | 1 | 7 | 7 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | HIGH | Historical wholesale sales across 7 customers confirm single... |
| `03097` | 235- 15 CM PLAIN AB MAGIC CL | `PKT` | ₹22.00 | 5 | 1 | 18 | 17 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 17 customers are divisible... |
| `03098` | 236- 15 CM PLAIN DLX CLASSIC | `PKT` | ₹25.00 | 5 | 1 | 6 | 6 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `03099` | 237- 15 CM PLAIN BOXE(2P CEL | `PKT` | ₹26.00 | 2 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **2** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03100` | 238- 15 CM COL AB MAGIC CLAS | `PKT` | ₹25.00 | 5 | 1 | 12 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `03101` | 239- 15 CM COL DLX CLASSIC ( | `PKT` | ₹27.50 | 5 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03103` | 241- 15 CM GREEN CLASSIC (5  | `PKT` | ₹23.00 | 5 | 1 | 16 | 15 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03104` | 242- 15 CM RED CLASSIC  (5 P | `PKT` | ₹27.50 | 5 | 1 | 11 | 11 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `03105` | 243- 15 CM 2 IN 1 CLASSIC (5 | `PKT` | ₹29.00 | 5 | 1 | 15 | 15 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03110` | 248- 30 CM PLAIN AB MAGIC CL | `PKT` | ₹22.00 | 5 | 1 | 15 | 15 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03208` | 608- G C SPL (10 P) GANESH | `PKT` | ₹57.50 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03231` | 721- 10 CM PENCIL VIRBALAJI  | `PKT` | ₹36.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03266` | 754- LALKAR BOMB GREEN W/F(1 | `PKT` | ₹85.00 | 10 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04048` | 1091- ROBOT BLACK S-61 SOM ( | `PCS` | ₹12.50 | 12 | 1 | 6 | 6 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04051` | 1094- 86 BLACK SOM(12 PCS) | `PCS` | ₹17.50 | 12 | 1 | 3 | 3 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04052` | 1095- 86 COLOUR SOM (12 PCS) | `PCS` | ₹23.00 | 12 | 1 | 5 | 5 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04053` | 1096- NICE BLACK SOM(12 PCS) | `PCS` | ₹18.00 | 12 | 1 | 6 | 6 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04054` | 1097- NICE COLOUR SOM (12 PC | `PCS` | ₹23.50 | 12 | 1 | 6 | 6 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04056` | 1099- VATMAN COLOUR SOM (12  | `PCS` | ₹26.00 | 12 | 1 | 7 | 7 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04057` | 1100- DOLPHIN BLACK SOM(6 PC | `PCS` | ₹29.00 | 6 | 1 | 4 | 4 | 100.0% | 6 | `[2, 3, 6]` | `RECOMMEND_APPROVE` | **6** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04058` | 1101- DOLPHIN COLOUR SOM (6  | `PCS` | ₹37.00 | 6 | 1 | 8 | 8 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `RECOMMEND_APPROVE` | **6** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04094` | 1084- PATANG BALLOON (10 P)  | `BOX` | ₹16.50 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04246` | 251- 30 CM COL AB MAGIC CLAS | `PKT` | ₹25.00 | 5 | 1 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04247` | 252- 30 CM COL DLX CLASSIC ( | `PKT` | ₹27.50 | 5 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04249` | 254- 30 CM GREEN CLASSIC (5  | `PKT` | ₹23.00 | 5 | 1 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04251` | 256- 30 CM RED CLASSIC (5 P) | `PKT` | ₹27.00 | 5 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04253` | 258- 30 CM 2 IN 1 CLASSIC (5 | `PKT` | ₹27.00 | 5 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04301` | 159- STRIPPED BIJALI MERCURY | `BAG` | ₹25.50 | 10 | 10 | 5 | 5 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 5 customers confirm 100.0%... |
| `04303` | 161- STRIPPED BIJALI AYYANAR | `BAG` | ₹32.00 | 10 | 10 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 7 customers confirm 100.0%... |
| `04305` | 163- STRIPPED BIJALI GAINT S | `BAG` | ₹50.00 | 10 | 10 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | Historical wholesale sales across 3 customers confirm 100.0%... |
| `04341` | 296- 28 CHORSA TURKEY  RAJLA | `PKT` | ₹13.50 | 50 | 1 | 3 | 3 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **50** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04346` | 301- 28 GAINT CHORSA (25 P)  | `PKT` | ₹17.50 | 25 | 1 | 9 | 9 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04348` | 303- 28 GAINT CHORSA (25 P)  | `PKT` | ₹19.00 | 25 | 1 | 7 | 7 | 100.0% | 25 | `[5, 25]` | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04351` | 316- 50 DLX RAGURAM ( 5 P) | `PKT` | ₹52.00 | 5 | 1 | 8 | 8 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04370` | 342- 3 1/2 GREEN PARROT W/F  | `PKT` | ₹15.00 | 10 | 1 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04378` | 350- 4 GREEN PARROT SADA VEL | `PKT` | ₹14.50 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04381` | 353- 4 MICKEY MOUSE BALAJI(  | `PKT` | ₹16.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04382` | 354- 4 GREEN PARROT VELAVAN  | `PKT` | ₹18.50 | 10 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04383` | 355- 4 ELEPHANT I.N (10 P) | `PKT` | ₹18.50 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04384` | 356- 4 GREEN PARROT SADA PON | `PKT` | ₹19.50 | 10 | 1 | 6 | 6 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04385` | 357- 4  MIX LABEL AYYANAR (1 | `PKT` | ₹21.00 | 10 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04386` | 358- 4 PARROT COCK (10 P) | `PKT` | ₹22.50 | 10 | 1 | 5 | 5 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04400` | 372- 4 DLX PARROT W/F ( 10 P | `PKT` | ₹29.00 | 10 | 1 | 12 | 12 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `04405` | 377- 4 SUP DLX MIX LABEL(10P | `PKT` | ₹27.00 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04411` | 383- 5 DLX JALLIKATTI DURGES | `PKT` | ₹27.00 | 10 | 1 | 4 | 4 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04434` | 409- 3 SOUND DHAMAKA RATHANA | `PKT` | ₹34.00 | 10 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04581` | 622- G C DLX  (10 P) 5 P T/M | `PKT` | ₹95.00 | 5 | 1 | 8 | 8 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04583` | 624- G C DLX  (10 P) 5 P MER | `PKT` | ₹125.00 | 5 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04584` | 625- G C DLX  (10 P) 5 P COL | `PKT` | ₹115.00 | 5 | 1 | 7 | 7 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04585` | 626- G C DLX  W (10 P) 5 P I | `PKT` | ₹130.00 | 5 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04586` | 627- G C DLX  (10 P) 5 P GAN | `PKT` | ₹140.00 | 5 | 1 | 7 | 7 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04589` | 630- G C DLX  (10 P) 5 P S.T | `PKT` | ₹195.00 | 5 | 1 | 6 | 6 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04590` | 631- 70 CM G C DLX  (10 P) 5 | `PKT` | ₹210.00 | 5 | 1 | 12 | 11 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04592` | 633- G C DLX  U.V. BOX (10 P | `PKT` | ₹135.00 | 5 | 1 | 4 | 4 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04595` | 636- G C DLX SPINNER ( 10 P  | `PKT` | ₹160.00 | 10 | 1 | 7 | 7 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04596` | 637- G C DLX  SPINNER(10P) 5 | `PKT` | ₹175.00 | 5 | 1 | 5 | 5 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04613` | 650- SUDARSHAN CHAKKAR ANIL  | `PKT` | ₹153.00 | 1 | 1 | 4 | 4 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical wholesale sales across 4 customers confirm single... |
| `04616` | 653- GIANT WHEEL AYYAN (5 PC | `PKT` | ₹175.00 | 1 | 1 | 4 | 4 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical wholesale sales across 4 customers confirm single... |
| `04619` | 656- WHISTLING WHEEL COCK (5 | `PKT` | ₹125.00 | 5 | 1 | 9 | 9 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04621` | 658- TITANIC WHEEL DURGESH ( | `PKT` | ₹130.00 | 5 | 1 | 5 | 5 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04625` | 662- SKY  WHEEL AYYAN (5 PCS | `PKT` | ₹345.00 | 1 | 1 | 3 | 3 | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical wholesale sales across 3 customers confirm single... |
| `04636` | 675- SILVER ROCKET(10P)5P AY | `PKT` | ₹75.00 | 5 | 1 | 3 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04639` | 678- LUNIK ROCKET (10 P) 2P  | `PKT` | ₹80.00 | 2 | 1 | 10 | 10 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04641` | 680- LUNIK ROCKET (10 P) 2P  | `PKT` | ₹112.00 | 2 | 1 | 6 | 6 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04646` | 685- 2 SOUND ROCKET (10 P) 2 | `PKT` | ₹82.00 | 2 | 1 | 12 | 12 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `04647` | 686- 2 SOUND ROCKET (10 P) 2 | `PKT` | ₹120.00 | 2 | 1 | 5 | 5 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04649` | 688- 2 SOUND ROCKET (10 P) 2 | `PKT` | ₹125.00 | 2 | 1 | 6 | 6 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04679` | 724- 15 CM PENCIL VIRBALAJI  | `PKT` | ₹53.00 | 10 | 1 | 8 | 8 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04684` | 729- MULTI COLOUR CANDLE S.T | `PKT` | ₹99.00 | 5 | 1 | 4 | 4 | 100.0% | 5 | `[5]` | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04910` | 1008- 18 HAND SHOT ( 2 PCS ) | `BOX` | ₹400.00 | 2 | 1 | 3 | 3 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `05426` | 692- 3 SOUND ROCKET (10 P) 2 | `PKT` | ₹85.00 | 2 | 1 | 8 | 8 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `05428` | 694- 3 SOUND ROCKET (10 P) 2 | `PKT` | ₹140.00 | 2 | 1 | 5 | 5 | 100.0% | 2 | `[2]` | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `06134` | W COLD PYRO R&G BOX 3.M.35.S | `BOX` | ₹80.00 | 6 | 1 | 3 | 3 | 100.0% | 6 | `[2, 3, 6]` | `RECOMMEND_APPROVE` | **6** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `06135` | W COLD PYRO YELLO BOX 3.M.30 | `BOX` | ₹120.00 | 10 | 1 | 4 | 3 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `06171` | 129- KIT-KAT(10 P)YUVA | `PKT` | ₹18.50 | 10 | 1 | 11 | 11 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `06173` | 131- KIT-KAT (10 P) RAJHARIS | `PKT` | ₹20.00 | 10 | 1 | 9 | 9 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `06174` | 132- KIT-KAT(10 P)U.V.BOX VE | `PKT` | ₹21.00 | 10 | 1 | 10 | 10 | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |

### Category 2: RECOMMEND_CHANGE (11 Products)
*100.0% compliance with unambiguous alternate multiples directly confirmed by description/UOM.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | GCD | Plausible Divisors | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00080` | 120- ASST CARTOON BEN TEN(25 | `PKT` | ₹55.00 | 25 | 1 | 7 | 7 | 0.0% | 4 | `[2, 4]` | `RECOMMEND_CHANGE` | **4** | HIGH | Suggested multiple 25 contradicted (0.0% div), but product d... |
| `00081` | 121- SNAKE CARTOON(25P)SAMLL | `PKT` | ₹55.00 | 25 | 1 | 8 | 8 | 0.0% | 4 | `[2, 4]` | `RECOMMEND_CHANGE` | **4** | HIGH | Suggested multiple 25 contradicted (0.0% div), but product d... |
| `00610` | 595- G C BIG T/MEENA (25 PCS | `PKT` | ₹75.00 | 25 | 1 | 5 | 5 | 0.0% | 4 | `[2, 4]` | `RECOMMEND_CHANGE` | **4** | HIGH | Suggested multiple 25 contradicted (0.0% div), but product d... |
| `00611` | 596- G C BIG GANESH (25 PCS) | `PKT` | ₹80.00 | 25 | 1 | 7 | 7 | 0.0% | 4 | `[2, 4]` | `RECOMMEND_CHANGE` | **4** | HIGH | Suggested multiple 25 contradicted (0.0% div), but product d... |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | `PKT` | ₹6.00 | 1 | 1 | 6 | 6 | 100.0% | 80 | `[2, 4, 5, 8, 10, 16, 20, 40, 80]` | `RECOMMEND_CHANGE` | **80** | HIGH | Current overlay enforces 1 (assuming bundle billing), but bi... |
| `04309` | 167- GOLD BIJALI A.G.S (50 P | `BAG` | ₹11.00 | 50 | 1 | 11 | 11 | 72.7% | 10 | `[2, 5, 10]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 50 represents cracker count per bag, but ... |
| `04311` | 169- GOLD BIJALI OTHER (100  | `BAG` | ₹20.00 | 100 | 1 | 7 | 7 | 71.4% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 100 represents cracker count per bag, but... |
| `04312` | 170- GOLD BIJALI A.G.S(100 P | `BAG` | ₹21.00 | 100 | 1 | 6 | 6 | 50.0% | 10 | `[2, 5, 10]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 100 represents cracker count per bag, but... |
| `04315` | 173- GOLD BIJALI SRIPATHI(10 | `BAG` | ₹30.00 | 100 | 1 | 3 | 3 | 33.3% | 10 | `[2, 5, 10]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 100 represents cracker count per bag, but... |
| `04316` | 174- GOLD BIJALI AYYANAR(100 | `BAG` | ₹37.50 | 100 | 1 | 3 | 3 | 66.7% | 10 | `[2, 5, 10]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 100 represents cracker count per bag, but... |
| `04317` | 175- GOLD BIJALI COCK(100 PC | `BAG` | ₹67.00 | 100 | 1 | 4 | 4 | 25.0% | 10 | `[2, 5, 10]` | `RECOMMEND_CHANGE` | **10** | HIGH | Suggested multiple 100 represents cracker count per bag, but... |

### Category 3: NEEDS_MANUAL_INVESTIGATION (43 Products)
*Orders fail suggested multiple but have common divisor GCD > 1 not explicitly confirmed by text.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | GCD | Plausible Divisors | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00109` | 178- 9 CM PLAIN INDRA (10 DA | `BOX` | ₹65.00 | 10 | 1 | 5 | 5 | 80.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (80.0% div), but common di... |
| `00502` | 559- DELUXE GUDIYA ( 4 PCS) | `BOX` | ₹500.00 | 4 | 1 | 1 | 1 | 0.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `00537` | 592- G C BIG R/G S.T.D (25 P | `PKT` | ₹53.00 | 25 | 1 | 1 | 1 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `00609` | 594- G C BIG VENKATESH (25 P | `PKT` | ₹45.00 | 25 | 1 | 1 | 1 | 0.0% | 16 | `[2, 4, 8, 16]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `00691` | 122- RAJDHANI RAIL(10 PCS)AY | `PKT` | ₹65.00 | 10 | 1 | 4 | 4 | 50.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (50.0% div), but common di... |
| `00876` | 601- G C ASOKA BIG SIZE GANE | `PKT` | ₹72.50 | 10 | 1 | 7 | 7 | 85.7% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (85.7% div), but common di... |
| `00925` | 602- G C ASOKA S.T.D (10 P)  | `PKT` | ₹88.00 | 10 | 1 | 9 | 9 | 55.6% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (55.6% div), but common di... |
| `02081` | 142- MAGIC FOUNTAIN OVEEYA(1 | `PKT` | ₹120.00 | 10 | 1 | 3 | 3 | 33.3% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (33.3% div), but common di... |
| `02152` | 1117- RING CAPS (1OOPKT= 1 B | `PKT` | ₹6.00 | 100 | 1 | 3 | 3 | 33.3% | 50 | `[2, 5, 10, 25, 50]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 100 (33.3% div), but common d... |
| `02153` | 1118- RING CAPS (1OOPKT= 1 B | `PKT` | ₹6.50 | 100 | 1 | 10 | 10 | 80.0% | 50 | `[2, 5, 10, 25, 50]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 100 (80.0% div), but common d... |
| `02669` | 567- DANCING BUTTERFLY R/G.( | `PKT` | ₹45.00 | 10 | 1 | 12 | 12 | 75.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (75.0% div), but common di... |
| `02897` | W 2 1/2" F. PIPE(3 PCS)AYYAN | `PKT` | ₹225.00 | 3 | 1 | 3 | 2 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 3 (0.0% div), but common divi... |
| `03089` | 183- 7 CM PLAIN M.R.P. (10 D | `BOX` | ₹80.00 | 10 | 1 | 3 | 3 | 66.7% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (66.7% div), but common di... |
| `03090` | 184- 7 CM COL SARAVANA(10 DA | `BOX` | ₹90.00 | 10 | 1 | 3 | 3 | 66.7% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (66.7% div), but common di... |
| `03091` | 185- 7 CM GREEN SARAVANA (10 | `BOX` | ₹105.00 | 10 | 1 | 2 | 2 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `03093` | 187- 7 CM COL VASANTHA(10 DA | `BOX` | ₹95.00 | 10 | 1 | 1 | 1 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `03107` | 245- 15 CM 2IN1 BOXE(2P CELL | `PKT` | ₹31.00 | 2 | 1 | 1 | 1 | 0.0% | 45 | `[3, 5, 9, 15, 45]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `03214` | 614- 45 CM G C SPL (10 P) CO | `PKT` | ₹124.00 | 10 | 1 | 8 | 8 | 87.5% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (87.5% div), but common di... |
| `03222` | 702- MULTI COLOUR ROCKET MER | `PKT` | ₹113.00 | 6 | 1 | 7 | 7 | 71.4% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 6 (71.4% div), but common div... |
| `03265` | 753- L. B. BOMB GREEN W/F (1 | `PKT` | ₹80.00 | 10 | 1 | 3 | 3 | 66.7% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (66.7% div), but common di... |
| `03272` | 760- THUNDER BOMB GREEN (10  | `PKT` | ₹130.00 | 10 | 1 | 3 | 3 | 33.3% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 10 (33.3% div), but common di... |
| `03275` | 763- V.I.P BOMB GREEN S.Q (6 | `PKT` | ₹140.00 | 6 | 1 | 1 | 1 | 0.0% | 20 | `[2, 4, 5, 10, 20]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04009` | 845- 7 SHOTS ANIL (5 PCS) (5 | `BOX` | ₹170.00 | 5 | 1 | 1 | 1 | 0.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04014` | 850- 7 SHOTS I. N.(10 PCS | `BOX` | ₹270.00 | 10 | 1 | 2 | 2 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04050` | 1093- V-35 BLACK VISHNU(10 P | `PCS` | ₹15.00 | 10 | 1 | 1 | 1 | 0.0% | 48 | `[2, 3, 4, 6, 8, 12, 16, 24, 48]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04055` | 1098- VATMAN BLACK SOM (12 P | `PCS` | ₹21.00 | 12 | 1 | 9 | 9 | 88.9% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 12 (88.9% div), but common di... |
| `04060` | 1103- TIGER COLOUR SOM (12 P | `PCS` | ₹67.50 | 12 | 1 | 2 | 2 | 0.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04062` | 1105- SPIDER BLACK SOM ( 3 P | `PCS` | ₹89.00 | 3 | 1 | 3 | 3 | 66.7% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | MEDIUM | Orders fail suggested multiple 3 (66.7% div), but common div... |
| `04063` | 1106- SPIDER COLOUR SOM  ( 3 | `PCS` | ₹97.00 | 3 | 1 | 2 | 2 | 50.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04064` | 1107- CAMANDO BLACK SOM ( 3  | `PCS` | ₹102.00 | 3 | 1 | 2 | 2 | 0.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04065` | 1108- CAMANDO COLOUR SOM ( 3 | `PCS` | ₹109.00 | 3 | 1 | 2 | 2 | 0.0% | 2 | `[2]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04207` | 189- 7 CM COL GOLD S.T.D(10D | `BOX` | ₹150.00 | 10 | 1 | 1 | 1 | 0.0% | 3 | `[3]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04313` | 171- GOLD BIJALI GIANT OVEEY | `BAG` | ₹44.00 | 100 | 1 | 2 | 2 | 50.0% | 10 | `[2, 5, 10]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04314` | 172- GOLD BIJALI APPLE(100 P | `BAG` | ₹27.00 | 100 | 1 | 2 | 2 | 0.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04423` | 395- 4 SUP DLX GOLD KARUDA ( | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 50.0% | 25 | `[5, 25]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04574` | 615- G C SPL (10 P) (5 P) S. | `PKT` | ₹150.00 | 10 | 1 | 2 | 2 | 50.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (2 line(s), 2 cust(s)) with non-divisible sales [... |
| `04601` | 642- G C SUP DLX  (10 P) 5 P | `PKT` | ₹215.00 | 5 | 1 | 1 | 1 | 0.0% | 4 | `[2, 4]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04628` | 665- STAR WHEEL (10 PCS) AYY | `PKT` | ₹156.00 | 10 | 1 | 1 | 1 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |
| `04680` | 725- 18 CM PENCIL VIRBALAJI  | `PKT` | ₹68.00 | 10 | 1 | 6 | 6 | 16.7% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (16.7% div), but common di... |
| `04915` | 1013- SKY SHOT (10 P ) COCK | `BOX` | ₹86.00 | 10 | 1 | 10 | 10 | 70.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 10 (70.0% div), but common di... |
| `05402` | 513- FLOWER POTS SUP DLX (2  | `PKT` | ₹65.00 | 2 | 1 | 7 | 7 | 42.9% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 2 (42.9% div), but common div... |
| `05403` | 514- FLOWER POTS SUP DLX (2  | `PKT` | ₹75.00 | 2 | 1 | 7 | 7 | 28.6% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | HIGH | Orders fail suggested multiple 2 (28.6% div), but common div... |
| `06098` | W 2 1/2" F. PIPE 2 IN 1 ( 2  | `BOX` | ₹200.00 | 2 | 1 | 1 | 1 | 0.0% | 5 | `[5]` | `NEEDS_MANUAL_INVESTIGATION` | **1** | LOW | Low volume (1 line(s), 1 cust(s)) with non-divisible sales [... |

### Category 4: RECOMMEND_REJECT (81 Products)
*Wholesale dispatches contain loose units (1, 2, 3) with GCD=1. Product is sold unconstrained.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | GCD | Plausible Divisors | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00111` | 180- 9 CM PLAIN CLASSIC (10D | `BOX` | ₹78.50 | 10 | 1 | 5 | 5 | 40.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (40.0% div; non-... |
| `00112` | 181- 9 CM COL CLASSIC (10 DA | `BOX` | ₹89.00 | 10 | 1 | 4 | 4 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (50.0% div; non-... |
| `00438` | 517- TRI COL FOUNTAIN RAJHAR | `PKT` | ₹185.00 | 5 | 1 | 9 | 9 | 44.4% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (44.4% div; non-d... |
| `00440` | 519- TRI COL FOUNTAIN MERCUR | `PKT` | ₹265.00 | 10 | 1 | 2 | 2 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5, 2] contradicts suggested p... |
| `00441` | 520- TRI COL FOUNTAIN COCK ( | `PKT` | ₹297.00 | 5 | 1 | 4 | 4 | 75.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `00443` | 522- TRI COL FOUNTAIN T/MEEN | `PKT` | ₹235.00 | 5 | 1 | 9 | 9 | 88.9% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (88.9% div; non-d... |
| `00445` | 524- COL FOG FOUNTAIN S.T.D. | `PKT` | ₹77.50 | 5 | 1 | 5 | 5 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `00446` | 525- JET FOUNTAIN W S.T.D(5  | `PKT` | ₹85.00 | 5 | 1 | 5 | 5 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `00447` | 526- KIDDY'S JOY F P 5IN 1 A | `PKT` | ₹165.00 | 5 | 1 | 5 | 5 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (0.0% div; non-di... |
| `00448` | 527- MINI POPPERS 5 IN 1 MER | `PKT` | ₹175.00 | 5 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (0.0% div; non-di... |
| `00450` | 529- TORA TORA F. POT 5 IN 1 | `PKT` | ₹355.00 | 5 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `00454` | 533- CRACKLING FOUNTAIN SIVA | `PKT` | ₹200.00 | 3 | 1 | 10 | 10 | 30.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (30.0% div; non-d... |
| `00460` | 539- GOLDEN WHISTE SMALL (2P | `PKT` | ₹150.00 | 2 | 1 | 5 | 5 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (60.0% div; non-d... |
| `00461` | 540- CHOTA BHAI F P MINI SIR | `PKT` | ₹150.00 | 5 | 1 | 8 | 8 | 87.5% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (87.5% div; non-d... |
| `00493` | 552- TIM TIM GUDIYA ( 5 PCS  | `BOX` | ₹165.00 | 5 | 1 | 11 | 11 | 81.8% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (81.8% div; non-d... |
| `00494` | 553- LITTLE STAR ANAR GUDIYA | `BOX` | ₹270.00 | 5 | 1 | 13 | 13 | 76.9% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (76.9% div; non-d... |
| `00495` | 554- 2 IN 1 ANAR GUDIYA (10  | `BOX` | ₹325.00 | 10 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `00496` | 555- GOLDEN STAR GUDIYA  ( 5 | `BOX` | ₹270.00 | 5 | 1 | 4 | 4 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `00497` | 556- ASHARFI GUDIYA ( 5 PCS) | `BOX` | ₹300.00 | 5 | 1 | 5 | 5 | 20.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (20.0% div; non-d... |
| `00499` | 557- JASMINE GUDIYA ( 5PCS) | `BOX` | ₹300.00 | 5 | 1 | 5 | 5 | 40.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (40.0% div; non-d... |
| `00501` | 558- DAZZLE GUDIYA ( 5 PCS) | `BOX` | ₹465.00 | 5 | 1 | 4 | 4 | 25.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (25.0% div; non-d... |
| `00503` | 560- GIFT BOX GUDIYA ( 4 PCS | `BOX` | ₹650.00 | 4 | 1 | 7 | 7 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 4 (0.0% div; non-di... |
| `00535` | 590- G C BIG JENIS(10 P)(5P) | `PKT` | ₹40.00 | 10 | 1 | 5 | 5 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (60.0% div; non-... |
| `00542` | 645- DISCO WHEEL GAYATHRI(10 | `PKT` | ₹76.00 | 10 | 1 | 10 | 10 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (50.0% div; non-... |
| `00544` | 647- SILVER GAINT WHEEL MERC | `PKT` | ₹165.00 | 10 | 1 | 8 | 8 | 12.5% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (12.5% div; non-... |
| `00744` | 541- MINI SIREM F. POT COCK  | `PKT` | ₹175.00 | 3 | 1 | 9 | 9 | 22.2% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (22.2% div; non-d... |
| `00745` | 542- BIG SIREM F. POT COCK ( | `PKT` | ₹280.00 | 3 | 1 | 5 | 5 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `02124` | 603- G C ASOKA SPINNER W JEN | `PKT` | ₹75.00 | 10 | 1 | 10 | 10 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (60.0% div; non-... |
| `02525` | 1087- BULLET ROCKET YUG ( 36 | `PCS` | ₹108.00 | 36 | 1 | 3 | 3 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 36 (0.0% div; non-d... |
| `02665` | 283- 15 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | 2 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `02832` | 182- 9 CM 2 IN 1 CLASSIC(10D | `BOX` | ₹120.00 | 10 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `03175` | 581- SUPER DRONE W AYYAN( 5  | `PKT` | ₹170.00 | 5 | 1 | 3 | 3 | 33.3% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (33.3% div; non-d... |
| `03176` | 582- HELICOPTER AYYAN ( 5PCS | `PKT` | ₹80.00 | 5 | 1 | 9 | 9 | 66.7% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `03177` | 583- HELICOPTER R. KRISHNA.( | `PKT` | ₹75.00 | 5 | 1 | 10 | 10 | 70.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (70.0% div; non-d... |
| `03216` | 696- WHISTLING ROCKET K.M.RA | `PKT` | ₹115.00 | 2 | 1 | 5 | 5 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `03225` | 705- PARACHUTE ROCKET AYYAN  | `PKT` | ₹375.00 | 2 | 1 | 3 | 3 | 66.7% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 2 (66.7% div; non-d... |
| `04005` | 841- 7 SHOTS OTHER(5 PCS) (5 | `BOX` | ₹65.00 | 5 | 1 | 12 | 12 | 83.3% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (83.3% div; non-d... |
| `04007` | 843- 7 SHOTS MERCURY (5 PCS) | `BOX` | ₹120.00 | 5 | 1 | 10 | 10 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (80.0% div; non-d... |
| `04008` | 844- 7 SHOTS I.N (5 PCS) (5P | `BOX` | ₹136.00 | 5 | 1 | 3 | 3 | 66.7% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04015` | 851- 7 SHOTS MERCURY(10 PCS) | `BOX` | ₹250.00 | 10 | 1 | 5 | 5 | 20.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (20.0% div; non-... |
| `04028` | 1060- COL SMOKE DHUA 5COL(5P | `PKT` | ₹120.00 | 5 | 1 | 10 | 10 | 60.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `04059` | 1102- TIGER BLACK SOM(12 PCS | `PCS` | ₹61.50 | 12 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 12 (0.0% div; non-d... |
| `04194` | 117- GEM MEGA ( 10 PKT ) 3 C | `PKT` | ₹145.00 | 10 | 1 | 6 | 6 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04236` | 213- 12 CM 5 IN 1 (5 PKT) CH | `PKT` | ₹120.00 | 5 | 1 | 6 | 6 | 66.7% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04508` | 500- FLOWER POTS DLX (10 P)  | `PKT` | ₹150.00 | 10 | 1 | 6 | 6 | 33.3% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (33.3% div; non-... |
| `04509` | 501- FLOWER POTS DLX (10 P)  | `PKT` | ₹245.00 | 10 | 1 | 7 | 7 | 28.6% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (28.6% div; non-... |
| `04511` | 503- FLOWER POTS DLX COL KOT | `PKT` | ₹350.00 | 10 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04512` | 504- FLOWER POTS DLX COL KOT | `PKT` | ₹355.00 | 10 | 1 | 3 | 3 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04513` | 505- FLOWER POTS MEGA DLX (1 | `PKT` | ₹290.00 | 10 | 1 | 6 | 6 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04514` | 506- F P MEGA DLX  (10 P) VI | `PKT` | ₹420.00 | 10 | 1 | 15 | 15 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04518` | 510- FLOWER POT DLX (5 PCS ) | `PKT` | ₹120.00 | 5 | 1 | 16 | 16 | 87.5% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (87.5% div; non-d... |
| `04519` | 511- FLOWER POT DLX (5 PCS ) | `PKT` | ₹175.00 | 5 | 1 | 3 | 3 | 66.7% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04520` | 512- FLOWER POT DLX (5 PCS ) | `PKT` | ₹240.00 | 5 | 1 | 8 | 8 | 12.5% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (12.5% div; non-d... |
| `04576` | 617- G C SPL SPINNER WHEEL(1 | `PKT` | ₹75.00 | 10 | 1 | 17 | 17 | 82.4% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (82.4% div; non-... |
| `04615` | 652- MASKA CHASKA I. N ( 5 P | `PKT` | ₹120.00 | 5 | 1 | 5 | 5 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (80.0% div; non-d... |
| `04618` | 655- MUSICAL WHEEL MERCURY ( | `PKT` | ₹102.50 | 5 | 1 | 10 | 10 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `04626` | 663- SPINNER BAMBARA LAVANYA | `PKT` | ₹85.00 | 10 | 1 | 5 | 5 | 20.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (20.0% div; non-... |
| `04627` | 664- LOTUS WHEEL (5 PCS) AYY | `PKT` | ₹120.00 | 5 | 1 | 4 | 4 | 75.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `04685` | 730- WHISTLING PIPER SONY (  | `PKT` | ₹285.00 | 5 | 1 | 6 | 6 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `04687` | 732- HAND SHOWER MARIESWARAN | `PKT` | ₹185.00 | 3 | 1 | 7 | 7 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04914` | 1012- 5 KA DHUM ( 5 P) ANIL | `BOX` | ₹155.00 | 5 | 1 | 4 | 4 | 75.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `04918` | 1016- TOP-TEN ( 10 P ) COCK | `BOX` | ₹350.00 | 10 | 1 | 5 | 5 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04924` | 1022- 2 1/2 F. P. (3P)6COL M | `BOX` | ₹175.00 | 3 | 1 | 9 | 9 | 44.4% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (44.4% div; non-d... |
| `04925` | 1023- 2 1/2 F. P. (3P)6COL M | `BOX` | ₹180.00 | 3 | 1 | 10 | 10 | 40.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (40.0% div; non-d... |
| `04927` | 1025- 2 1/2 F. P. (3PCS) MIX | `BOX` | ₹225.00 | 3 | 1 | 9 | 9 | 44.4% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (44.4% div; non-d... |
| `04929` | 1027- 2 1/2 F. P. (3P)MIX CO | `BOX` | ₹500.00 | 3 | 1 | 3 | 3 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04930` | 1028- 2 1/2 F. P. (3P)3 IN 1 | `BOX` | ₹422.00 | 3 | 1 | 4 | 4 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04931` | 1029- PARACHUTE NIGHTOUT ( 3 | `BOX` | ₹400.00 | 3 | 1 | 7 | 7 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04932` | 1030- 2 1/2 F. P.LONG(3P)MIX | `BOX` | ₹455.00 | 3 | 1 | 6 | 6 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04941` | 1039- 3  FANCY PIPE (2P) MIX | `BOX` | ₹600.00 | 2 | 1 | 4 | 4 | 50.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 2 (50.0% div; non-d... |
| `04942` | 1040- 3  FANCY PIPE (3P) MIX | `BOX` | ₹940.00 | 3 | 1 | 7 | 7 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `05404` | 515- FLOWER POTS RANG BARAAT | `PKT` | ₹405.00 | 2 | 1 | 5 | 5 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `05460` | 1052- 4"  F. P.(2P) 8 COL MI | `BOX` | ₹1100.00 | 2 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `05950` | W COL SMOKE DHUA  COL (5 P)  | `BOX` | ₹120.00 | 5 | 1 | 7 | 6 | 42.9% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (42.9% div; non-d... |
| `06049` | W 1 1/4 POGO MIXED ( 10 P) 2 | `BOX` | ₹58.00 | 10 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06054` | W 2 1/2 F PIPE  BALAJI ( 3 P | `BOX` | ₹175.00 | 3 | 1 | 5 | 3 | 20.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (20.0% div; non-d... |
| `06058` | W 3 F PIPE BIG SIZZ MIXD ( 2 | `BOX` | ₹580.00 | 2 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06072` | W 4 F P 3 COL MIXED ( 2 P) W | `BOX` | ₹850.00 | 2 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06074` | W 4 F P DLX 15 COL MIXED ( 2 | `BOX` | ₹900.00 | 2 | 1 | 1 | 1 | 0.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06099` | W 18 SHOT ROMANCANDLE ( 2P) | `BOX` | ₹400.00 | 2 | 1 | 5 | 5 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `06156` | W 2 1/2 F PIPE  MIX BIG  ( 3 | `BOX` | ₹375.00 | 3 | 1 | 5 | 5 | 80.0% | 1 | `[]` | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (80.0% div; non-d... |

### Category 5: INSUFFICIENT_HISTORY (158 Products)
*Zero sales (96 items) or low volume (62 items) in D2627. Safe default 1 retained.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | GCD | Plausible Divisors | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00120` | 195- 10 CM SILVER DROPS SARA | `PKT` | ₹15.50 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00144` | 276- 10 CM PLAIN ASOK ( 5 P) | `PKT` | ₹20.00 | 5 | 1 | 2 | 2 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00145` | 277- 10 CM COL ASOK ( 5 P) | `PKT` | ₹23.00 | 5 | 1 | 1 | 1 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00147` | 278- 10 CM GREEN ASOK ( 5 P) | `PKT` | ₹28.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00148` | 279- 10 CM RED ASOK ( 5 P) | `PKT` | ₹30.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00149` | 280- 10 CM 4 COLOUR ASOK ( 5 | `PKT` | ₹28.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00180` | 149- MINI RED BIJALI CAT BRA | `BAG` | ₹58.00 | 10 | 10 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `00182` | 151- RED BIJALI GANESH(100 P | `BAG` | ₹41.00 | 10 | 10 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `00185` | 154- RED BIJALI VIMAL(100 P) | `BAG` | ₹65.00 | 10 | 10 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `00187` | 291- 10 GAINT JAWAN GEMS (10 | `BUNDLE` | ₹360.00 | 1 | 1 | 2 | 2 | 100.0% | 1 | `[]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 lines, 2 customer). All orders divisi... |
| `00251` | 309- 20 DLX BALAJI( 10 P) | `PKT` | ₹37.50 | 10 | 1 | 2 | 2 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00254` | 312- 24 DLX COCK (10P) | `BOX` | ₹63.00 | 10 | 1 | 1 | 1 | 100.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00294` | 334- 2 3/4 KURVI AYYANAR (25 | `PKT` | ₹9.50 | 25 | 1 | 2 | 2 | 100.0% | 250 | `[2, 5, 10, 25, 50, 125, 250]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00368` | 413- 2 LXM DHAMAKA GENIUS (2 | `PKT` | ₹5.50 | 25 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00370` | 415- 3 1/2 LXM DHAMAKA AYYAN | `PKT` | ₹13.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00371` | 416- 3 1/2 LXM DHAMAKA I.N(1 | `PKT` | ₹14.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00372` | 417- 3 1/2 LXM DHAMAKA AMBIK | `PKT` | ₹15.00 | 10 | 1 | 1 | 1 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00374` | 419- 3 1/2 LXM DHAMAKA S.T.D | `PKT` | ₹24.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00381` | 426- 4' LXM DHAMAKA I.N ( 10 | `PKT` | ₹18.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00382` | 427- 4' LXM DHAMAKA AYYANAR  | `PKT` | ₹21.00 | 10 | 1 | 1 | 1 | 100.0% | 300 | `[2, 3, 4, 5, 6, 10, 12, 15, 20, 25, 30, 50, 60, 75, 100, 150, 300]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00383` | 428- 4' LXM DHAMAKA AYYAN (  | `PKT` | ₹32.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00387` | 432- 4' DLX LXM DHAMAKA I.N  | `PKT` | ₹23.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00388` | 433- 4' DLX BAJ DHAMAKA T/ME | `PKT` | ₹30.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00389` | 434- 4' DLX LXM DHAMAKA T/ME | `PKT` | ₹32.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00391` | 436- 4' DLX LXM DHAMAKA AYYA | `PKT` | ₹35.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00395` | 439- 4 DLX GOLD LXM T/MEENA  | `PKT` | ₹30.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00396` | 440- 4 DLX GOLD LXM AYYANAR( | `PKT` | ₹35.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00429` | 445- FLOWER POTS SMALL ARUDH | `PKT` | ₹50.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00430` | 446- FLOWER POTS SMALL MURCU | `PKT` | ₹64.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00442` | 521- TRI COL FOUNTAIN S.T.D  | `PKT` | ₹375.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00449` | 528- HAPPINESS F. POT 5 IN 1 | `PKT` | ₹265.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00463` | 575- MAGIC WHIP S.T.D( 2 P) | `PKT` | ₹89.00 | 2 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00492` | 551- MINI PEARL GUDIYA ( 5 P | `BOX` | ₹135.00 | 5 | 1 | 1 | 1 | 100.0% | 5 | `[5]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00504` | 561- ASHARFI  GOLDEN STAR OT | `BOX` | ₹240.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00505` | 562- MUTT PUTT ANAR MERCURY  | `BOX` | ₹200.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00533` | 588- G C BIG T/MEENA( 10 P)( | `PKT` | ₹30.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00534` | 589- G C BIG GANESH ( 10 P)( | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00543` | 646- DISCO WHEEL S.M.K.(10 P | `PKT` | ₹85.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00564` | 707- 18 T STAR D/VADIVEL(10P | `PKT` | ₹15.00 | 10 | 1 | 1 | 1 | 100.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00566` | 709- 18 T STAR T/MEENA (10P) | `PKT` | ₹20.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00568` | 711- 120 T STAR S.T.D (10P)  | `PKT` | ₹155.00 | 5 | 1 | 1 | 1 | 100.0% | 5 | `[5]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00619` | 740- SUPER BULLET BOMB AYYAN | `PKT` | ₹25.00 | 10 | 1 | 2 | 2 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00620` | 741- BULLET BOMB GANESH ( 10 | `PKT` | ₹27.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00622` | 743- SUPER BULLET BOMB ( 10  | `PKT` | ₹39.00 | 10 | 1 | 1 | 1 | 100.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `00631` | 752- JHANSI BOMB GREEN W/F(1 | `PKT` | ₹80.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00688` | 598- G C ASOKA T/MEENA (10 P | `PKT` | ₹40.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00758` | 599- G C ASOKA AYYANAR(10 P) | `PKT` | ₹50.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `00761` | 649- SUN FLOWER WHEEL I. N ( | `PKT` | ₹255.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `00866` | 158- STRIPPED BIJALI ROSE(50 | `BAG` | ₹11.50 | 50 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02042` | 281- 12 CM PLAIN ASOK ( 2 P) | `PKT` | ₹35.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02155` | 1120- RING CAPS (1OOPKT= 1 B | `PKT` | ₹7.00 | 100 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02275` | 282- 12 CM COLOUR ASOK ( 2 P | `PKT` | ₹40.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02667` | 284- 30 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02668` | 285- 30 CM COL ASOK ( 2 P) | `PKT` | ₹70.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02671` | 569- DANCING BUTTERFLY AYYAN | `PKT` | ₹125.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02672` | 670- PYRO DANCE BUTTERFLY SU | `PKT` | ₹140.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02673` | 571- COL CHAN. BUTTERFLY S.T | `PKT` | ₹132.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02677` | 668- RAINBOW ROCKET S.T.D (1 | `PKT` | ₹130.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02679` | 670- ROCKET BOMB (10P) 5P N. | `PKT` | ₹45.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02710` | 197- 30 CM GREEN SARAVANA (2 | `PKT` | ₹25.00 | 2 | 1 | 1 | 1 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `02711` | 198- 30 CM RED SARAVANA (2 P | `PKT` | ₹27.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `02841` | 233- 12 CM 4 IN 1 LX CLASSIC | `PKT` | ₹22.00 | 5 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `02885` | 580- SKY SCRAPPER DRONE MERC | `PCS` | ₹125.00 | 5 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `02905` | W 1000 LAR (600 COUNTING) S. | `PKT` | ₹180.00 | 1 | 1 | 2 | 2 | 100.0% | 1 | `[]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 lines, 2 customer). All orders divisi... |
| `03092` | 186- 7 CM RED M.R.P. (10 DAB | `BOX` | ₹120.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03094` | 188- 7 CM PLAIN GOLD S.T.D(1 | `BOX` | ₹180.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03102` | 240- 15 CM COL BOXE(2P CELLE | `PKT` | ₹29.00 | 2 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03111` | 249- 30 CM PLAIN DLX CLASSIC | `PKT` | ₹25.00 | 5 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03112` | 250- 30 CM PLAIN BOXE(2P CEL | `PKT` | ₹26.00 | 2 | 1 | 1 | 1 | 100.0% | 40 | `[2, 4, 5, 8, 10, 20, 40]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `03179` | 585- HELICOPTER ANIL( 5PCS) | `PKT` | ₹100.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03180` | 586- HELICOPTER SUNSHINE( 10 | `PKT` | ₹290.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03212` | 612- G C SPL W (10 P) I.N | `PKT` | ₹90.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03213` | 613- G C SPL (10 P) (5 P) SU | `PKT` | ₹94.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03218` | 698- WHISTLING ROCKET MERCUR | `PKT` | ₹200.00 | 2 | 1 | 2 | 2 | 100.0% | 4 | `[2, 4]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03219` | 699- WHISTLING ROCKET ANIL(1 | `PKT` | ₹227.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03220` | 700- SILVER JET ROCKET S.T.D | `PKT` | ₹225.00 | 2 | 1 | 2 | 2 | 100.0% | 2 | `[2]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03221` | 701- ROHINI ROCKET S.T.D (10 | `PKT` | ₹227.00 | 2 | 1 | 2 | 2 | 100.0% | 2 | `[2]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `03226` | 706- PARACHUTE ROCKET S.T.D  | `PKT` | ₹575.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03229` | 719- 7 CM PENCIL VIRBALAJI ( | `PKT` | ₹20.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03230` | 720- 7 CM PENCIL T/MEENA ( 1 | `PKT` | ₹24.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `03232` | 722- 10 CM PENCIL T/MEENA (  | `PKT` | ₹45.00 | 10 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `03233` | 723- 12 CM PENCIL VIRBALAJI  | `PKT` | ₹43.00 | 10 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `03267` | 755- LALKAR BOMB FOIL W/F(10 | `PKT` | ₹90.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04006` | 842- 7 SHOTS J.K (5 PCS) (5P | `BOX` | ₹80.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04012` | 848- 7 SHOTS OTHER (10 PCS) | `BOX` | ₹180.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04016` | 852- 7 SHOTS SIGNAL ROCKET C | `BOX` | ₹500.00 | 15 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04045` | 1088- YOGESH BLACK GUN REX ( | `PKT` | ₹7.00 | 12 | 1 | 2 | 2 | 100.0% | 12 | `[2, 3, 4, 6, 12]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04046` | 1089- TOM COLOUR YUG ( 12 PC | `PCS` | ₹7.50 | 12 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04047` | 1090- V-30 COLOUR VISHNU (12 | `PCS` | ₹12.10 | 12 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04049` | 1092- V-301 COLOUR VISHNU (  | `PCS` | ₹12.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04192` | 115- R & G MATCH BOX RAYAL(6 | `BUNDLE` | ₹500.00 | 1 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `04195` | 118- WONDER CRACKLING ( 10 P | `PKT` | ₹210.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04239` | 216- 15 CM  50 X 50 (5 PCS)C | `PKT` | ₹35.00 | 5 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04248` | 253- 30 CM COL BOXE(2P CELLE | `PKT` | ₹29.00 | 2 | 1 | 1 | 1 | 100.0% | 40 | `[2, 4, 5, 8, 10, 20, 40]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04254` | 259- 30 CM 2 IN 1 BOXE(2P CE | `PKT` | ₹29.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04302` | 160- STRIPPED BIJALI ROSE(10 | `BAG` | ₹21.50 | 10 | 10 | 2 | 2 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **10** | LOW | Low volume in D2627 (2 lines, 2 customer). All orders divisi... |
| `04306` | 164- STRIPPED BIJALI S.T.D(1 | `BAG` | ₹60.00 | 10 | 10 | 1 | 1 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **10** | LOW | Low volume in D2627 (1 lines, 1 customer). All orders divisi... |
| `04310` | 168- GOLD BIJALI COCK (50 PC | `BAG` | ₹35.50 | 50 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04342` | 297- 28 CHORSA (25PCS) VELVA | `PKT` | ₹14.50 | 25 | 1 | 2 | 2 | 100.0% | 25 | `[5, 25]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04343` | 298- 32 CHORSA MIX RED-GOA S | `PKT` | ₹12.50 | 50 | 1 | 1 | 1 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04347` | 302- 28 GAINT CHORSA (25 P)  | `PKT` | ₹18.50 | 25 | 1 | 2 | 2 | 100.0% | 25 | `[5, 25]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04349` | 304- 28 GAINT CHORSA (25 P)D | `PKT` | ₹19.50 | 25 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04350` | 305- 28 SUP GAINT CHORSA N.M | `PKT` | ₹24.00 | 25 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04352` | 317- 50 DLX GANESH DURAI( 5  | `PKT` | ₹80.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04371` | 343- 3 1/2  PEACOCK 9 CM  S. | `PKT` | ₹24.00 | 10 | 1 | 1 | 1 | 100.0% | 30 | `[2, 3, 5, 6, 10, 15, 30]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04372` | 344- 3 1/2 DLX KURVI GANESH  | `PKT` | ₹25.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04373` | 345- 3 1/2 GREEN PARROT W/F  | `PKT` | ₹25.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04374` | 346- 3 1/2 JAWAN AYYAN (10 P | `PKT` | ₹27.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04377` | 349- 4  MIX LABEL DURGESH (1 | `PKT` | ₹14.00 | 10 | 1 | 1 | 1 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04379` | 351- 4 GREEN PARROT SRIPATHI | `PKT` | ₹16.00 | 10 | 1 | 1 | 1 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04380` | 352- 4  LADY T/MEENA  (10 P) | `PKT` | ₹16.00 | 10 | 1 | 1 | 1 | 100.0% | 70 | `[2, 5, 7, 10, 14, 35, 70]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04387` | 359- 4 GREEN PARROT W/F V.F. | `PKT` | ₹32.00 | 10 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04388` | 360- 4 KING AYYAN (10 P) | `PKT` | ₹32.50 | 10 | 1 | 1 | 1 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04389` | 361- 10 CM PEACOCK COLF S.T. | `PKT` | ₹34.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04390` | 362- 4 GREEN PARROT W/F B.F. | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04413` | 385- 5 DLX  ELEPHANT(10P) JA | `PKT` | ₹31.00 | 10 | 1 | 2 | 2 | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04424` | 396- 4 SUP DLX GOLD ELEPHANT | `PKT` | ₹57.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04428` | 403- 2 SOUND DHAMAKA ANIL (1 | `PKT` | ₹32.00 | 10 | 1 | 1 | 1 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04429` | 404- 2 SOUND DHAMAKA S.T.D ( | `PKT` | ₹36.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04430` | 405- 2 SOUND DHAMAKA MERCURY | `PKT` | ₹42.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04433` | 408- 3 SOUND DHAMAKA NM JYOT | `PKT` | ₹28.50 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04435` | 410- 3 SOUND DHAMAKA I.N. (1 | `PKT` | ₹40.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04510` | 502- FLOWER POTS COL KOTI DL | `PKT` | ₹375.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04563` | 563- OMG POTS ANAR MERCURY ( | `BOX` | ₹315.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04564` | 564- CROWN JEWEL'S ANAR MERC | `BOX` | ₹625.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04580` | 621- G C DLX  (10 P) 5 P VEN | `PKT` | ₹75.00 | 5 | 1 | 2 | 2 | 100.0% | 20 | `[2, 4, 5, 10, 20]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04587` | 628- G C DLX  (10 P) 5 P ANI | `PKT` | ₹160.00 | 5 | 1 | 1 | 1 | 100.0% | 15 | `[3, 5, 15]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04588` | 629- G C DLX  (10 P) 5 P SUN | `PKT` | ₹165.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04593` | 634- G C DLX  PLASTIC (10 P) | `PKT` | ₹110.00 | 5 | 1 | 2 | 2 | 100.0% | 5 | `[5]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04600` | 641- G C SUP DLX  (10 P) 5 P | `PKT` | ₹190.00 | 5 | 1 | 2 | 2 | 100.0% | 5 | `[5]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04620` | 657- WHIZZ WHEEL S.T.D (5 PC | `PKT` | ₹139.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04622` | 659- TOP TUCKER AYYAN ( 5 P) | `PKT` | ₹80.00 | 5 | 1 | 1 | 1 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `04634` | 673- ROCKET BOMB (10P) 5P S. | `PKT` | ₹144.00 | 5 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04640` | 679- EXPO ROCKET (10 P) 2P G | `PKT` | ₹85.00 | 2 | 1 | 2 | 2 | 100.0% | 2 | `[2]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04643` | 682- LUNIK ROCKET (10 P) 2P  | `PKT` | ₹130.00 | 2 | 1 | 2 | 2 | 100.0% | 10 | `[2, 5, 10]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `04650` | 689- 2 SOUND ROCKET (10 P) 2 | `PKT` | ₹132.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04926` | 1024- 2 1/2 F. P. (2P)6COL M | `BOX` | ₹190.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `04928` | 1026- 3 FANCY PIPE (2 PCS) S | `BOX` | ₹850.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05004` | 1115- PUBG GUN ( 5 P X 1 PKT | `BOX` | ₹90.00 | 5 | 1 | 2 | 2 | 100.0% | 5 | `[5]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `05020` | 1133- COLD PYRO BLACK R.R.R  | `BOX` | ₹110.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05021` | 1134- COLD PYRO YELLO BOX TA | `BOX` | ₹120.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05023` | 1136- NAAGARA FALLS ( 25 PCS | `BOX` | ₹1200.00 | 25 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05427` | 693- 3 SOUND ROCKET (10 P) 2 | `PKT` | ₹135.00 | 2 | 1 | 2 | 2 | 100.0% | 2 | `[2]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). All observed... |
| `05459` | 1051- 4"  F. P.(2P) 3 COL. M | `BOX` | ₹860.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05461` | 1053- 4"  DLX F.P.(2P) 12 CO | `BOX` | ₹950.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05462` | 1054- 4"  F.P.(2P)DOUBLE BAL | `BOX` | ₹1230.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `05933` | W 1000 LAR (800 COUNTING) S. | `BOX` | ₹200.00 | 1 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `05953` | W 4 F. PIPE (2 PCS)  I. N. | `BOX` | ₹900.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06048` | W TOP- TEN ( 10 P ) COCK | `BOX` | ₹285.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06053` | W 2 1/2 F PIPE MIX UV BOX (  | `BOX` | ₹165.00 | 3 | 1 | 1 | 1 | 100.0% | 36 | `[2, 3, 4, 6, 9, 12, 18, 36]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |
| `06056` | W 2 1/2 F PIPE MEGAL ( 3 P ) | `BOX` | ₹445.00 | 3 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06057` | W 3 F PIPE LIGHT AND HOT MIX | `BOX` | ₹685.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06068` | W 3 1/2 F P DOUBLE BALL (2 P | `BOX` | ₹750.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06073` | W 4 F P 3 COL MIXED ( 2 P) W | `BOX` | ₹900.00 | 2 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06092` | W 7 SHOT ( 10 P ) MERCURY | `BOX` | ₹210.00 | 10 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Maintain safe unc... |
| `06106` | W 5000 LAR (600) COUNTING SA | `BOX` | ₹950.00 | 1 | 1 | 0 | 0 | 0.0% | 0 | `[]` | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero eligible sales transactions in D2627. Retain currently ... |
| `06157` | W COLD PYRO BOX 3.M.35.S (6P | `BOX` | ₹100.00 | 6 | 1 | 2 | 1 | 100.0% | 6 | `[2, 3, 6]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 1 customer(s)). All observed... |
| `06175` | 133- KIT-KAT BIG(10 P)TIRUMI | `PKT` | ₹32.00 | 10 | 1 | 1 | 1 | 100.0% | 100 | `[2, 4, 5, 10, 20, 25, 50, 100]` | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). All observed... |

---

## 7. Recommended Safe Cloned-Dataset Dry-Run Protocol

Before deploying any updated packaging rules into production:
1. **Business Owner Review**: Review [`PACKAGING_BUSINESS_REVIEW_WORKSHEET.md`](./PACKAGING_BUSINESS_REVIEW_WORKSHEET.md) and [`ACTIVE_RULE_RISK_REGISTER.md`](./ACTIVE_RULE_RISK_REGISTER.md).
2. **Controlled Overlay JSON Update**: Update `sync-service/app/data/catalog_pack_rules.json` only for explicitly approved items.
3. **Cloned-Dataset Order Validation Run**: Clone `legacy-software-extracted/FAVWIN/D2627` to a test sandbox and replay all 3,590 historical wholesale orders to verify that zero legitimate orders are rejected.
