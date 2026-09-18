# PYROJA Active Packaging Rules Risk Register & Pilot Safety Audit

**Document Version:** 1.0.0  
**Date Generated:** September 19, 2026  
**Scope:** Detailed audit of all 32 currently approved rules in `sync-service/app/data/catalog_pack_rules.json`  
**Audit Fiscal Year:** `legacy-software-extracted/FAVWIN/D2627` (April 5, 2026 to August 29, 2026)  

---

## 1. Executive Summary: Active Rule Pilot Safety

Before initiating showroom tablet pilots or live FoxPro order synchronization, all 32 active packaging overlay rules were independently audited against historical wholesale order dispatches:

| Safe Pilot Status | Count | % of Active Rules | Empirical Qualification | Operational Directive |
| :--- | :---: | :---: | :--- | :--- |
| **`SAFE_FOR_PILOT`** | **21** | **65.6%** | 100.0% historical compliance across $\ge 2$ customers and $\ge 3$ lines | Approved for live enforcement in pilot showroom |
| **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | **11** | **34.4%** | Rule requires change (1 item) or lacks multi-customer history (10 items) | **Do not enforce above 1 in pilot** until business owner sign-off |
| **Total Active Overlay Rules** | **32** | **100.0%** | Complete overlay rule registry | Clear risk-gated separation |

---

## 2. 'Do Not Use in Pilot Until Signed Off' List (11 Rules)

> [!CAUTION]
> **Operational Constraint:** The 11 rules below MUST NOT enforce multiples on wholesale tablet orders during pilot testing without explicit sign-off.
> - **Rule `04042` (`DHAGA (80 DABBI)`)**: Currently enforces `1`, but wholesale orders are strictly multiples of `80` packets. Enforcing 1 allows loose single-packet orders (₹6.00) that contradict business dispatch practice.
> - **Zero-Transaction Rules (6 items)**: No sales recorded in D2627; cannot be empirically validated.
> - **Low-Volume Rules (4 items)**: Only 1 or 2 lines recorded; cannot establish multi-customer policy.

| Code | Product Name | Brand | UOM | Current Enforced | Hist WS Lines | Custs | Invs | Div % | Historical Recommendation | Safe Pilot Status | Risk & Mitigation Directive |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00180` | 149- MINI RED BIJALI CAT BRAND | RED , STRIPPED, GO | `BAG` | **10** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 10 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |
| `00182` | 151- RED BIJALI GANESH(100 PCS | RED , STRIPPED, GO | `BAG` | **10** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 10 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |
| `00185` | 154- RED BIJALI VIMAL(100 P)10 | RED , STRIPPED, GO | `BAG` | **10** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 10 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |
| `00187` | 291- 10 GAINT JAWAN GEMS (100P | 10 CHORSA | `BUNDLE` | **1** | 2 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Low volume in D2627 (2 lines, 2 customer). All orders divisible by 1, but multi-customer corroboration insufficient. Evidence: GCD=1, Plausible Divisors=[]. Retain approved multiple 1; observe during seasonal peak. |
| `02905` | W 1000 LAR (600 COUNTING) S.K. | OFF SEASON LIST 20 | `PKT` | **1** | 2 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Low volume in D2627 (2 lines, 2 customer). All orders divisible by 1, but multi-customer corroboration insufficient. Evidence: GCD=1, Plausible Divisors=[]. Retain approved multiple 1; observe during seasonal peak. |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | POP - POP | `PKT` | **1** | 6 | 6 | 6 | 100.0% | `RECOMMEND_CHANGE` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Current overlay enforces 1 (assuming bundle billing), but billing UOM is PKT and 100% of wholesale orders across 6 customers are in multiples of 80 packets (₹480/bundle). Evidence: GCD=80, Plausible Divisors=[2, 4, 5, 8, 10, 16, 20, 40, 80]. Unambiguous packaging unit from description and sales; change multiple to 80. |
| `04192` | 115- R & G MATCH BOX RAYAL(600 | MATCH BOX | `BUNDLE` | **1** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 1 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |
| `04302` | 160- STRIPPED BIJALI ROSE(100P | RED , STRIPPED, GO | `BAG` | **10** | 2 | 2 | 2 | 100.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Low volume in D2627 (2 lines, 2 customer). All orders divisible by 10, but multi-customer corroboration insufficient. Evidence: GCD=50, Plausible Divisors=[2, 5, 10, 25, 50]. Retain approved multiple 10; observe during seasonal peak. |
| `04306` | 164- STRIPPED BIJALI S.T.D(100 | RED , STRIPPED, GO | `BAG` | **10** | 1 | 1 | 1 | 100.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Low volume in D2627 (1 lines, 1 customer). All orders divisible by 10, but multi-customer corroboration insufficient. Evidence: GCD=50, Plausible Divisors=[2, 5, 10, 25, 50]. Retain approved multiple 10; observe during seasonal peak. |
| `05933` | W 1000 LAR (800 COUNTING) S.K. | OFF SEASON LIST 20 | `BOX` | **1** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 1 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |
| `06106` | W 5000 LAR (600) COUNTING SANT | OFF SEASON LIST 20 | `BOX` | **1** | 0 | 0 | 0 | 0.0% | `INSUFFICIENT_HISTORY` | **`DO_NOT_USE_IN_PILOT_UNTIL_SIGNED_OFF`** | Zero eligible sales transactions in D2627. Retain currently approved multiple 1 based on catalog specification; observe during seasonal peak. (Evidence: GCD=N/A, Plausible Divisors=[]). |

---

## 3. 'Safe for Pilot' List (21 Rules)

These 21 overlay rules are **empirically validated** with 100.0% compliance across $\ge 2$ wholesale customers and $\ge 3$ lines in D2627:

| Code | Product Name | Brand | UOM | Current Enforced | Hist WS Lines | Custs | Invs | Qty Distribution | Div % | GCD | Plausible Divisors | Historical Recommendation | Safe Pilot Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| `00079` | 119- ASST CARTOON(10 PCS)DURGE | ASST CARTOON & RAI | `PKT` | **1** | 3 | 3 | 3 | `4(2)|20(1)` | 100.0% | 4 | `[2, 4]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00082` | 124- BIG NAGGOLI PANDYAN BLACK | SERPANTS & NAGGOLI | `BUNDLE` | **1** | 15 | 15 | 15 | `1(2)|2(5)|3(3)|5(4)|8(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00083` | 125- BIG NAGGOLI PANDYAN RED(1 | SERPANTS & NAGGOLI | `BUNDLE` | **1** | 6 | 6 | 6 | `2(1)|3(2)|300(1)|420(1)|600(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00178` | 148- RED BIJALI ROSE (100 PCS | RED , STRIPPED, GO | `BAG` | **10** | 10 | 10 | 10 | `10(1)|40(2)|50(2)|100(4)|350(1)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00181` | 150- RED BIJALI AYYANAR (100 P | RED , STRIPPED, GO | `BAG` | **10** | 7 | 7 | 7 | `10(1)|20(1)|50(3)|100(1)|200(1)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00183` | 152- RED BIJALI S.T.D.(100 PCS | RED , STRIPPED, GO | `BAG` | **10** | 12 | 12 | 12 | `20(6)|40(3)|50(2)|60(1)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00184` | 153- RED BIJALI SONY (100 PCS) | RED , STRIPPED, GO | `BAG` | **10** | 3 | 3 | 3 | `10(1)|30(1)|50(1)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00186` | 290- 10 CHORASA MUNNA DURGESH( | 10 CHORSA | `BUNDLE` | **1** | 7 | 7 | 7 | `1(2)|2(2)|3(1)|4(1)|5(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00223` | 293- 16 CHORSA B GROUP (50P= 1 | 28 -CHORSA & 28-GA | `PKT` | **50** | 9 | 9 | 9 | `50(1)|100(5)|150(1)|200(2)` | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00224` | 294- 28 CHORSA K.R.K (50P= 1 B | 28 -CHORSA & 28-GA | `PKT` | **50** | 15 | 15 | 15 | `50(4)|100(2)|150(1)|200(5)|250(2)|300(1)` | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00225` | 295- 28 CHORSA TAJ  T/MEENA (5 | 28 -CHORSA & 28-GA | `PKT` | **50** | 3 | 3 | 3 | `50(2)|100(1)` | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00455` | 534- JADUGAR UV.BOX AYYAN (4 P | FANCY FLOWER POTS  | `PKT` | **1** | 9 | 9 | 9 | `1(4)|2(2)|3(2)|5(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `00456` | 535- MANORANJAN U.V.BOX AYYAN( | FANCY FLOWER POTS  | `PKT` | **1** | 7 | 7 | 7 | `1(3)|2(3)|3(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `02157` | 1121- MISSILE SIREN(127X1)TITA | RING CAPS AND MISS | `PKT` | **1** | 13 | 13 | 13 | `2(1)|3(1)|5(5)|10(3)|20(3)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `03088` | 114- R & G MATCH BOX SHANTHI(6 | MATCH BOX | `BUNDLE` | **1** | 7 | 7 | 7 | `1(6)|2(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04301` | 159- STRIPPED BIJALI MERCURY(5 | RED , STRIPPED, GO | `BAG` | **10** | 5 | 5 | 5 | `50(3)|100(2)` | 100.0% | 50 | `[2, 5, 10, 25, 50]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04303` | 161- STRIPPED BIJALI AYYANAR(1 | RED , STRIPPED, GO | `BAG` | **10** | 7 | 7 | 7 | `20(1)|30(1)|50(2)|60(1)|100(2)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04305` | 163- STRIPPED BIJALI GAINT S.T | RED , STRIPPED, GO | `BAG` | **10** | 3 | 3 | 3 | `10(1)|20(1)|50(1)` | 100.0% | 10 | `[2, 5, 10]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04613` | 650- SUDARSHAN CHAKKAR ANIL (  | FANCY - CHAKKAR /  | `PKT` | **1** | 4 | 4 | 4 | `2(1)|5(2)|10(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04616` | 653- GIANT WHEEL AYYAN (5 PCS) | FANCY - CHAKKAR /  | `PKT` | **1** | 4 | 4 | 4 | `1(1)|2(1)|5(2)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |
| `04625` | 662- SKY  WHEEL AYYAN (5 PCS)  | FANCY - CHAKKAR /  | `PKT` | **1** | 3 | 3 | 3 | `1(2)|3(1)` | 100.0% | 1 | `[]` | `RECOMMEND_APPROVE` | **`SAFE_FOR_PILOT`** |

---

## 4. Pilot Governance Recommendation

1. **Pilot Configuration Policy**:  
   - For the 21 `SAFE_FOR_PILOT` rules, maintain active enforcement (`status: 'APPROVED'`, `enabled: true`).
   - For `04042`, update pack multiple to `80` upon business-owner approval.
   - For the remaining 10 rules with insufficient history, either retain as catalog specifications with explicit business sign-off or temporarily set `status: 'PENDING_REVIEW'` (enforcing `1`) to avoid unverified blocking during pilot.
