# PYROJA Packaging Rules Historical Sales Evidence & Recommendation Report

**Document Version:** 1.0.0  
**Date Generated:** September 19, 2026  
**Active Fiscal Year Dataset:** `legacy-software-extracted/FAVWIN/D2627` (2026-04-05 to 2026-08-29)  
**Total Scope Analyzed:** All 439 Packaging Rule Candidates (32 Currently Enforced Overlays + 407 Heuristic Candidates > 1)  
**Safety Principle:** 100% Read-Only DBF Inspection. Zero database, stock, or code modifications. No rule promoted to `APPROVED` without business owner review.  

---

## 1. Executive Summary

In FoxPro `ITEMMST.DBF`, the `QIB` (Quantity In Box) field is `1` across all 3,019 products and `PACK` represents the FoxPro billed unit of measure (`PKT`, `BOX`, `BUNDLE`, `BAG`), not the wholesale dispatch case multiple. Enforcing pack restrictions directly from unverified regex heuristics creates severe commercial risks, including false positives (e.g. multi-shot cake tube counts, garland cracker counts, matchbox master bundles) that would block legitimate wholesale orders with `422 Unprocessable Entity` errors.

To determine which pack multiples are safe and commercially justified, we audited the complete sales order history in `SALETRN.DBF` (3,612 transactions across 134 invoices and 60 distinct customer accounts) against all 439 candidate products. Retail cash counter orders (`PCODE == '99999'`) were isolated so that walk-in loose retail purchases do not distort wholesale commercial dispatch analysis.

### Key Audit Findings & Summary Matrix

| Recommendation Category | Total Count | % of Candidates | Empirical Validation Basis | Primary Recommended Action |
| :--- | :---: | :---: | :--- | :--- |
| **`RECOMMEND_APPROVE`** | **146** | **33.3%** | Consistent multi-customer wholesale orders (100% divisible, $\ge 2$ customers, $\ge 3$ lines) | Eligible for business owner sign-off to enforce in `catalog_pack_rules.json` |
| **`RECOMMEND_CHANGE`** | **32** | **7.3%** | Wholesale orders consistently follow a different multiple $M_{alt} \ne M_{prop}$ across multiple customers | Adopt proven alternate multiple (e.g. 4 instead of 25; 10 bags instead of 100 crackers; 80 for Dhaga) |
| **`RECOMMEND_REJECT`** | **103** | **23.5%** | Wholesale orders frequently contain loose units (1, 2, 3, etc.) contradicting the suggested multiple | Reject multiple; keep enforced multiple at `1` to prevent blocking wholesale orders |
| **`INSUFFICIENT_HISTORY`** | **158** | **36.0%** | Zero sales (96 items) or single-customer/low-volume data (62 items) in D2627 | Maintain safe default `1`; monitor during Diwali peak season |
| **Total Candidates** | **439** | **100.0%** | Comprehensive audit across all active candidates | Business owner review required prior to activation |

---

## 2. Historical Data Scope & Confidence Limitations

Understanding the data boundaries is vital before converting recommendations into production policy:

1. **Fiscal Year Scope (D2627)**:  
   - Sales records span April 5, 2026 to August 29, 2026 (66 distinct transaction dates across 5 months).
   - Total sales lines: 3,612 lines across 134 invoices.
   - Customer base: 60 active customer accounts (59 wholesale credit accounts, 1 retail cash account `99999`).

2. **Seasonal Fireworks Ordering Dynamics**:  
   - Fireworks wholesale ordering in India experiences exponential seasonality. August data represents early-season distributor procurement, dealer indenting, and advance wholesale booking.
   - 703 distinct products have recorded transactions in D2627, while 96 candidate products have zero transactions so far this fiscal year. The absence of transactions does not mean a product is inactive; many seasonal novelties are ordered exclusively in September and October.

3. **Strict Multi-Customer Corroboration Standard**:  
   - Under our audit protocol, **no pack multiple can be recommended for approval based on a single customer or a single invoice**.
   - Even if an order of 10 units was placed, a single customer order cannot distinguish whether the customer coincidentally wanted 10 units or was constrained by packaging. A minimum of 2 distinct wholesale customers ($C_{ws} \ge 2$) and 3 wholesale lines ($L_{ws} \ge 3$) is required for `RECOMMEND_APPROVE`.

4. **Isolation of Retail Walk-In Cash Account (`99999`)**:  
   - `99999` accounts for 22 retail transactions. Because retail customers are permitted to purchase loose units, retail transactions were excluded from wholesale divisibility percentages.

---

## 3. Audit of the 32 Currently Enforced Overlay Rules

The 32 explicit rules currently configured in `sync-service/app/data/catalog_pack_rules.json` were evaluated against the historical transaction dataset:

### A. Empirically Verified Overrides (22 Products)
These 22 rules have robust sales records confirming business behavior:
- **Red & Stripped Bijali (10 Bags Outer Case)**: `00178`, `00181`, `00183`, `00184`, `04301`, `04303`, `04305` — 100% of orders across 3 to 12 distinct wholesale customers were multiples of 10 bags (e.g. 10, 20, 30, 40, 50, 60, 100, 200 bags).
- **Chorsa Bundles (50 Packets)**: `00223`, `00224`, `00225` — 100% of orders across 3 to 15 wholesale customers were multiples of 50 packets (e.g. 50, 100, 150, 200, 250 packets).
- **Bundle-Billed Items Enforcing 1**: `00082`, `00083` (Naggoli bundles), `00186` (10 Chorsa bundle), `03088` (Matchbox 600 Dabba bundle) — Invoices confirm these items are billed per bundle in quantities of 1, 2, 3, 5 bundles. Setting enforced multiple to 1 prevents blocking bundle orders.
- **Loose-Pack Fancy Items Enforcing 1**: `00079` (Asst Cartoon), `00455`, `00456` (Ayyan Jadugar/Manoranjan UV Box), `02157` (Missile Siren 127X1), `04613`, `04616`, `04625` (Ayyan wheels) — Invoices confirm loose customer orders (e.g. 1, 2, 3, 4, 5 units), validating that enforced multiple `1` correctly prevents blocking orders.

### B. Critical Discovery: Rule `04042` (`DHAGA (80 DABBI) INDIA`)
> [!IMPORTANT]
> **Rule Correction Recommended for `04042`:**
> - Current overlay rule sets `pack_multiple: 1` under the assumption that Dhaga is billed per bundle.
> - However, in `SALETRN.DBF`, the billing `UNIT` is `PKT` (rate ₹6.00) and **100% of historical wholesale orders across 6 distinct customers were in multiples of 80 packets** (`QTY: 80(5), 320(1)`).
> - Customers are ordering in master bundles of 80 packets (₹480/bundle).
> - **Recommendation:** Change enforced pack multiple from `1` to `80` upon business owner approval.

### C. Overlay Rules with Low/Zero Volume in D2627 (10 Products)
The remaining 10 overlay rules had fewer than 3 lines in D2627:
- **Zero Transactions in D2627 (6 Products)**: `00180` (Mini Red Bijali Cat), `00182` (Red Bijali Ganesh), `00185` (Red Bijali Vimal), `04192` (Matchbox Rayal), `05933` (W 1000 Lar SKM), `06106` (W 5000 Lar Santhanmari).
- **1 to 2 Lines in D2627 (4 Products)**: `00187` (10 Gaint Jawan Gems, 2 lines of 1 bundle), `02905` (W 1000 Lar SKM, 2 lines of 5-6 boxes), `04302` (Stripped Bijali Rose, 2 lines of 100 & 350 bags), `04306` (Stripped Bijali STD, 1 line of 50 bags).
- **Recommendation:** Retain existing approved configurations based on manufacturing specifications; conduct verification during peak season.

---

## 4. Deep-Dive: `RECOMMEND_CHANGE` Candidates (32 Products)

For 32 products, the heuristic extracted a number from the product description, but empirical sales orders prove wholesale dispatches strictly follow a **different, lower multiple** across multiple customers:

### Key Patterns in Alternate Multiples
1. **Inner Pack vs. Outer Pack Discrepancy (4P Inner Pack)**:  
   - `00080` (`ASST CARTOON BEN TEN (25P) AYYANAR 4P`) & `00081` (`SNAKE CARTOON (25P) SAMLL AYYANAR 4P`): Heuristic extracted `25` from `(25P)`. However, across 7 and 8 distinct wholesale customers, **100% of orders were multiples of 4** (`4, 8, 12`). The outer box contains 25, but the sellable inner pack is 4 packets! Enforcing 25 would have blocked every single historical customer order!
   - `00610` (`G C BIG T/MEENA (25 PCS) (W) (4P)`) & `00611` (`G C BIG GANESH (25 PCS) (4P)`): Exactly identical pattern. Heuristic extracted `25`, but 100% of sales across 5 and 7 customers were multiples of 4 (`4, 8, 12, 16, 20`). Recommended multiple: `4`.

2. **Gold Bijali Cracker Count vs. Case Pack (10 Bags)**:  
   - `04309`, `04311`, `04312`, `04315`, `04316`, `04317`: Product names contain `(50 PCS)` or `(100 PCS)`, representing the number of small crackers inside each individual bag. The heuristic suggested 50 or 100. However, in `SALETRN.DBF`, the billing unit is `BAG` and all wholesale orders are in multiples of **10 bags** (e.g. 20, 30, 40, 50, 100, 160, 250 bags). This perfectly mirrors the Red Bijali rules! Recommended multiple: `10`.

3. **Inner Dabba / Packet Sub-Packs (5 Packets / Dabbi)**:  
   - `04680` (`18 CM PENCIL VIRBALAJI ( 10 P )`): Heuristic extracted 10. Across 6 wholesale customers, 5 ordered 5 units and 1 ordered 10 units. Inner packet size is 5. Recommended multiple: `5`.
   - `04915` (`SKY SHOT (10 P ) COCK`): Heuristic extracted 10. Across 10 wholesale customers, orders were 5, 10, and 40 units (100% divisible by 5). Recommended multiple: `5`.
   - `00109` (`9 CM PLAIN INDRA (10 DABBI=1BOX)`): Orders across 5 customers were 10, 15, 30, 40, 50 dabbi (all multiples of 5). Recommended multiple: `5`.

4. **Ring Caps Half-Box Dispatches (50 Packets)**:  
   - `02152` & `02153` (`RING CAPS (1OOPKT= 1 BOX)`): Heuristic extracted 100. Invoices across 3 and 10 customers reveal orders of 100, 150, 200, 250, 500, 800 packets (strictly multiples of 50 packets / half-boxes). Recommended multiple: `50`.

### Complete Table of All 32 `RECOMMEND_CHANGE` Products

| Code | Product Name | UOM | Rate (₹) | Suggested | Proposed Multiple | WS Lines | Custs | Wholesale Quantity Distribution | Commercial Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| `00080` | 120- ASST CARTOON BEN TEN(25P)AYYAN | `PKT` | ₹55.00 | 25 | **4** | 7 | 7 | `4(7)` | Wholesale orders fail suggested multiple 25 (0.0% div), but 100% match alternate pack multiple 4 across 7 customers. |
| `00081` | 121- SNAKE CARTOON(25P)SAMLL AYYANA | `PKT` | ₹55.00 | 25 | **4** | 8 | 8 | `4(6)|8(1)|12(1)` | Wholesale orders fail suggested multiple 25 (0.0% div), but 100% match alternate pack multiple 4 across 8 customers. |
| `00109` | 178- 9 CM PLAIN INDRA (10 DABBI=1BO | `BOX` | ₹65.00 | 10 | **5** | 5 | 5 | `10(1)|15(1)|30(1)|40(1)|50(1)` | Wholesale orders fail suggested multiple 10 (80.0% div), but 100% match alternate pack multiple 5 across 5 customers. |
| `00610` | 595- G C BIG T/MEENA (25 PCS) (W) ( | `PKT` | ₹75.00 | 25 | **4** | 5 | 5 | `4(1)|8(1)|12(1)|16(1)|20(1)` | Wholesale orders fail suggested multiple 25 (0.0% div), but 100% match alternate pack multiple 4 across 5 customers. |
| `00611` | 596- G C BIG GANESH (25 PCS) (4P) | `PKT` | ₹80.00 | 25 | **4** | 7 | 7 | `4(3)|8(3)|16(1)` | Wholesale orders fail suggested multiple 25 (0.0% div), but 100% match alternate pack multiple 4 across 7 customers. |
| `00691` | 122- RAJDHANI RAIL(10 PCS)AYYANAR ( | `PKT` | ₹65.00 | 10 | **5** | 4 | 4 | `5(2)|10(1)|20(1)` | Wholesale orders fail suggested multiple 10 (50.0% div), but 100% match alternate pack multiple 5 across 4 customers. |
| `00876` | 601- G C ASOKA BIG SIZE GANESH(10 P | `PKT` | ₹72.50 | 10 | **5** | 7 | 7 | `10(2)|15(1)|30(2)|40(1)|70(1)` | Wholesale orders fail suggested multiple 10 (85.7% div), but 100% match alternate pack multiple 5 across 7 customers. |
| `00925` | 602- G C ASOKA S.T.D (10 P) (5P) | `PKT` | ₹88.00 | 10 | **5** | 9 | 9 | `5(3)|10(3)|20(2)|35(1)` | Wholesale orders fail suggested multiple 10 (55.6% div), but 100% match alternate pack multiple 5 across 9 customers. |
| `02081` | 142- MAGIC FOUNTAIN OVEEYA(10 PCS) | `PKT` | ₹120.00 | 10 | **5** | 3 | 3 | `5(2)|10(1)` | Wholesale orders fail suggested multiple 10 (33.3% div), but 100% match alternate pack multiple 5 across 3 customers. |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX)RACH | `PKT` | ₹6.00 | 100 | **50** | 3 | 3 | `100(1)|150(1)|250(1)` | Wholesale orders fail suggested multiple 100 (33.3% div), but 100% match alternate pack multiple 50 across 3 customers. |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX) AYY | `PKT` | ₹6.50 | 100 | **50** | 10 | 10 | `100(2)|150(2)|200(3)|500(2)|800(1)` | Wholesale orders fail suggested multiple 100 (80.0% div), but 100% match alternate pack multiple 50 across 10 customers. |
| `02669` | 567- DANCING BUTTERFLY R/G.(10P) VA | `PKT` | ₹45.00 | 10 | **5** | 12 | 12 | `5(1)|10(3)|15(1)|30(3)|40(1)|75(1)|100(2)` | Wholesale orders fail suggested multiple 10 (75.0% div), but 100% match alternate pack multiple 5 across 12 customers. |
| `02897` | W 2 1/2" F. PIPE(3 PCS)AYYANAR | `PKT` | ₹225.00 | 3 | **5** | 3 | 2 | `5(1)|10(2)` | Wholesale orders fail suggested multiple 3 (0.0% div), but 100% match alternate pack multiple 5 across 2 customers. |
| `03089` | 183- 7 CM PLAIN M.R.P. (10 DABBI=1B | `BOX` | ₹80.00 | 10 | **5** | 3 | 3 | `5(1)|20(1)|30(1)` | Wholesale orders fail suggested multiple 10 (66.7% div), but 100% match alternate pack multiple 5 across 3 customers. |
| `03090` | 184- 7 CM COL SARAVANA(10 DABBI=1BO | `BOX` | ₹90.00 | 10 | **5** | 3 | 3 | `5(1)|10(1)|20(1)` | Wholesale orders fail suggested multiple 10 (66.7% div), but 100% match alternate pack multiple 5 across 3 customers. |
| `03214` | 614- 45 CM G C SPL (10 P) COCK | `PKT` | ₹124.00 | 10 | **5** | 8 | 8 | `5(1)|10(4)|20(2)|60(1)` | Wholesale orders fail suggested multiple 10 (87.5% div), but 100% match alternate pack multiple 5 across 8 customers. |
| `03222` | 702- MULTI COLOUR ROCKET MERCURY (  | `PKT` | ₹113.00 | 6 | **2** | 7 | 7 | `6(5)|10(2)` | Wholesale orders fail suggested multiple 6 (71.4% div), but 100% match alternate pack multiple 2 across 7 customers. |
| `03265` | 753- L. B. BOMB GREEN W/F (10 P) B. | `PKT` | ₹80.00 | 10 | **5** | 3 | 3 | `10(2)|25(1)` | Wholesale orders fail suggested multiple 10 (66.7% div), but 100% match alternate pack multiple 5 across 3 customers. |
| `03272` | 760- THUNDER BOMB GREEN (10 P) S.T. | `PKT` | ₹130.00 | 10 | **5** | 3 | 3 | `5(2)|10(1)` | Wholesale orders fail suggested multiple 10 (33.3% div), but 100% match alternate pack multiple 5 across 3 customers. |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | `PKT` | ₹6.00 | 1 | **80** | 6 | 6 | `80(5)|320(1)` | Current overlay enforces 1 (assuming bundle billing), but billing UOM is PKT and 100% of wholesale orders across 6 customers are in multiples of 80 packets (₹480/bundle). Recommend changing pack multiple to 80. |
| `04055` | 1098- VATMAN BLACK SOM (12 PCS) | `PCS` | ₹21.00 | 12 | **2** | 9 | 9 | `10(1)|12(3)|24(2)|36(2)|60(1)` | Wholesale orders fail suggested multiple 12 (88.9% div), but 100% match alternate pack multiple 2 across 9 customers. |
| `04062` | 1105- SPIDER BLACK SOM ( 3 PCS) | `PCS` | ₹89.00 | 3 | **2** | 3 | 3 | `2(1)|6(2)` | Wholesale orders fail suggested multiple 3 (66.7% div), but 100% match alternate pack multiple 2 across 3 customers. |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS) | `BAG` | ₹11.00 | 50 | **10** | 11 | 11 | `20(1)|30(1)|40(1)|50(4)|100(2)|150(1)|400(1)` | Wholesale orders fail suggested multiple 50 (72.7% div), but 100% match alternate pack multiple 10 across 11 customers. |
| `04311` | 169- GOLD BIJALI OTHER (100 PCS) | `BAG` | ₹20.00 | 100 | **50** | 7 | 7 | `50(2)|100(1)|200(3)|300(1)` | Wholesale orders fail suggested multiple 100 (71.4% div), but 100% match alternate pack multiple 50 across 7 customers. |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS) | `BAG` | ₹21.00 | 100 | **10** | 6 | 6 | `20(1)|30(1)|100(2)|160(1)|200(1)` | Wholesale orders fail suggested multiple 100 (50.0% div), but 100% match alternate pack multiple 10 across 6 customers. |
| `04315` | 173- GOLD BIJALI SRIPATHI(100 PCS) | `BAG` | ₹30.00 | 100 | **10** | 3 | 3 | `30(1)|50(1)|100(1)` | Wholesale orders fail suggested multiple 100 (33.3% div), but 100% match alternate pack multiple 10 across 3 customers. |
| `04316` | 174- GOLD BIJALI AYYANAR(100 PCS) | `BAG` | ₹37.50 | 100 | **10** | 3 | 3 | `30(1)|100(2)` | Wholesale orders fail suggested multiple 100 (66.7% div), but 100% match alternate pack multiple 10 across 3 customers. |
| `04317` | 175- GOLD BIJALI COCK(100 PCS ) | `BAG` | ₹67.00 | 100 | **10** | 4 | 4 | `30(1)|250(2)|400(1)` | Wholesale orders fail suggested multiple 100 (25.0% div), but 100% match alternate pack multiple 10 across 4 customers. |
| `04680` | 725- 18 CM PENCIL VIRBALAJI ( 10 P  | `PKT` | ₹68.00 | 10 | **5** | 6 | 6 | `5(5)|10(1)` | Wholesale orders fail suggested multiple 10 (16.7% div), but 100% match alternate pack multiple 5 across 6 customers. |
| `04915` | 1013- SKY SHOT (10 P ) COCK | `BOX` | ₹86.00 | 10 | **5** | 10 | 10 | `5(3)|10(6)|40(1)` | Wholesale orders fail suggested multiple 10 (70.0% div), but 100% match alternate pack multiple 5 across 10 customers. |
| `05402` | 513- FLOWER POTS SUP DLX (2 P)SUPER | `PKT` | ₹65.00 | 2 | **5** | 7 | 7 | `5(4)|10(3)` | Wholesale orders fail suggested multiple 2 (42.9% div), but 100% match alternate pack multiple 5 across 7 customers. |
| `05403` | 514- FLOWER POTS SUP DLX (2 P) GOVI | `PKT` | ₹75.00 | 2 | **5** | 7 | 7 | `5(5)|10(1)|30(1)` | Wholesale orders fail suggested multiple 2 (28.6% div), but 100% match alternate pack multiple 5 across 7 customers. |

---

## 5. Deep-Dive: `RECOMMEND_REJECT` Candidates (103 Products)

The audit identified 103 products where enforcing the heuristic pack multiple would be **commercially harmful** because wholesale customers routinely purchase loose units or unconstrained quantities:

1. **Multi-Customer Contradictions (73 Products)**:  
   - These products have $\ge 3$ lines and $\ge 2$ customers, but divisibility by the heuristic multiple is low ($< 85\%$) and the greatest common divisor of observed orders is `1`.
   - *Prominent Example:* `00503` (`GIFT BOX GUDIYA ( 4 PCS)`). Heuristic suggested `4`. However, 7 distinct wholesale customers each ordered **exactly 1 box** (`QTY: 1.0(7)`). If a multiple of 4 were enforced, all 7 wholesale orders would have failed!
   - *Prominent Example:* `00447` (`KIDDY'S JOY F P 5IN 1 AYYAN ( 5 PCS)`). Orders across 5 customers: `1.0(2), 2.0(3)`. Customers buy 1 or 2 loose units.
   - *Prominent Example:* `00454` (`CRACKLING FOUNTAIN SIVASAKTHI (3 P)`). Orders across 10 customers: `1.0(1), 2.0(1), 3.0(1), 5.0(3), 10.0(3), 15.0(1)`. Unconstrained loose sales.

2. **Low-Volume Disproving Orders (30 Products)**:  
   - Products with 1 or 2 wholesale lines where a customer purchased a non-divisible quantity (e.g. 1 unit of a 5-pack fountain, or 2 units of a 12-pack sparkler).
   - Even with low volume, an actual wholesale dispatch of 1 unit proves that FoxPro accepted loose ordering. Enforcing the heuristic multiple would block future re-orders.

---

## 6. Deep-Dive: `RECOMMEND_APPROVE` Candidates (146 Products)

146 products demonstrate **100% empirical compliance** across multiple wholesale customers and are ready for business owner sign-off:
- **22 Existing Overlays**: Verified to be 100% compliant in D2627.
- **124 New Heuristic Candidates**: Products where multi-customer wholesale orders strictly respect the pack multiple.
  - *10 CM Classic Sparklers (`(5 P)`)*: `00132`, `00133`, `00134`, `00136`, `00137`, `00138`, `00139` — Across 11 to 13 wholesale customers, 100% of orders were multiples of 5 (e.g. 10, 20, 30, 40, 50, 100, 150 packets).
  - *20 & 24 DLX Crackers (`(10 P)`)*: `00250`, `00251`, `00252`, `00253`, `00255` — Across 6 to 14 customers, 100% of orders were multiples of 10 packets.
  - *Kurvi & Parrot Crackers (`(25 P)`)*: `00288`, `00289`, `00292`, `00293`, `00294` — Across 4 to 12 customers, 100% of orders were multiples of 25 packets.

---

## 7. Deep-Dive: `INSUFFICIENT_HISTORY` Candidates (158 Products)

158 products cannot be approved or rejected with confidence based on D2627 data alone:
- **96 Products with Zero Sales Lines**: These items have not yet had transactions recorded in D2627.
- **62 Products with Single-Customer or Low-Volume Divisible Sales**: Products where 1 customer purchased a multiple of the pack (e.g. 1 order of 10), but multi-customer corroboration is absent.
- **Policy Recommendation**: Retain safe default `1` for all 158 products. Tablet POS displays the suggested multiple as a soft increment guide, but the server will never reject a wholesale order.

---

## 8. Complete Decision Reference Table (All 439 Candidate Products)

The complete dataset is exported to [`PACKAGING_RULE_DECISIONS.csv`](./PACKAGING_RULE_DECISIONS.csv). Below is the comprehensive summary table organized by recommendation category:

### Category 1: RECOMMEND_CHANGE (32 Products)
*Products where historical sales prove an alternate pack multiple should be enforced.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00080` | 120- ASST CARTOON BEN TEN(25P) | `PKT` | ₹55.00 | 25 | 1 | 7 | 7 | 0.0% | `RECOMMEND_CHANGE` | **4** | HIGH | Wholesale orders fail suggested multiple 25 (0.0% div), but ... |
| `00081` | 121- SNAKE CARTOON(25P)SAMLL A | `PKT` | ₹55.00 | 25 | 1 | 8 | 8 | 0.0% | `RECOMMEND_CHANGE` | **4** | HIGH | Wholesale orders fail suggested multiple 25 (0.0% div), but ... |
| `00109` | 178- 9 CM PLAIN INDRA (10 DABB | `BOX` | ₹65.00 | 10 | 1 | 5 | 5 | 80.0% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (80.0% div), but... |
| `00610` | 595- G C BIG T/MEENA (25 PCS)  | `PKT` | ₹75.00 | 25 | 1 | 5 | 5 | 0.0% | `RECOMMEND_CHANGE` | **4** | HIGH | Wholesale orders fail suggested multiple 25 (0.0% div), but ... |
| `00611` | 596- G C BIG GANESH (25 PCS) ( | `PKT` | ₹80.00 | 25 | 1 | 7 | 7 | 0.0% | `RECOMMEND_CHANGE` | **4** | HIGH | Wholesale orders fail suggested multiple 25 (0.0% div), but ... |
| `00691` | 122- RAJDHANI RAIL(10 PCS)AYYA | `PKT` | ₹65.00 | 10 | 1 | 4 | 4 | 50.0% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (50.0% div), but... |
| `00876` | 601- G C ASOKA BIG SIZE GANESH | `PKT` | ₹72.50 | 10 | 1 | 7 | 7 | 85.7% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (85.7% div), but... |
| `00925` | 602- G C ASOKA S.T.D (10 P) (5 | `PKT` | ₹88.00 | 10 | 1 | 9 | 9 | 55.6% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (55.6% div), but... |
| `02081` | 142- MAGIC FOUNTAIN OVEEYA(10  | `PKT` | ₹120.00 | 10 | 1 | 3 | 3 | 33.3% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (33.3% div), but... |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX | `PKT` | ₹6.00 | 100 | 1 | 3 | 3 | 33.3% | `RECOMMEND_CHANGE` | **50** | MEDIUM | Wholesale orders fail suggested multiple 100 (33.3% div), bu... |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX | `PKT` | ₹6.50 | 100 | 1 | 10 | 10 | 80.0% | `RECOMMEND_CHANGE` | **50** | HIGH | Wholesale orders fail suggested multiple 100 (80.0% div), bu... |
| `02669` | 567- DANCING BUTTERFLY R/G.(10 | `PKT` | ₹45.00 | 10 | 1 | 12 | 12 | 75.0% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (75.0% div), but... |
| `02897` | W 2 1/2" F. PIPE(3 PCS)AYYANAR | `PKT` | ₹225.00 | 3 | 1 | 3 | 2 | 0.0% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 3 (0.0% div), but 1... |
| `03089` | 183- 7 CM PLAIN M.R.P. (10 DAB | `BOX` | ₹80.00 | 10 | 1 | 3 | 3 | 66.7% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (66.7% div), but... |
| `03090` | 184- 7 CM COL SARAVANA(10 DABB | `BOX` | ₹90.00 | 10 | 1 | 3 | 3 | 66.7% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (66.7% div), but... |
| `03214` | 614- 45 CM G C SPL (10 P) COCK | `PKT` | ₹124.00 | 10 | 1 | 8 | 8 | 87.5% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (87.5% div), but... |
| `03222` | 702- MULTI COLOUR ROCKET MERCU | `PKT` | ₹113.00 | 6 | 1 | 7 | 7 | 71.4% | `RECOMMEND_CHANGE` | **2** | HIGH | Wholesale orders fail suggested multiple 6 (71.4% div), but ... |
| `03265` | 753- L. B. BOMB GREEN W/F (10  | `PKT` | ₹80.00 | 10 | 1 | 3 | 3 | 66.7% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (66.7% div), but... |
| `03272` | 760- THUNDER BOMB GREEN (10 P) | `PKT` | ₹130.00 | 10 | 1 | 3 | 3 | 33.3% | `RECOMMEND_CHANGE` | **5** | MEDIUM | Wholesale orders fail suggested multiple 10 (33.3% div), but... |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | `PKT` | ₹6.00 | 1 | 1 | 6 | 6 | 100.0% | `RECOMMEND_CHANGE` | **80** | HIGH | Current overlay enforces 1 (assuming bundle billing), but bi... |
| `04055` | 1098- VATMAN BLACK SOM (12 PCS | `PCS` | ₹21.00 | 12 | 1 | 9 | 9 | 88.9% | `RECOMMEND_CHANGE` | **2** | HIGH | Wholesale orders fail suggested multiple 12 (88.9% div), but... |
| `04062` | 1105- SPIDER BLACK SOM ( 3 PCS | `PCS` | ₹89.00 | 3 | 1 | 3 | 3 | 66.7% | `RECOMMEND_CHANGE` | **2** | MEDIUM | Wholesale orders fail suggested multiple 3 (66.7% div), but ... |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS | `BAG` | ₹11.00 | 50 | 1 | 11 | 11 | 72.7% | `RECOMMEND_CHANGE` | **10** | HIGH | Wholesale orders fail suggested multiple 50 (72.7% div), but... |
| `04311` | 169- GOLD BIJALI OTHER (100 PC | `BAG` | ₹20.00 | 100 | 1 | 7 | 7 | 71.4% | `RECOMMEND_CHANGE` | **50** | HIGH | Wholesale orders fail suggested multiple 100 (71.4% div), bu... |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS | `BAG` | ₹21.00 | 100 | 1 | 6 | 6 | 50.0% | `RECOMMEND_CHANGE` | **10** | HIGH | Wholesale orders fail suggested multiple 100 (50.0% div), bu... |
| `04315` | 173- GOLD BIJALI SRIPATHI(100  | `BAG` | ₹30.00 | 100 | 1 | 3 | 3 | 33.3% | `RECOMMEND_CHANGE` | **10** | MEDIUM | Wholesale orders fail suggested multiple 100 (33.3% div), bu... |
| `04316` | 174- GOLD BIJALI AYYANAR(100 P | `BAG` | ₹37.50 | 100 | 1 | 3 | 3 | 66.7% | `RECOMMEND_CHANGE` | **10** | MEDIUM | Wholesale orders fail suggested multiple 100 (66.7% div), bu... |
| `04317` | 175- GOLD BIJALI COCK(100 PCS  | `BAG` | ₹67.00 | 100 | 1 | 4 | 4 | 25.0% | `RECOMMEND_CHANGE` | **10** | MEDIUM | Wholesale orders fail suggested multiple 100 (25.0% div), bu... |
| `04680` | 725- 18 CM PENCIL VIRBALAJI (  | `PKT` | ₹68.00 | 10 | 1 | 6 | 6 | 16.7% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (16.7% div), but... |
| `04915` | 1013- SKY SHOT (10 P ) COCK | `BOX` | ₹86.00 | 10 | 1 | 10 | 10 | 70.0% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 10 (70.0% div), but... |
| `05402` | 513- FLOWER POTS SUP DLX (2 P) | `PKT` | ₹65.00 | 2 | 1 | 7 | 7 | 42.9% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 2 (42.9% div), but ... |
| `05403` | 514- FLOWER POTS SUP DLX (2 P) | `PKT` | ₹75.00 | 2 | 1 | 7 | 7 | 28.6% | `RECOMMEND_CHANGE` | **5** | HIGH | Wholesale orders fail suggested multiple 2 (28.6% div), but ... |

### Category 2: RECOMMEND_APPROVE (146 Products)
*Products where historical wholesale sales confirm 100% compliance with candidate multiple.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00079` | 119- ASST CARTOON(10 PCS)DURGE | `PKT` | ₹13.50 | 1 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical sales across 3 customers confirm single/loose bil... |
| `00082` | 124- BIG NAGGOLI PANDYAN BLACK | `BUNDLE` | ₹150.00 | 1 | 1 | 15 | 15 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 15 customers confirm single/loose bi... |
| `00083` | 125- BIG NAGGOLI PANDYAN RED(1 | `BUNDLE` | ₹155.00 | 1 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 6 customers confirm single/loose bil... |
| `00110` | 179- 9 CM COL INDRA (10 DABBI= | `BOX` | ₹69.50 | 10 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00132` | 221- 10 CM PLAIN CLASSIC (5 P) | `PKT` | ₹12.50 | 5 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00133` | 222- 10 CM COL CLASSIC (5 P) | `PKT` | ₹13.50 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00134` | 223- 10 CM GREEN CLASSIC (5 P) | `PKT` | ₹13.00 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00136` | 224- 10 CM RED CLASSIC(5 P) | `PKT` | ₹13.50 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00137` | 225- 10 CM 2 IN 1 CLASSIC(5 P) | `PKT` | ₹13.50 | 5 | 1 | 13 | 13 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 13 customers are divisible... |
| `00138` | 226- 12 CM PLAIN LX CLASSIC (5 | `PKT` | ₹14.50 | 5 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00139` | 227- 12 CM COL LX CLASSIC (5 P | `PKT` | ₹15.50 | 5 | 1 | 12 | 12 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `00140` | 228- 12 CM PLAIN DLX CLASSIC ( | `PKT` | ₹16.50 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00142` | 229- 12 CM COL DLX CLASSIC (5  | `PKT` | ₹17.50 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00143` | 230- 12 CM GREEN LX CLASSIC (5 | `PKT` | ₹14.75 | 5 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00178` | 148- RED BIJALI ROSE (100 PCS | `BAG` | ₹17.50 | 10 | 10 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 10 customers confirm 100% ... |
| `00181` | 150- RED BIJALI AYYANAR (100 P | `BAG` | ₹30.00 | 10 | 10 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 7 customers confirm 100% c... |
| `00183` | 152- RED BIJALI S.T.D.(100 PCS | `BAG` | ₹53.00 | 10 | 10 | 12 | 12 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 12 customers confirm 100% ... |
| `00184` | 153- RED BIJALI SONY (100 PCS) | `BAG` | ₹60.00 | 10 | 10 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | Historical wholesale sales across 3 customers confirm 100% c... |
| `00186` | 290- 10 CHORASA MUNNA DURGESH( | `BUNDLE` | ₹335.00 | 1 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 7 customers confirm single/loose bil... |
| `00223` | 293- 16 CHORSA B GROUP (50P= 1 | `PKT` | ₹7.25 | 50 | 50 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **50** | HIGH | Historical wholesale sales across 9 customers confirm 100% c... |
| `00224` | 294- 28 CHORSA K.R.K (50P= 1 B | `PKT` | ₹12.00 | 50 | 50 | 15 | 15 | 100.0% | `RECOMMEND_APPROVE` | **50** | HIGH | Historical wholesale sales across 15 customers confirm 100% ... |
| `00225` | 295- 28 CHORSA TAJ  T/MEENA (5 | `PKT` | ₹13.25 | 50 | 50 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **50** | MEDIUM | Historical wholesale sales across 3 customers confirm 100% c... |
| `00250` | 308- 20 DLX KING GANESH DURAI( | `PKT` | ₹25.50 | 10 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00252` | 310- 24 DLX RAGURAM ( 10 P) | `PKT` | ₹30.00 | 10 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00253` | 311- 24 DLX GANESH DURAI( 10 P | `PKT` | ₹32.00 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00255` | 313- 28 DLX RAGURAM(10 P) | `PKT` | ₹37.50 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00256` | 314- 32 DLX KICK SHOT BALAJI(  | `PKT` | ₹65.00 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00257` | 315- 48 DLX RAGURAM ( 5 P) | `PKT` | ₹50.00 | 5 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00288` | 329- 2' PARROT AYYANAR (25 PCS | `PKT` | ₹5.00 | 25 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **25** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00289` | 330- 2 3/4 KURVI DURGESH (25 P | `PKT` | ₹6.50 | 25 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `00291` | 331- 2 3/4 KURVI VELVAN (10 PC | `PKT` | ₹7.50 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00292` | 332- 2 3/4 KURVI GEMS (25 P) | `PKT` | ₹7.75 | 25 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00293` | 333- 2 3/4 GREEN PARROT PONMAL | `PKT` | ₹9.50 | 25 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **25** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00297` | 337- 3 1/2 BEN TEN DURGESH/JAY | `PKT` | ₹9.50 | 15 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **15** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00298` | 338- 3 1/2 JOKER SADA BAJAJI(1 | `PKT` | ₹10.75 | 10 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `00299` | 339- 3 1/2 MIX LABEL SADA AYYA | `PKT` | ₹13.50 | 10 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00300` | 340- 3 1/2 GREEN PARROT PONMAL | `PKT` | ₹14.00 | 10 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `00301` | 341- 3 1/2 ELEPHANT I.N(10 P) | `PKT` | ₹14.50 | 10 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00325` | 399- 2 SOUND DHAMAKA RAJHARISH | `PKT` | ₹22.00 | 10 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `00326` | 400- 2 SOUND DHAMAKA NM JYOTHI | `PKT` | ₹25.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00328` | 402- 2 SOUND DHAMAKA I.N. (10P | `PKT` | ₹30.00 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00427` | 444- FLOWER POTS SMALL RAJLAXM | `PKT` | ₹38.00 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `00455` | 534- JADUGAR UV.BOX AYYAN (4 P | `PKT` | ₹260.00 | 1 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 9 customers confirm single/loose bil... |
| `00456` | 535- MANORANJAN U.V.BOX AYYAN( | `PKT` | ₹260.00 | 1 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 7 customers confirm single/loose bil... |
| `00491` | 550- SADA MATKA ANAR OTHER (10 | `PCS` | ₹15.00 | 100 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **100** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00536` | 591- G C BIG W MERCURY(10 P)(5 | `PKT` | ₹44.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00565` | 708- 18 T STAR SRIPATHI(10P) 1 | `PKT` | ₹16.00 | 10 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00567` | 710- 48 T STAR (10P) SRIPATHI  | `PKT` | ₹50.00 | 10 | 1 | 12 | 12 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `00614` | 735- BULLET BOMB MINI SRI ATHI | `PKT` | ₹14.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00615` | 736- MINI BULLET BOMB T/MEENA( | `PKT` | ₹16.50 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00616` | 737- BULLET BOMB MINI SRIPATHI | `PKT` | ₹18.00 | 10 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `00617` | 738- BULLET BOMB MEDIUM T/MEEN | `PKT` | ₹21.00 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00618` | 739- BULLET BOMB MEDIUM APPLE( | `PKT` | ₹21.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `00621` | 742- BULLET BOMB BIG DLX T/MEE | `PKT` | ₹32.50 | 10 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00630` | 751- SOLDIER BOMB GREEN W/G (1 | `PKT` | ₹75.00 | 10 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `00707` | 138- GANGA JAMUNA SRI PATHI(5P | `PKT` | ₹45.00 | 5 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `00769` | 600- G C ASOKA W MERCURY(10 P) | `PKT` | ₹67.50 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `00848` | 231- 12 CM RED LX CLASSIC (5 P | `PKT` | ₹17.50 | 5 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `01167` | 139- GANGA JAMUNA OVEETA(5P) | `PKT` | ₹52.00 | 5 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `01176` | 141- GANGA JAMUNA MERCURY( 5 P | `PKT` | ₹65.00 | 5 | 1 | 4 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `02154` | 1119- RING CAPS (1OOPKT= 1 BOX | `PKT` | ₹7.00 | 100 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **100** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `02157` | 1121- MISSILE SIREN(127X1)TITA | `PKT` | ₹65.00 | 1 | 1 | 13 | 13 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 13 customers confirm single/loose bi... |
| `02660` | 666- BABY ROCKET RAJ LAXMI (10 | `PKT` | ₹30.00 | 10 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `02676` | 667- COLOUR ROCKET AYYANAR (10 | `PKT` | ₹48.50 | 10 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `02680` | 671- ROCKET BOMB (10P) 5P AYYA | `PKT` | ₹55.00 | 5 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `02681` | 672- ROCKET BOMB (10P) 5P GANE | `PKT` | ₹58.00 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `02756` | 606- G C SPL (10 P) VENKATESH | `PKT` | ₹36.00 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `02765` | 232- 12 CM 2 IN 1 CLASSIC(5 P) | `PKT` | ₹17.00 | 5 | 1 | 13 | 13 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 13 customers are divisible... |
| `02852` | 607- G C SPL (10 P) T/MEENA | `PKT` | ₹56.00 | 10 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `03088` | 114- R & G MATCH BOX SHANTHI(6 | `BUNDLE` | ₹500.00 | 1 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **1** | HIGH | Historical sales across 7 customers confirm single/loose bil... |
| `03097` | 235- 15 CM PLAIN AB MAGIC CLAS | `PKT` | ₹22.00 | 5 | 1 | 18 | 17 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 17 customers are divisible... |
| `03098` | 236- 15 CM PLAIN DLX CLASSIC(5 | `PKT` | ₹25.00 | 5 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `03099` | 237- 15 CM PLAIN BOXE(2P CELLE | `PKT` | ₹26.00 | 2 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **2** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03100` | 238- 15 CM COL AB MAGIC CLASSI | `PKT` | ₹25.00 | 5 | 1 | 12 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `03101` | 239- 15 CM COL DLX CLASSIC (5  | `PKT` | ₹27.50 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03103` | 241- 15 CM GREEN CLASSIC (5 P) | `PKT` | ₹23.00 | 5 | 1 | 16 | 15 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03104` | 242- 15 CM RED CLASSIC  (5 P) | `PKT` | ₹27.50 | 5 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `03105` | 243- 15 CM 2 IN 1 CLASSIC (5 P | `PKT` | ₹29.00 | 5 | 1 | 15 | 15 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03110` | 248- 30 CM PLAIN AB MAGIC CLAS | `PKT` | ₹22.00 | 5 | 1 | 15 | 15 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 15 customers are divisible... |
| `03208` | 608- G C SPL (10 P) GANESH | `PKT` | ₹57.50 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03231` | 721- 10 CM PENCIL VIRBALAJI (  | `PKT` | ₹36.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `03266` | 754- LALKAR BOMB GREEN W/F(10  | `PKT` | ₹85.00 | 10 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04048` | 1091- ROBOT BLACK S-61 SOM (12 | `PCS` | ₹12.50 | 12 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04051` | 1094- 86 BLACK SOM(12 PCS) | `PCS` | ₹17.50 | 12 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **12** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04052` | 1095- 86 COLOUR SOM (12 PCS) | `PCS` | ₹23.00 | 12 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04053` | 1096- NICE BLACK SOM(12 PCS) | `PCS` | ₹18.00 | 12 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04054` | 1097- NICE COLOUR SOM (12 PCS) | `PCS` | ₹23.50 | 12 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04056` | 1099- VATMAN COLOUR SOM (12 PC | `PCS` | ₹26.00 | 12 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **12** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04057` | 1100- DOLPHIN BLACK SOM(6 PCS) | `PCS` | ₹29.00 | 6 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **6** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04058` | 1101- DOLPHIN COLOUR SOM (6 PC | `PCS` | ₹37.00 | 6 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **6** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04094` | 1084- PATANG BALLOON (10 P) KI | `BOX` | ₹16.50 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04246` | 251- 30 CM COL AB MAGIC CLASSI | `PKT` | ₹25.00 | 5 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04247` | 252- 30 CM COL DLX CLASSIC (5  | `PKT` | ₹27.50 | 5 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04249` | 254- 30 CM GREEN CLASSIC (5 P) | `PKT` | ₹23.00 | 5 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04251` | 256- 30 CM RED CLASSIC (5 P) | `PKT` | ₹27.00 | 5 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04253` | 258- 30 CM 2 IN 1 CLASSIC (5 P | `PKT` | ₹27.00 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04301` | 159- STRIPPED BIJALI MERCURY(5 | `BAG` | ₹25.50 | 10 | 10 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 5 customers confirm 100% c... |
| `04303` | 161- STRIPPED BIJALI AYYANAR(1 | `BAG` | ₹32.00 | 10 | 10 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | Historical wholesale sales across 7 customers confirm 100% c... |
| `04305` | 163- STRIPPED BIJALI GAINT S.T | `BAG` | ₹50.00 | 10 | 10 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | Historical wholesale sales across 3 customers confirm 100% c... |
| `04341` | 296- 28 CHORSA TURKEY  RAJLAXM | `PKT` | ₹13.50 | 50 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **50** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04346` | 301- 28 GAINT CHORSA (25 P) K. | `PKT` | ₹17.50 | 25 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04348` | 303- 28 GAINT CHORSA (25 P) SE | `PKT` | ₹19.00 | 25 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **25** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04351` | 316- 50 DLX RAGURAM ( 5 P) | `PKT` | ₹52.00 | 5 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04370` | 342- 3 1/2 GREEN PARROT W/F VE | `PKT` | ₹15.00 | 10 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04378` | 350- 4 GREEN PARROT SADA VELAV | `PKT` | ₹14.50 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04381` | 353- 4 MICKEY MOUSE BALAJI( 10 | `PKT` | ₹16.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04382` | 354- 4 GREEN PARROT VELAVAN (1 | `PKT` | ₹18.50 | 10 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04383` | 355- 4 ELEPHANT I.N (10 P) | `PKT` | ₹18.50 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04384` | 356- 4 GREEN PARROT SADA PONMA | `PKT` | ₹19.50 | 10 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04385` | 357- 4  MIX LABEL AYYANAR (10  | `PKT` | ₹21.00 | 10 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04386` | 358- 4 PARROT COCK (10 P) | `PKT` | ₹22.50 | 10 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04400` | 372- 4 DLX PARROT W/F ( 10 P)V | `PKT` | ₹29.00 | 10 | 1 | 12 | 12 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `04405` | 377- 4 SUP DLX MIX LABEL(10P)A | `PKT` | ₹27.00 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04411` | 383- 5 DLX JALLIKATTI DURGESH  | `PKT` | ₹27.00 | 10 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04434` | 409- 3 SOUND DHAMAKA RATHANAA( | `PKT` | ₹34.00 | 10 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04581` | 622- G C DLX  (10 P) 5 P T/MEE | `PKT` | ₹95.00 | 5 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04583` | 624- G C DLX  (10 P) 5 P MERCU | `PKT` | ₹125.00 | 5 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04584` | 625- G C DLX  (10 P) 5 P COLOU | `PKT` | ₹115.00 | 5 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04585` | 626- G C DLX  W (10 P) 5 P I.N | `PKT` | ₹130.00 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04586` | 627- G C DLX  (10 P) 5 P GANES | `PKT` | ₹140.00 | 5 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04589` | 630- G C DLX  (10 P) 5 P S.T.D | `PKT` | ₹195.00 | 5 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04590` | 631- 70 CM G C DLX  (10 P) 5 P | `PKT` | ₹210.00 | 5 | 1 | 12 | 11 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `04592` | 633- G C DLX  U.V. BOX (10 P)  | `PKT` | ₹135.00 | 5 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04595` | 636- G C DLX SPINNER ( 10 P )A | `PKT` | ₹160.00 | 10 | 1 | 7 | 7 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 7 customers are divisible ... |
| `04596` | 637- G C DLX  SPINNER(10P) 5P  | `PKT` | ₹175.00 | 5 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04613` | 650- SUDARSHAN CHAKKAR ANIL (  | `PKT` | ₹153.00 | 1 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical sales across 4 customers confirm single/loose bil... |
| `04616` | 653- GIANT WHEEL AYYAN (5 PCS) | `PKT` | ₹175.00 | 1 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical sales across 4 customers confirm single/loose bil... |
| `04619` | 656- WHISTLING WHEEL COCK (5 P | `PKT` | ₹125.00 | 5 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `04621` | 658- TITANIC WHEEL DURGESH ( 5 | `PKT` | ₹130.00 | 5 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **5** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04625` | 662- SKY  WHEEL AYYAN (5 PCS)  | `PKT` | ₹345.00 | 1 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **1** | MEDIUM | Historical sales across 3 customers confirm single/loose bil... |
| `04636` | 675- SILVER ROCKET(10P)5P AYYA | `PKT` | ₹75.00 | 5 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `04639` | 678- LUNIK ROCKET (10 P) 2P T/ | `PKT` | ₹80.00 | 2 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |
| `04641` | 680- LUNIK ROCKET (10 P) 2P ME | `PKT` | ₹112.00 | 2 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04646` | 685- 2 SOUND ROCKET (10 P) 2P  | `PKT` | ₹82.00 | 2 | 1 | 12 | 12 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 12 customers are divisible... |
| `04647` | 686- 2 SOUND ROCKET (10 P) 2P  | `PKT` | ₹120.00 | 2 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `04649` | 688- 2 SOUND ROCKET (10 P) 2P  | `PKT` | ₹125.00 | 2 | 1 | 6 | 6 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 6 customers are divisible ... |
| `04679` | 724- 15 CM PENCIL VIRBALAJI (  | `PKT` | ₹53.00 | 10 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `04684` | 729- MULTI COLOUR CANDLE S.T.D | `PKT` | ₹99.00 | 5 | 1 | 4 | 4 | 100.0% | `RECOMMEND_APPROVE` | **5** | MEDIUM | 100.0% of wholesale orders across 4 customers are divisible ... |
| `04910` | 1008- 18 HAND SHOT ( 2 PCS ) M | `BOX` | ₹400.00 | 2 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **2** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `05426` | 692- 3 SOUND ROCKET (10 P) 2P  | `PKT` | ₹85.00 | 2 | 1 | 8 | 8 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 8 customers are divisible ... |
| `05428` | 694- 3 SOUND ROCKET (10 P) 2P  | `PKT` | ₹140.00 | 2 | 1 | 5 | 5 | 100.0% | `RECOMMEND_APPROVE` | **2** | HIGH | 100.0% of wholesale orders across 5 customers are divisible ... |
| `06134` | W COLD PYRO R&G BOX 3.M.35.S ( | `BOX` | ₹80.00 | 6 | 1 | 3 | 3 | 100.0% | `RECOMMEND_APPROVE` | **6** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `06135` | W COLD PYRO YELLO BOX 3.M.30.S | `BOX` | ₹120.00 | 10 | 1 | 4 | 3 | 100.0% | `RECOMMEND_APPROVE` | **10** | MEDIUM | 100.0% of wholesale orders across 3 customers are divisible ... |
| `06171` | 129- KIT-KAT(10 P)YUVA | `PKT` | ₹18.50 | 10 | 1 | 11 | 11 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 11 customers are divisible... |
| `06173` | 131- KIT-KAT (10 P) RAJHARISH | `PKT` | ₹20.00 | 10 | 1 | 9 | 9 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 9 customers are divisible ... |
| `06174` | 132- KIT-KAT(10 P)U.V.BOX VETR | `PKT` | ₹21.00 | 10 | 1 | 10 | 10 | 100.0% | `RECOMMEND_APPROVE` | **10** | HIGH | 100.0% of wholesale orders across 10 customers are divisible... |

### Category 3: RECOMMEND_REJECT (103 Products)
*Products where wholesale order history contradicts enforcement (sold loose/unconstrained).*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00111` | 180- 9 CM PLAIN CLASSIC (10DAB | `BOX` | ₹78.50 | 10 | 1 | 5 | 5 | 40.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (40.0% div; non-... |
| `00112` | 181- 9 CM COL CLASSIC (10 DABB | `BOX` | ₹89.00 | 10 | 1 | 4 | 4 | 50.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (50.0% div; non-... |
| `00438` | 517- TRI COL FOUNTAIN RAJHARIS | `PKT` | ₹185.00 | 5 | 1 | 9 | 9 | 44.4% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (44.4% div; non-d... |
| `00440` | 519- TRI COL FOUNTAIN MERCURY  | `PKT` | ₹265.00 | 10 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5, 2] contradicts suggested p... |
| `00441` | 520- TRI COL FOUNTAIN COCK (5  | `PKT` | ₹297.00 | 5 | 1 | 4 | 4 | 75.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `00443` | 522- TRI COL FOUNTAIN T/MEENA  | `PKT` | ₹235.00 | 5 | 1 | 9 | 9 | 88.9% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (88.9% div; non-d... |
| `00445` | 524- COL FOG FOUNTAIN S.T.D.(5 | `PKT` | ₹77.50 | 5 | 1 | 5 | 5 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `00446` | 525- JET FOUNTAIN W S.T.D(5 P) | `PKT` | ₹85.00 | 5 | 1 | 5 | 5 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `00447` | 526- KIDDY'S JOY F P 5IN 1 AYY | `PKT` | ₹165.00 | 5 | 1 | 5 | 5 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (0.0% div; non-di... |
| `00448` | 527- MINI POPPERS 5 IN 1 MERCU | `PKT` | ₹175.00 | 5 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (0.0% div; non-di... |
| `00450` | 529- TORA TORA F. POT 5 IN 1 A | `PKT` | ₹355.00 | 5 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `00454` | 533- CRACKLING FOUNTAIN SIVASA | `PKT` | ₹200.00 | 3 | 1 | 10 | 10 | 30.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (30.0% div; non-d... |
| `00460` | 539- GOLDEN WHISTE SMALL (2P)S | `PKT` | ₹150.00 | 2 | 1 | 5 | 5 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (60.0% div; non-d... |
| `00461` | 540- CHOTA BHAI F P MINI SIREN | `PKT` | ₹150.00 | 5 | 1 | 8 | 8 | 87.5% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (87.5% div; non-d... |
| `00493` | 552- TIM TIM GUDIYA ( 5 PCS ) | `BOX` | ₹165.00 | 5 | 1 | 11 | 11 | 81.8% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (81.8% div; non-d... |
| `00494` | 553- LITTLE STAR ANAR GUDIYA ( | `BOX` | ₹270.00 | 5 | 1 | 13 | 13 | 76.9% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (76.9% div; non-d... |
| `00495` | 554- 2 IN 1 ANAR GUDIYA (10 PC | `BOX` | ₹325.00 | 10 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `00496` | 555- GOLDEN STAR GUDIYA  ( 5PC | `BOX` | ₹270.00 | 5 | 1 | 4 | 4 | 50.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `00497` | 556- ASHARFI GUDIYA ( 5 PCS) | `BOX` | ₹300.00 | 5 | 1 | 5 | 5 | 20.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (20.0% div; non-d... |
| `00499` | 557- JASMINE GUDIYA ( 5PCS) | `BOX` | ₹300.00 | 5 | 1 | 5 | 5 | 40.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (40.0% div; non-d... |
| `00501` | 558- DAZZLE GUDIYA ( 5 PCS) | `BOX` | ₹465.00 | 5 | 1 | 4 | 4 | 25.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (25.0% div; non-d... |
| `00502` | 559- DELUXE GUDIYA ( 4 PCS) | `BOX` | ₹500.00 | 4 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2] contradicts suggested pack... |
| `00503` | 560- GIFT BOX GUDIYA ( 4 PCS) | `BOX` | ₹650.00 | 4 | 1 | 7 | 7 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 4 (0.0% div; non-di... |
| `00535` | 590- G C BIG JENIS(10 P)(5P) | `PKT` | ₹40.00 | 10 | 1 | 5 | 5 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (60.0% div; non-... |
| `00537` | 592- G C BIG R/G S.T.D (25 P)( | `PKT` | ₹53.00 | 25 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5] contradicts suggested pack... |
| `00542` | 645- DISCO WHEEL GAYATHRI(10 P | `PKT` | ₹76.00 | 10 | 1 | 10 | 10 | 50.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (50.0% div; non-... |
| `00544` | 647- SILVER GAINT WHEEL MERCUR | `PKT` | ₹165.00 | 10 | 1 | 8 | 8 | 12.5% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (12.5% div; non-... |
| `00609` | 594- G C BIG VENKATESH (25 PCS | `PKT` | ₹45.00 | 25 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [16] contradicts suggested pac... |
| `00744` | 541- MINI SIREM F. POT COCK (  | `PKT` | ₹175.00 | 3 | 1 | 9 | 9 | 22.2% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (22.2% div; non-d... |
| `00745` | 542- BIG SIREM F. POT COCK ( 3 | `PKT` | ₹280.00 | 3 | 1 | 5 | 5 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `02124` | 603- G C ASOKA SPINNER W JENIS | `PKT` | ₹75.00 | 10 | 1 | 10 | 10 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (60.0% div; non-... |
| `02525` | 1087- BULLET ROCKET YUG ( 36 P | `PCS` | ₹108.00 | 36 | 1 | 3 | 3 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 36 (0.0% div; non-d... |
| `02665` | 283- 15 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `02832` | 182- 9 CM 2 IN 1 CLASSIC(10DAB | `BOX` | ₹120.00 | 10 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `03091` | 185- 7 CM GREEN SARAVANA (10 D | `BOX` | ₹105.00 | 10 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5, 5] contradicts suggested p... |
| `03093` | 187- 7 CM COL VASANTHA(10 DABB | `BOX` | ₹95.00 | 10 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5] contradicts suggested pack... |
| `03107` | 245- 15 CM 2IN1 BOXE(2P CELLEP | `PKT` | ₹31.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [45] contradicts suggested pac... |
| `03175` | 581- SUPER DRONE W AYYAN( 5 PC | `PKT` | ₹170.00 | 5 | 1 | 3 | 3 | 33.3% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (33.3% div; non-d... |
| `03176` | 582- HELICOPTER AYYAN ( 5PCS) | `PKT` | ₹80.00 | 5 | 1 | 9 | 9 | 66.7% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `03177` | 583- HELICOPTER R. KRISHNA.( 5 | `PKT` | ₹75.00 | 5 | 1 | 10 | 10 | 70.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (70.0% div; non-d... |
| `03216` | 696- WHISTLING ROCKET K.M.RAJA | `PKT` | ₹115.00 | 2 | 1 | 5 | 5 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `03225` | 705- PARACHUTE ROCKET AYYAN (4 | `PKT` | ₹375.00 | 2 | 1 | 3 | 3 | 66.7% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 2 (66.7% div; non-d... |
| `03275` | 763- V.I.P BOMB GREEN S.Q (6 P | `PKT` | ₹140.00 | 6 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [20] contradicts suggested pac... |
| `04005` | 841- 7 SHOTS OTHER(5 PCS) (5P) | `BOX` | ₹65.00 | 5 | 1 | 12 | 12 | 83.3% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (83.3% div; non-d... |
| `04007` | 843- 7 SHOTS MERCURY (5 PCS) ( | `BOX` | ₹120.00 | 5 | 1 | 10 | 10 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (80.0% div; non-d... |
| `04008` | 844- 7 SHOTS I.N (5 PCS) (5P) | `BOX` | ₹136.00 | 5 | 1 | 3 | 3 | 66.7% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04009` | 845- 7 SHOTS ANIL (5 PCS) (5P) | `BOX` | ₹170.00 | 5 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2] contradicts suggested pack... |
| `04014` | 850- 7 SHOTS I. N.(10 PCS | `BOX` | ₹270.00 | 10 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5, 5] contradicts suggested p... |
| `04015` | 851- 7 SHOTS MERCURY(10 PCS) | `BOX` | ₹250.00 | 10 | 1 | 5 | 5 | 20.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (20.0% div; non-... |
| `04028` | 1060- COL SMOKE DHUA 5COL(5P)S | `PKT` | ₹120.00 | 5 | 1 | 10 | 10 | 60.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (60.0% div; non-d... |
| `04050` | 1093- V-35 BLACK VISHNU(10 PCS | `PCS` | ₹15.00 | 10 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [48] contradicts suggested pac... |
| `04059` | 1102- TIGER BLACK SOM(12 PCS) | `PCS` | ₹61.50 | 12 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 12 (0.0% div; non-d... |
| `04060` | 1103- TIGER COLOUR SOM (12 PCS | `PCS` | ₹67.50 | 12 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2, 10] contradicts suggested ... |
| `04063` | 1106- SPIDER COLOUR SOM  ( 3 P | `PCS` | ₹97.00 | 3 | 1 | 2 | 2 | 50.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2] contradicts suggested pack... |
| `04064` | 1107- CAMANDO BLACK SOM ( 3 PC | `PCS` | ₹102.00 | 3 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2, 2] contradicts suggested p... |
| `04065` | 1108- CAMANDO COLOUR SOM ( 3 P | `PCS` | ₹109.00 | 3 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [2, 2] contradicts suggested p... |
| `04194` | 117- GEM MEGA ( 10 PKT ) 3 COL | `PKT` | ₹145.00 | 10 | 1 | 6 | 6 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04207` | 189- 7 CM COL GOLD S.T.D(10DAB | `BOX` | ₹150.00 | 10 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [3] contradicts suggested pack... |
| `04236` | 213- 12 CM 5 IN 1 (5 PKT) CHAN | `PKT` | ₹120.00 | 5 | 1 | 6 | 6 | 66.7% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04313` | 171- GOLD BIJALI GIANT OVEEYA( | `BAG` | ₹44.00 | 100 | 1 | 2 | 2 | 50.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [30] contradicts suggested pac... |
| `04314` | 172- GOLD BIJALI APPLE(100 PCS | `BAG` | ₹27.00 | 100 | 1 | 2 | 2 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [120, 30] contradicts suggeste... |
| `04423` | 395- 4 SUP DLX GOLD KARUDA (10 | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 50.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [25] contradicts suggested pac... |
| `04508` | 500- FLOWER POTS DLX (10 P) OV | `PKT` | ₹150.00 | 10 | 1 | 6 | 6 | 33.3% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (33.3% div; non-... |
| `04509` | 501- FLOWER POTS DLX (10 P) GO | `PKT` | ₹245.00 | 10 | 1 | 7 | 7 | 28.6% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (28.6% div; non-... |
| `04511` | 503- FLOWER POTS DLX COL KOTI( | `PKT` | ₹350.00 | 10 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04512` | 504- FLOWER POTS DLX COL KOTI  | `PKT` | ₹355.00 | 10 | 1 | 3 | 3 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04513` | 505- FLOWER POTS MEGA DLX (10  | `PKT` | ₹290.00 | 10 | 1 | 6 | 6 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04514` | 506- F P MEGA DLX  (10 P) VIRA | `PKT` | ₹420.00 | 10 | 1 | 15 | 15 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04518` | 510- FLOWER POT DLX (5 PCS )GO | `PKT` | ₹120.00 | 5 | 1 | 16 | 16 | 87.5% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (87.5% div; non-d... |
| `04519` | 511- FLOWER POT DLX (5 PCS )ME | `PKT` | ₹175.00 | 5 | 1 | 3 | 3 | 66.7% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (66.7% div; non-d... |
| `04520` | 512- FLOWER POT DLX (5 PCS )S. | `PKT` | ₹240.00 | 5 | 1 | 8 | 8 | 12.5% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (12.5% div; non-d... |
| `04574` | 615- G C SPL (10 P) (5 P) S.T. | `PKT` | ₹150.00 | 10 | 1 | 2 | 2 | 50.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5] contradicts suggested pack... |
| `04576` | 617- G C SPL SPINNER WHEEL(10P | `PKT` | ₹75.00 | 10 | 1 | 17 | 17 | 82.4% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (82.4% div; non-... |
| `04601` | 642- G C SUP DLX  (10 P) 5 P S | `PKT` | ₹215.00 | 5 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [4] contradicts suggested pack... |
| `04615` | 652- MASKA CHASKA I. N ( 5 P ) | `PKT` | ₹120.00 | 5 | 1 | 5 | 5 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (80.0% div; non-d... |
| `04618` | 655- MUSICAL WHEEL MERCURY (5  | `PKT` | ₹102.50 | 5 | 1 | 10 | 10 | 50.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `04626` | 663- SPINNER BAMBARA LAVANYA ( | `PKT` | ₹85.00 | 10 | 1 | 5 | 5 | 20.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (20.0% div; non-... |
| `04627` | 664- LOTUS WHEEL (5 PCS) AYYAN | `PKT` | ₹120.00 | 5 | 1 | 4 | 4 | 75.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `04628` | 665- STAR WHEEL (10 PCS) AYYAN | `PKT` | ₹156.00 | 10 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5] contradicts suggested pack... |
| `04685` | 730- WHISTLING PIPER SONY ( 5  | `PKT` | ₹285.00 | 5 | 1 | 6 | 6 | 50.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (50.0% div; non-d... |
| `04687` | 732- HAND SHOWER MARIESWARAN ( | `PKT` | ₹185.00 | 3 | 1 | 7 | 7 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04914` | 1012- 5 KA DHUM ( 5 P) ANIL | `BOX` | ₹155.00 | 5 | 1 | 4 | 4 | 75.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 5 (75.0% div; non-d... |
| `04918` | 1016- TOP-TEN ( 10 P ) COCK | `BOX` | ₹350.00 | 10 | 1 | 5 | 5 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 10 (0.0% div; non-d... |
| `04924` | 1022- 2 1/2 F. P. (3P)6COL MIX | `BOX` | ₹175.00 | 3 | 1 | 9 | 9 | 44.4% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (44.4% div; non-d... |
| `04925` | 1023- 2 1/2 F. P. (3P)6COL MIX | `BOX` | ₹180.00 | 3 | 1 | 10 | 10 | 40.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (40.0% div; non-d... |
| `04927` | 1025- 2 1/2 F. P. (3PCS) MIX C | `BOX` | ₹225.00 | 3 | 1 | 9 | 9 | 44.4% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (44.4% div; non-d... |
| `04929` | 1027- 2 1/2 F. P. (3P)MIX COL  | `BOX` | ₹500.00 | 3 | 1 | 3 | 3 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04930` | 1028- 2 1/2 F. P. (3P)3 IN 1 B | `BOX` | ₹422.00 | 3 | 1 | 4 | 4 | 0.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04931` | 1029- PARACHUTE NIGHTOUT ( 3 P | `BOX` | ₹400.00 | 3 | 1 | 7 | 7 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04932` | 1030- 2 1/2 F. P.LONG(3P)MIX C | `BOX` | ₹455.00 | 3 | 1 | 6 | 6 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `04941` | 1039- 3  FANCY PIPE (2P) MIX C | `BOX` | ₹600.00 | 2 | 1 | 4 | 4 | 50.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 2 (50.0% div; non-d... |
| `04942` | 1040- 3  FANCY PIPE (3P) MIX C | `BOX` | ₹940.00 | 3 | 1 | 7 | 7 | 0.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (0.0% div; non-di... |
| `05404` | 515- FLOWER POTS RANG BARAAT ( | `PKT` | ₹405.00 | 2 | 1 | 5 | 5 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `05460` | 1052- 4"  F. P.(2P) 8 COL MIX  | `BOX` | ₹1100.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `05950` | W COL SMOKE DHUA  COL (5 P) SU | `BOX` | ₹120.00 | 5 | 1 | 7 | 6 | 42.9% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 5 (42.9% div; non-d... |
| `06049` | W 1 1/4 POGO MIXED ( 10 P) 2 P | `BOX` | ₹58.00 | 10 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06054` | W 2 1/2 F PIPE  BALAJI ( 3 P) | `BOX` | ₹175.00 | 3 | 1 | 5 | 3 | 20.0% | `RECOMMEND_REJECT` | **1** | MEDIUM | Wholesale dispatches contradict multiple 3 (20.0% div; non-d... |
| `06058` | W 3 F PIPE BIG SIZZ MIXD ( 2P  | `BOX` | ₹580.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06072` | W 4 F P 3 COL MIXED ( 2 P) W M | `BOX` | ₹850.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06074` | W 4 F P DLX 15 COL MIXED ( 2 P | `BOX` | ₹900.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [1] contradicts suggested pack... |
| `06098` | W 2 1/2" F. PIPE 2 IN 1 ( 2 P  | `BOX` | ₹200.00 | 2 | 1 | 1 | 1 | 0.0% | `RECOMMEND_REJECT` | **1** | LOW | Non-divisible wholesale order [5] contradicts suggested pack... |
| `06099` | W 18 SHOT ROMANCANDLE ( 2P) | `BOX` | ₹400.00 | 2 | 1 | 5 | 5 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 2 (80.0% div; non-d... |
| `06156` | W 2 1/2 F PIPE  MIX BIG  ( 3 P | `BOX` | ₹375.00 | 3 | 1 | 5 | 5 | 80.0% | `RECOMMEND_REJECT` | **1** | HIGH | Wholesale dispatches contradict multiple 3 (80.0% div; non-d... |

### Category 4: INSUFFICIENT_HISTORY (158 Products)
*Products with zero or low transaction volume in D2627; safe default 1 retained.*

| Code | Product Name | UOM | Rate (₹) | Sug | Enf | WS Lines | Custs | Div % | Rec Action | Rec Mult | Conf | Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00120` | 195- 10 CM SILVER DROPS SARAVA | `PKT` | ₹15.50 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00144` | 276- 10 CM PLAIN ASOK ( 5 P) | `PKT` | ₹20.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00145` | 277- 10 CM COL ASOK ( 5 P) | `PKT` | ₹23.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00147` | 278- 10 CM GREEN ASOK ( 5 P) | `PKT` | ₹28.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00148` | 279- 10 CM RED ASOK ( 5 P) | `PKT` | ₹30.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00149` | 280- 10 CM 4 COLOUR ASOK ( 5 P | `PKT` | ₹28.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00180` | 149- MINI RED BIJALI CAT BRAND | `BAG` | ₹58.00 | 10 | 10 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `00182` | 151- RED BIJALI GANESH(100 PCS | `BAG` | ₹41.00 | 10 | 10 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `00185` | 154- RED BIJALI VIMAL(100 P)10 | `BAG` | ₹65.00 | 10 | 10 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **10** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `00187` | 291- 10 GAINT JAWAN GEMS (100P | `BUNDLE` | ₹360.00 | 1 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 lines, 2 customer). Retain approved m... |
| `00251` | 309- 20 DLX BALAJI( 10 P) | `PKT` | ₹37.50 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00254` | 312- 24 DLX COCK (10P) | `BOX` | ₹63.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00294` | 334- 2 3/4 KURVI AYYANAR (25 P | `PKT` | ₹9.50 | 25 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00368` | 413- 2 LXM DHAMAKA GENIUS (25  | `PKT` | ₹5.50 | 25 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00370` | 415- 3 1/2 LXM DHAMAKA AYYANAR | `PKT` | ₹13.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00371` | 416- 3 1/2 LXM DHAMAKA I.N(10  | `PKT` | ₹14.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00372` | 417- 3 1/2 LXM DHAMAKA AMBIKA( | `PKT` | ₹15.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00374` | 419- 3 1/2 LXM DHAMAKA S.T.D ( | `PKT` | ₹24.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00381` | 426- 4' LXM DHAMAKA I.N ( 10 P | `PKT` | ₹18.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00382` | 427- 4' LXM DHAMAKA AYYANAR (  | `PKT` | ₹21.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00383` | 428- 4' LXM DHAMAKA AYYAN ( 10 | `PKT` | ₹32.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00387` | 432- 4' DLX LXM DHAMAKA I.N (  | `PKT` | ₹23.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00388` | 433- 4' DLX BAJ DHAMAKA T/MEEN | `PKT` | ₹30.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00389` | 434- 4' DLX LXM DHAMAKA T/MEEN | `PKT` | ₹32.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00391` | 436- 4' DLX LXM DHAMAKA AYYANA | `PKT` | ₹35.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00395` | 439- 4 DLX GOLD LXM T/MEENA (  | `PKT` | ₹30.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00396` | 440- 4 DLX GOLD LXM AYYANAR( 1 | `PKT` | ₹35.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00429` | 445- FLOWER POTS SMALL ARUDHAR | `PKT` | ₹50.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00430` | 446- FLOWER POTS SMALL MURCURY | `PKT` | ₹64.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00442` | 521- TRI COL FOUNTAIN S.T.D (5 | `PKT` | ₹375.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00449` | 528- HAPPINESS F. POT 5 IN 1 S | `PKT` | ₹265.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00463` | 575- MAGIC WHIP S.T.D( 2 P) | `PKT` | ₹89.00 | 2 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00492` | 551- MINI PEARL GUDIYA ( 5 PCS | `BOX` | ₹135.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00504` | 561- ASHARFI  GOLDEN STAR OTHE | `BOX` | ₹240.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00505` | 562- MUTT PUTT ANAR MERCURY (  | `BOX` | ₹200.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00533` | 588- G C BIG T/MEENA( 10 P)(10 | `PKT` | ₹30.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00534` | 589- G C BIG GANESH ( 10 P)(10 | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00543` | 646- DISCO WHEEL S.M.K.(10 PCS | `PKT` | ₹85.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00564` | 707- 18 T STAR D/VADIVEL(10P)  | `PKT` | ₹15.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00566` | 709- 18 T STAR T/MEENA (10P) 1 | `PKT` | ₹20.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00568` | 711- 120 T STAR S.T.D (10P) 5  | `PKT` | ₹155.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00619` | 740- SUPER BULLET BOMB AYYANAR | `PKT` | ₹25.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00620` | 741- BULLET BOMB GANESH ( 10 P | `PKT` | ₹27.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00622` | 743- SUPER BULLET BOMB ( 10 P  | `PKT` | ₹39.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `00631` | 752- JHANSI BOMB GREEN W/F(10P | `PKT` | ₹80.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00688` | 598- G C ASOKA T/MEENA (10 P) | `PKT` | ₹40.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00758` | 599- G C ASOKA AYYANAR(10 P) | `PKT` | ₹50.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `00761` | 649- SUN FLOWER WHEEL I. N (10 | `PKT` | ₹255.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `00866` | 158- STRIPPED BIJALI ROSE(50 P | `BAG` | ₹11.50 | 50 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02042` | 281- 12 CM PLAIN ASOK ( 2 P) | `PKT` | ₹35.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02155` | 1120- RING CAPS (1OOPKT= 1 BOX | `PKT` | ₹7.00 | 100 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02275` | 282- 12 CM COLOUR ASOK ( 2 P) | `PKT` | ₹40.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02667` | 284- 30 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02668` | 285- 30 CM COL ASOK ( 2 P) | `PKT` | ₹70.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02671` | 569- DANCING BUTTERFLY AYYAN ( | `PKT` | ₹125.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02672` | 670- PYRO DANCE BUTTERFLY SUNS | `PKT` | ₹140.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02673` | 571- COL CHAN. BUTTERFLY S.T.D | `PKT` | ₹132.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02677` | 668- RAINBOW ROCKET S.T.D (10P | `PKT` | ₹130.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02679` | 670- ROCKET BOMB (10P) 5P N.M. | `PKT` | ₹45.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02710` | 197- 30 CM GREEN SARAVANA (2 P | `PKT` | ₹25.00 | 2 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `02711` | 198- 30 CM RED SARAVANA (2 P) | `PKT` | ₹27.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `02841` | 233- 12 CM 4 IN 1 LX CLASSIC ( | `PKT` | ₹22.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `02885` | 580- SKY SCRAPPER DRONE MERCUR | `PCS` | ₹125.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `02905` | W 1000 LAR (600 COUNTING) S.K. | `PKT` | ₹180.00 | 1 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 lines, 2 customer). Retain approved m... |
| `03092` | 186- 7 CM RED M.R.P. (10 DABBI | `BOX` | ₹120.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03094` | 188- 7 CM PLAIN GOLD S.T.D(10D | `BOX` | ₹180.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03102` | 240- 15 CM COL BOXE(2P CELLEPH | `PKT` | ₹29.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03111` | 249- 30 CM PLAIN DLX CLASSIC ( | `PKT` | ₹25.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03112` | 250- 30 CM PLAIN BOXE(2P CELLE | `PKT` | ₹26.00 | 2 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `03179` | 585- HELICOPTER ANIL( 5PCS) | `PKT` | ₹100.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03180` | 586- HELICOPTER SUNSHINE( 10 P | `PKT` | ₹290.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03212` | 612- G C SPL W (10 P) I.N | `PKT` | ₹90.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03213` | 613- G C SPL (10 P) (5 P) SUNS | `PKT` | ₹94.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03218` | 698- WHISTLING ROCKET MERCURY( | `PKT` | ₹200.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03219` | 699- WHISTLING ROCKET ANIL(10P | `PKT` | ₹227.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03220` | 700- SILVER JET ROCKET S.T.D ( | `PKT` | ₹225.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03221` | 701- ROHINI ROCKET S.T.D (10 P | `PKT` | ₹227.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `03226` | 706- PARACHUTE ROCKET S.T.D (  | `PKT` | ₹575.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03229` | 719- 7 CM PENCIL VIRBALAJI ( 1 | `PKT` | ₹20.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03230` | 720- 7 CM PENCIL T/MEENA ( 10  | `PKT` | ₹24.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `03232` | 722- 10 CM PENCIL T/MEENA ( 10 | `PKT` | ₹45.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `03233` | 723- 12 CM PENCIL VIRBALAJI (  | `PKT` | ₹43.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `03267` | 755- LALKAR BOMB FOIL W/F(10 P | `PKT` | ₹90.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04006` | 842- 7 SHOTS J.K (5 PCS) (5P) | `BOX` | ₹80.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04012` | 848- 7 SHOTS OTHER (10 PCS) | `BOX` | ₹180.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04016` | 852- 7 SHOTS SIGNAL ROCKET COC | `BOX` | ₹500.00 | 15 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04045` | 1088- YOGESH BLACK GUN REX ( 1 | `PKT` | ₹7.00 | 12 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04046` | 1089- TOM COLOUR YUG ( 12 PCS  | `PCS` | ₹7.50 | 12 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04047` | 1090- V-30 COLOUR VISHNU (12 P | `PCS` | ₹12.10 | 12 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04049` | 1092- V-301 COLOUR VISHNU ( 10 | `PCS` | ₹12.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04192` | 115- R & G MATCH BOX RAYAL(600 | `BUNDLE` | ₹500.00 | 1 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `04195` | 118- WONDER CRACKLING ( 10 PCS | `PKT` | ₹210.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04239` | 216- 15 CM  50 X 50 (5 PCS)CHA | `PKT` | ₹35.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04248` | 253- 30 CM COL BOXE(2P CELLEPH | `PKT` | ₹29.00 | 2 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04254` | 259- 30 CM 2 IN 1 BOXE(2P CELL | `PKT` | ₹29.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04302` | 160- STRIPPED BIJALI ROSE(100P | `BAG` | ₹21.50 | 10 | 10 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **10** | LOW | Low volume in D2627 (2 lines, 2 customer). Retain approved m... |
| `04306` | 164- STRIPPED BIJALI S.T.D(100 | `BAG` | ₹60.00 | 10 | 10 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **10** | LOW | Low volume in D2627 (1 lines, 1 customer). Retain approved m... |
| `04310` | 168- GOLD BIJALI COCK (50 PCS) | `BAG` | ₹35.50 | 50 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04342` | 297- 28 CHORSA (25PCS) VELVAN | `PKT` | ₹14.50 | 25 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04343` | 298- 32 CHORSA MIX RED-GOA SUN | `PKT` | ₹12.50 | 50 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04347` | 302- 28 GAINT CHORSA (25 P) AJ | `PKT` | ₹18.50 | 25 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04349` | 304- 28 GAINT CHORSA (25 P)DUR | `PKT` | ₹19.50 | 25 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04350` | 305- 28 SUP GAINT CHORSA N.M.J | `PKT` | ₹24.00 | 25 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04352` | 317- 50 DLX GANESH DURAI( 5 P) | `PKT` | ₹80.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04371` | 343- 3 1/2  PEACOCK 9 CM  S.T. | `PKT` | ₹24.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04372` | 344- 3 1/2 DLX KURVI GANESH (1 | `PKT` | ₹25.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04373` | 345- 3 1/2 GREEN PARROT W/F B. | `PKT` | ₹25.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04374` | 346- 3 1/2 JAWAN AYYAN (10 P) | `PKT` | ₹27.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04377` | 349- 4  MIX LABEL DURGESH (10  | `PKT` | ₹14.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04379` | 351- 4 GREEN PARROT SRIPATHI ( | `PKT` | ₹16.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04380` | 352- 4  LADY T/MEENA  (10 P) | `PKT` | ₹16.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04387` | 359- 4 GREEN PARROT W/F V.F.I( | `PKT` | ₹32.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04388` | 360- 4 KING AYYAN (10 P) | `PKT` | ₹32.50 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04389` | 361- 10 CM PEACOCK COLF S.T.D( | `PKT` | ₹34.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04390` | 362- 4 GREEN PARROT W/F B.F.W  | `PKT` | ₹35.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04413` | 385- 5 DLX  ELEPHANT(10P) JAYM | `PKT` | ₹31.00 | 10 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04424` | 396- 4 SUP DLX GOLD ELEPHANT ( | `PKT` | ₹57.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04428` | 403- 2 SOUND DHAMAKA ANIL (10P | `PKT` | ₹32.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04429` | 404- 2 SOUND DHAMAKA S.T.D (10 | `PKT` | ₹36.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04430` | 405- 2 SOUND DHAMAKA MERCURY ( | `PKT` | ₹42.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04433` | 408- 3 SOUND DHAMAKA NM JYOTHI | `PKT` | ₹28.50 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04435` | 410- 3 SOUND DHAMAKA I.N. (10P | `PKT` | ₹40.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04510` | 502- FLOWER POTS COL KOTI DLX( | `PKT` | ₹375.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04563` | 563- OMG POTS ANAR MERCURY ( 5 | `BOX` | ₹315.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04564` | 564- CROWN JEWEL'S ANAR MERCUR | `BOX` | ₹625.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04580` | 621- G C DLX  (10 P) 5 P VENKA | `PKT` | ₹75.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04587` | 628- G C DLX  (10 P) 5 P ANIL | `PKT` | ₹160.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04588` | 629- G C DLX  (10 P) 5 P SUNSH | `PKT` | ₹165.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04593` | 634- G C DLX  PLASTIC (10 P) 5 | `PKT` | ₹110.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04600` | 641- G C SUP DLX  (10 P) 5 P M | `PKT` | ₹190.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04620` | 657- WHIZZ WHEEL S.T.D (5 PCS) | `PKT` | ₹139.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04622` | 659- TOP TUCKER AYYAN ( 5 P) | `PKT` | ₹80.00 | 5 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `04634` | 673- ROCKET BOMB (10P) 5P S.T. | `PKT` | ₹144.00 | 5 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04640` | 679- EXPO ROCKET (10 P) 2P GAN | `PKT` | ₹85.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04643` | 682- LUNIK ROCKET (10 P) 2P AY | `PKT` | ₹130.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `04650` | 689- 2 SOUND ROCKET (10 P) 2P  | `PKT` | ₹132.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04926` | 1024- 2 1/2 F. P. (2P)6COL MIX | `BOX` | ₹190.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `04928` | 1026- 3 FANCY PIPE (2 PCS) SON | `BOX` | ₹850.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05004` | 1115- PUBG GUN ( 5 P X 1 PKT ) | `BOX` | ₹90.00 | 5 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `05020` | 1133- COLD PYRO BLACK R.R.R (  | `BOX` | ₹110.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05021` | 1134- COLD PYRO YELLO BOX TAIW | `BOX` | ₹120.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05023` | 1136- NAAGARA FALLS ( 25 PCS)  | `BOX` | ₹1200.00 | 25 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05427` | 693- 3 SOUND ROCKET (10 P) 2P  | `PKT` | ₹135.00 | 2 | 1 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 2 customer(s)). Insufficient... |
| `05459` | 1051- 4"  F. P.(2P) 3 COL. MIX | `BOX` | ₹860.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05461` | 1053- 4"  DLX F.P.(2P) 12 COL. | `BOX` | ₹950.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05462` | 1054- 4"  F.P.(2P)DOUBLE BALL  | `BOX` | ₹1230.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `05933` | W 1000 LAR (800 COUNTING) S.K. | `BOX` | ₹200.00 | 1 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `05953` | W 4 F. PIPE (2 PCS)  I. N. | `BOX` | ₹900.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06048` | W TOP- TEN ( 10 P ) COCK | `BOX` | ₹285.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06053` | W 2 1/2 F PIPE MIX UV BOX ( 3  | `BOX` | ₹165.00 | 3 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |
| `06056` | W 2 1/2 F PIPE MEGAL ( 3 P ) M | `BOX` | ₹445.00 | 3 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06057` | W 3 F PIPE LIGHT AND HOT MIX ( | `BOX` | ₹685.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06068` | W 3 1/2 F P DOUBLE BALL (2 P)  | `BOX` | ₹750.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06073` | W 4 F P 3 COL MIXED ( 2 P) W   | `BOX` | ₹900.00 | 2 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06092` | W 7 SHOT ( 10 P ) MERCURY | `BOX` | ₹210.00 | 10 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Maintain safe unconstraine... |
| `06106` | W 5000 LAR (600) COUNTING SANT | `BOX` | ₹950.00 | 1 | 1 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **1** | NONE | Zero sales transactions in D2627. Retain currently approved ... |
| `06157` | W COLD PYRO BOX 3.M.35.S (6P) | `BOX` | ₹100.00 | 6 | 1 | 2 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (2 line(s), 1 customer(s)). Insufficient... |
| `06175` | 133- KIT-KAT BIG(10 P)TIRUMINI | `PKT` | ₹32.00 | 10 | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **1** | LOW | Low volume in D2627 (1 line(s), 1 customer(s)). Insufficient... |

---

## 9. Recommended Implementation & Cloned-Dataset Dry Run Protocol

To transition these empirical findings into production safely without operational disruption:

1. **Business Owner Review via Worksheet**:  
   - The business owner reviews [`PACKAGING_BUSINESS_REVIEW_WORKSHEET.md`](./PACKAGING_BUSINESS_REVIEW_WORKSHEET.md).
   - Check `[x] Approve` or `[x] Change: ___` or `[x] Reject` for candidate items.

2. **Controlled Overlay JSON Update**:  
   - Only rules explicitly signed off by the business owner are added to `sync-service/app/data/catalog_pack_rules.json` with `status: 'APPROVED'`.
   - Heuristic rules remain `UNVERIFIED_HEURISTIC` (enforced multiple `1`).

3. **Safe Dry-Run Verification on Cloned Dataset**:  
   - Clone `legacy-software-extracted/FAVWIN/D2627` to a temporary sandbox directory.
   - Run the order validation suite across all historical orders using the updated rules.
   - Confirm that zero historical wholesale orders are falsely rejected.
