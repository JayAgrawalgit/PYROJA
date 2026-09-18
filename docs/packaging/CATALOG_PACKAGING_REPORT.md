# PYROJA Hardened Catalog Packaging Rules & Resolution Report

**Date Generated:** September 19, 2026  
**Active Fiscal Year:** D2627  
**Catalog Scope:** All Active Commercial Products (n = 1093)  
**FoxPro DBF Integrity:** 100% Read-Only (Zero modifications to legacy databases)  

---

## 1. Executive Summary

In FoxPro `ITEMMST.DBF`, the `QIB` (Quantity In Box) field is `1` across all 3,019 products and `PACK` represents the FoxPro billed unit of measure (e.g., `PKT`, `BOX`, `BUNDLE`), rather than the wholesale case pack multiple. Enforcing quantity restrictions directly from legacy data would either block wholesale orders or allow incorrect loose sales.

To ensure wholesale orders are never blocked or distorted by unverified heuristic parsing, the PYROJA system strictly enforces a **Separation of Concerns Architecture**:

1. **`suggested_pack_multiple` (Guarded Heuristics & Recommendations)**:  
   - Derived from guarded regex parsing of product descriptions.
   - Used exclusively for **Tablet POS user guidance** (pre-filling quick-add buttons and pack increments).
   - **NEVER used to reject wholesale orders.**

2. **`enforced_pack_multiple` (Business-Approved Wholesale Enforcement)**:  
   - Used by the server for wholesale order validation (`qty % enforced_pack_multiple == 0`).
   - **Guaranteed to be `1` unless an explicit, enabled rule with `status = APPROVED` exists in `catalog_pack_rules.json`.**
   - Completely eliminates the risk of heuristic false positives causing `422 Unprocessable Entity` rejections in the field.

3. **Retail Walk-In Cash Account (`99999`) Rule**:  
   - Cash customer `99999` (and any account in the `RETAIL` tier) completely bypasses wholesale multiple checks and can purchase single loose units (>= 1).

---

## 2. Catalog Statistics & Source Distribution

| Metric | Value | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **Total Active Commercial Products** | **1093** | **100.0%** | Products with non-empty name and active rate/stock |
| Tier 1: Explicit Approved Overrides | 32 | 2.9% | Explicit rules in `catalog_pack_rules.json` with `status: APPROVED` |
| Tier 2: Guarded Heuristic Suggestions | 840 | 76.9% | Suggested pack multiples derived from guarded regex (enforced = 1) |
| Tier 3: Safe Fallback (`1`) | 221 | 20.2% | Products with no pattern detected (suggested = 1, enforced = 1) |

### Enforced vs. Suggested Pack Multiples Breakdown

| Pack Multiple | Enforced Count (Server) | Suggested Count (Tablet) | Commercial Category Context |
| :---: | :---: | :---: | :--- |
| **1** | **1078** (98.6%) | **671** (61.4%) | Single units, aerial cakes, garland boxes, bundles, unverified heuristic items |
| **2** | **0** (0.0%) | **52** (4.8%) | Multi-tube fancy fountain pots, paired rocket packs |
| **3** | **0** (0.0%) | **21** (1.9%) | Multi-tube fancy fountain pots, paired rocket packs |
| **4** | **0** (0.0%) | **2** (0.2%) | Classic sparkler packs (5 P), fancy wheel boxes |
| **5** | **0** (0.0%) | **111** (10.2%) | Classic sparkler packs (5 P), fancy wheel boxes |
| **6** | **0** (0.0%) | **6** (0.5%) | Cold pyro boxes, VIP bombs (6 P) |
| **10** | **12** (1.1%) | **176** (16.1%) | Standard sparkler boxes (10 P), rocket packets, ground chakkars |
| **12** | **0** (0.0%) | **12** (1.1%) | Standard sparkler boxes (10 P), rocket packets, ground chakkars |
| **15** | **0** (0.0%) | **2** (0.2%) | Large sparkler packets, fancy aerial shells, bullet rockets |
| **25** | **0** (0.0%) | **19** (1.7%) | Large sparkler packets, fancy aerial shells, bullet rockets |
| **36** | **0** (0.0%) | **1** (0.1%) | Commercial fireworks packs |
| **50** | **3** (0.3%) | **8** (0.7%) | Chorsa bundles, bijali cracker boxes |
| **100** | **0** (0.0%) | **12** (1.1%) | Chorsa bundles, bijali cracker boxes |

---

## 3. High-Priority Products Requiring Business Review

The following **62 products** have been identified for commercial review. They either lack explicit parenthetical tags in the FoxPro master description or represent high-multiple bundles that should be confirmed before wholesale season.

| Code | Product Description | FoxPro UOM | Selling Rate | Suggested Pack | Enforced Pack | Source | Action / Reason |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `00491` | 550- SADA MATKA ANAR OTHER (100P) | `PCS` | ₹15.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `00866` | 158- STRIPPED BIJALI ROSE(50 PCS)10 BAG | `BAG` | ₹11.50 | **50** | **1** | `heuristic` | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. |
| `02122` | 450- FLOWER POTS BIG K.V.S | `PKT` | ₹40.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX)RACHNA | `PKT` | ₹6.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX) AYYAN | `PKT` | ₹6.50 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `02154` | 1119- RING CAPS (1OOPKT= 1 BOX)GOKUL | `PKT` | ₹7.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `02155` | 1120- RING CAPS (1OOPKT= 1 BOX)COCK | `PKT` | ₹7.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `02764` | 451- FLOWER POTS BIG N.M JYOTHI | `PKT` | ₹50.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `02779` | 286- FANCY SPARKLERS LOLLY POP | `PKT` | ₹125.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `02783` | 288- SPINNIG SPARKLERS KALLIAMAL | `PKT` | ₹190.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS) | `BAG` | ₹11.00 | **50** | **1** | `heuristic` | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. |
| `04310` | 168- GOLD BIJALI COCK (50 PCS) | `BAG` | ₹35.50 | **50** | **1** | `heuristic` | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. |
| `04311` | 169- GOLD BIJALI OTHER (100 PCS) | `BAG` | ₹20.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS) | `BAG` | ₹21.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04313` | 171- GOLD BIJALI GIANT OVEEYA(100 PCS) | `BAG` | ₹44.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04314` | 172- GOLD BIJALI APPLE(100 PCS) | `BAG` | ₹27.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04315` | 173- GOLD BIJALI SRIPATHI(100 PCS) | `BAG` | ₹30.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04316` | 174- GOLD BIJALI AYYANAR(100 PCS) | `BAG` | ₹37.50 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04317` | 175- GOLD BIJALI COCK(100 PCS ) | `BAG` | ₹67.00 | **100** | **1** | `heuristic` | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. |
| `04318` | 176- BASKET BOMB SINGADA RAVINDRA(10 BAG | `BAG` | ₹62.00 | **1** | **1** | `fallback` | BAG packaging item with suggested multiple 1. Confirm outer bag case size. |
| `04341` | 296- 28 CHORSA TURKEY  RAJLAXMI(50P= 1 B | `PKT` | ₹13.50 | **50** | **1** | `heuristic` | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. |
| `04343` | 298- 32 CHORSA MIX RED-GOA SUN(50P=1BUND | `PKT` | ₹12.50 | **50** | **1** | `heuristic` | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. |
| `04460` | 452- FLOWER POTS BIG T/MEENA | `PKT` | ₹55.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04461` | 453- FLOWER POTS BIG AYYANAR | `PKT` | ₹68.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04462` | 454- FLOWER POTS BIG OVEEYA | `PKT` | ₹78.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04463` | 455- FLOWER POTS BIG MERCURY | `PKT` | ₹80.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04464` | 456- FLOWER POTS BIG COCK | `PKT` | ₹124.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04465` | 457- FLOWER POTS BIG S.T.D | `PKT` | ₹135.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04468` | 460- FLOWER POTS SPECIAL G.P.M | `PKT` | ₹45.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04469` | 461- FLOWER POTS SPECIAL K.V.S | `PKT` | ₹45.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04470` | 462- FLOWER POTS SPECIAL SRI SAI | `PKT` | ₹50.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04471` | 463- FLOWER POTS SPECIAL NM JYOTHI | `PKT` | ₹60.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04472` | 464- FLOWER POTS SPECIAL ANBARSI | `PKT` | ₹60.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04473` | 465- FLOWER POTS SPECIAL T/MEENA | `PKT` | ₹65.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04474` | 466- FLOWER POTS SPECIAL AYYANAR | `PKT` | ₹102.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04475` | 467- FLOWER POTS SPECIAL OVEEYA | `PKT` | ₹105.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04476` | 468- FLOWER POTS SPECIAL MERCURY | `PKT` | ₹106.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04477` | 469- FLOWER POTS SPECIAL I.N | `PKT` | ₹110.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04478` | 470- FLOWER POTS SPECIAL S.T.D | `PKT` | ₹180.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04479` | 471- FLOWER POTS SPECIAL COCK | `PKT` | ₹220.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04482` | 474- FLOWER POTS ASHOKA K.V.S | `PKT` | ₹55.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04483` | 475- FLOWER POTS ASHOKA SRI SAI | `PKT` | ₹62.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04484` | 476- FLOWER POTS ASHOKA ANBARSI | `PKT` | ₹69.50 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04485` | 477- FLOWER POTS ASHOKA NM JYOTHI | `PKT` | ₹70.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04486` | 478- FLOWER POTS ASHOKA T/MEENA | `PKT` | ₹83.50 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04487` | 479- FLOWER POTS ASHOKA SRIPATHI | `PKT` | ₹85.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04488` | 480- FLOWER POTS ASHOKA OVEEYA | `PKT` | ₹140.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04489` | 481- FLOWER POTS ASHOKA MERCURY | `PKT` | ₹150.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04493` | 485- FLOWER POTS GAINT AYYANAR | `PKT` | ₹150.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04494` | 486- FLOWER POTS GAINT I. N. | `PKT` | ₹155.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04495` | 487- FLOWER POTS GAINT MERCURY | `PKT` | ₹202.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04496` | 488- FLOWER POTS GAINT COL.KOTI MERCURY | `PKT` | ₹250.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04497` | 489- FLOWER POTS GAINT S.T.D | `PKT` | ₹325.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04499` | 491- FLOWER POTS COL KOTI UV.BOX OTHER | `PKT` | ₹110.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04500` | 492- FLOWER POTS COL KOTI UV.BOX ROJAPOO | `PKT` | ₹135.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04501` | 493- FLOWER POTS COL KOTI UV.BOX RAJLAXM | `PKT` | ₹140.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04502` | 494- FLOWER POTS COL KOTI UV.BOX T/MEENA | `PKT` | ₹150.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04503` | 495- FLOWER POTS COL KOTI UV.BOX GOVINDA | `PKT` | ₹165.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `04504` | 496- FLOWER POTS COL KOTI AYYANAR | `PKT` | ₹200.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `05960` | W SPARKULAR MACHINE POWDER | `PKT` | ₹910.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `06136` | W SPARKULAR GUN SADI-(CELL) | `BOX` | ₹150.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |
| `06137` | W SPARKULAR GUN PENCIL-(CELL) | `BOX` | ₹200.00 | **1** | **1** | `fallback` | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. |

---

## 4. Complete Active Commercial Product Catalog (1093 Products)

| Code | Product Description | Brand | FoxPro UOM | Rate (₹) | Suggested Pack | Enforced Pack | Status | Source |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `00013` | 111- ROLL CAPS AGNI | ROLL AND DOT CAPS | `PKT` | ₹48.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00079` | 119- ASST CARTOON(10 PCS)DURGESH (1P) | ASST CARTOON & RAIL | `PKT` | ₹13.50 | 1 | **1** | `APPROVED` | `override` |
| `00080` | 120- ASST CARTOON BEN TEN(25P)AYYANAR 4P | ASST CARTOON & RAIL | `PKT` | ₹55.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00081` | 121- SNAKE CARTOON(25P)SAMLL AYYANAR 4P | ASST CARTOON & RAIL | `PKT` | ₹55.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00082` | 124- BIG NAGGOLI PANDYAN BLACK(100X1=1 B | SERPANTS & NAGGOLI | `BUNDLE` | ₹150.00 | 1 | **1** | `APPROVED` | `override` |
| `00083` | 125- BIG NAGGOLI PANDYAN RED(100X1= 1BOX | SERPANTS & NAGGOLI | `BUNDLE` | ₹155.00 | 1 | **1** | `APPROVED` | `override` |
| `00109` | 178- 9 CM PLAIN INDRA (10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹65.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00110` | 179- 9 CM COL INDRA (10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹69.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00111` | 180- 9 CM PLAIN CLASSIC (10DABBI=1 | 9 CM SPARKLERS | `BOX` | ₹78.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00112` | 181- 9 CM COL CLASSIC (10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹89.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00117` | 192- 10 CM PLAIN LEO | SARAVANA SPARKLERS | `PKT` | ₹15.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00118` | 193- 10 CM GREEN BHAWAN | SARAVANA SPARKLERS | `PKT` | ₹16.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00119` | 194- 10 CM RED DEEOAM | SARAVANA SPARKLERS | `PKT` | ₹17.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00120` | 195- 10 CM SILVER DROPS SARAVANA(5P) | SARAVANA SPARKLERS | `PKT` | ₹15.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00132` | 221- 10 CM PLAIN CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹12.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00133` | 222- 10 CM COL CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹13.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00134` | 223- 10 CM GREEN CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹13.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00136` | 224- 10 CM RED CLASSIC(5 P) | CLASSIC SPARKLERS | `PKT` | ₹13.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00137` | 225- 10 CM 2 IN 1 CLASSIC(5 P) | CLASSIC SPARKLERS | `PKT` | ₹13.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00138` | 226- 12 CM PLAIN LX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹14.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00139` | 227- 12 CM COL LX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹15.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00140` | 228- 12 CM PLAIN DLX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹16.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00142` | 229- 12 CM COL DLX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹17.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00143` | 230- 12 CM GREEN LX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹14.75 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00144` | 276- 10 CM PLAIN ASOK ( 5 P) | ASOK SPARKLERS | `PKT` | ₹20.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00145` | 277- 10 CM COL ASOK ( 5 P) | ASOK SPARKLERS | `PKT` | ₹23.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00147` | 278- 10 CM GREEN ASOK ( 5 P) | ASOK SPARKLERS | `PKT` | ₹28.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00148` | 279- 10 CM RED ASOK ( 5 P) | ASOK SPARKLERS | `PKT` | ₹30.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00149` | 280- 10 CM 4 COLOUR ASOK ( 5 P) | ASOK SPARKLERS | `PKT` | ₹28.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00178` | 148- RED BIJALI ROSE (100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹17.50 | 10 | **10** | `APPROVED` | `override` |
| `00180` | 149- MINI RED BIJALI CAT BRAND(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹58.00 | 10 | **10** | `APPROVED` | `override` |
| `00181` | 150- RED BIJALI AYYANAR (100 PCS) 10 BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹30.00 | 10 | **10** | `APPROVED` | `override` |
| `00182` | 151- RED BIJALI GANESH(100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹41.00 | 10 | **10** | `APPROVED` | `override` |
| `00183` | 152- RED BIJALI S.T.D.(100 PCS ) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹53.00 | 10 | **10** | `APPROVED` | `override` |
| `00184` | 153- RED BIJALI SONY (100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹60.00 | 10 | **10** | `APPROVED` | `override` |
| `00185` | 154- RED BIJALI VIMAL(100 P)10 BAG 1 3/4 | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹65.00 | 10 | **10** | `APPROVED` | `override` |
| `00186` | 290- 10 CHORASA MUNNA DURGESH(100P=1BUND | 10 CHORSA | `BUNDLE` | ₹335.00 | 1 | **1** | `APPROVED` | `override` |
| `00187` | 291- 10 GAINT JAWAN GEMS (100P=1BUNDLE ) | 10 CHORSA | `BUNDLE` | ₹360.00 | 1 | **1** | `APPROVED` | `override` |
| `00223` | 293- 16 CHORSA B GROUP (50P= 1 BUNDEL) | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹7.25 | 50 | **50** | `APPROVED` | `override` |
| `00224` | 294- 28 CHORSA K.R.K (50P= 1 BUNDEL) | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹12.00 | 50 | **50** | `APPROVED` | `override` |
| `00225` | 295- 28 CHORSA TAJ  T/MEENA (50P= 1 BUND | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹13.25 | 50 | **50** | `APPROVED` | `override` |
| `00250` | 308- 20 DLX KING GANESH DURAI( 10 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹25.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00251` | 309- 20 DLX BALAJI( 10 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹37.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00252` | 310- 24 DLX RAGURAM ( 10 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00253` | 311- 24 DLX GANESH DURAI( 10 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹32.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00254` | 312- 24 DLX COCK (10P) | 2 3/4 , 4' DELUXE PATALA | `BOX` | ₹63.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00255` | 313- 28 DLX RAGURAM(10 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹37.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00256` | 314- 32 DLX KICK SHOT BALAJI( 5 P ) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹65.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00257` | 315- 48 DLX RAGURAM ( 5 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹50.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00288` | 329- 2' PARROT AYYANAR (25 PCS) | ONE SOUND DHAMAKA | `PKT` | ₹5.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00289` | 330- 2 3/4 KURVI DURGESH (25 PCS) | ONE SOUND DHAMAKA | `PKT` | ₹6.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00291` | 331- 2 3/4 KURVI VELVAN (10 PCS) | ONE SOUND DHAMAKA | `PKT` | ₹7.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00292` | 332- 2 3/4 KURVI GEMS (25 P) | ONE SOUND DHAMAKA | `PKT` | ₹7.75 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00293` | 333- 2 3/4 GREEN PARROT PONMALAR(25 P) | ONE SOUND DHAMAKA | `PKT` | ₹9.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00294` | 334- 2 3/4 KURVI AYYANAR (25 P) | ONE SOUND DHAMAKA | `PKT` | ₹9.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00297` | 337- 3 1/2 BEN TEN DURGESH/JAYA (15 P) | ONE SOUND DHAMAKA | `PKT` | ₹9.50 | 15 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00298` | 338- 3 1/2 JOKER SADA BAJAJI(10 P) | ONE SOUND DHAMAKA | `PKT` | ₹10.75 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00299` | 339- 3 1/2 MIX LABEL SADA AYYANAR (10 P | ONE SOUND DHAMAKA | `PKT` | ₹13.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00300` | 340- 3 1/2 GREEN PARROT PONMALAR (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹14.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00301` | 341- 3 1/2 ELEPHANT I.N(10 P) | ONE SOUND DHAMAKA | `PKT` | ₹14.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00325` | 399- 2 SOUND DHAMAKA RAJHARISH(10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹22.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00326` | 400- 2 SOUND DHAMAKA NM JYOTHI(10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹25.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00328` | 402- 2 SOUND DHAMAKA I.N. (10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00368` | 413- 2 LXM DHAMAKA GENIUS (25 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹5.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00370` | 415- 3 1/2 LXM DHAMAKA AYYANAR (10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹13.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00371` | 416- 3 1/2 LXM DHAMAKA I.N(10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹14.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00372` | 417- 3 1/2 LXM DHAMAKA AMBIKA(10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹15.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00373` | 418- 3 1/2 LXM DLX DHAMAKA AYYANAR ( 10 | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹22.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00374` | 419- 3 1/2 LXM DHAMAKA S.T.D ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹24.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00378` | 423- 4' LXM ONE SOUND DHAMAKA GENIUS (10 | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹14.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00379` | 424- 4' LXM ONE SOUND DHAMAKA T/MEENA(10 | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹16.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00381` | 426- 4' LXM DHAMAKA I.N ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹18.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00382` | 427- 4' LXM DHAMAKA AYYANAR ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹21.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00383` | 428- 4' LXM DHAMAKA AYYAN ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹32.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00384` | 429- 4' LXM DHAMAKA(10 CM) W/F S.T.D | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹34.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00387` | 432- 4' DLX LXM DHAMAKA I.N ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹23.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00388` | 433- 4' DLX BAJ DHAMAKA T/MEENA( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00389` | 434- 4' DLX LXM DHAMAKA T/MEENA( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹32.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00390` | 435- 4' DLX LXM DHAMAKA S.K.M W/F(12PLY) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹32.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00391` | 436- 4' DLX LXM DHAMAKA AYYANAR ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹35.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00395` | 439- 4 DLX GOLD LXM T/MEENA ( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00396` | 440- 4 DLX GOLD LXM AYYANAR( 10 P) | GULAB KAMAL ONE SOUND DHAMAKA | `PKT` | ₹35.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00427` | 444- FLOWER POTS SMALL RAJLAXMI(10 P) | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹38.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00429` | 445- FLOWER POTS SMALL ARUDHARA(10 P) | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹50.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00430` | 446- FLOWER POTS SMALL MURCURY(10 P) | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹64.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00438` | 517- TRI COL FOUNTAIN RAJHARISH W (5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹185.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00439` | 518- TRI COL FOUNTAIN W UV.BOX OM GANESH | FANCY FLOWER POTS MIXED | `PKT` | ₹190.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00440` | 519- TRI COL FOUNTAIN MERCURY (10 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹265.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00441` | 520- TRI COL FOUNTAIN COCK (5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹297.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00442` | 521- TRI COL FOUNTAIN S.T.D (5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹375.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00443` | 522- TRI COL FOUNTAIN T/MEENA (5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹235.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00444` | 523- F P VARNAJAL AYYAN( 10 P) (1P) | FANCY FLOWER POTS MIXED | `PKT` | ₹415.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00445` | 524- COL FOG FOUNTAIN S.T.D.(5 P) (2P) | FANCY FLOWER POTS MIXED | `PKT` | ₹77.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00446` | 525- JET FOUNTAIN W S.T.D(5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹85.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00447` | 526- KIDDY'S JOY F P 5IN 1 AYYAN ( 5P) | FANCY FLOWER POTS MIXED | `PKT` | ₹165.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00448` | 527- MINI POPPERS 5 IN 1 MERCURY( 5 P ) | FANCY FLOWER POTS MIXED | `PKT` | ₹175.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00449` | 528- HAPPINESS F. POT 5 IN 1 S.T.D (5 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹265.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00450` | 529- TORA TORA F. POT 5 IN 1 AYYAN( 5 P | FANCY FLOWER POTS MIXED | `PKT` | ₹355.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00451` | 530- FIRE DROPS 5 COL MIX AYYAN(1 P)1BOX | FANCY FLOWER POTS MIXED | `BOX` | ₹65.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00452` | 531- KULFI STAR F POT 5 COL MIX PANDYAN | FANCY FLOWER POTS MIXED | `PKT` | ₹75.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00453` | 532- CHEERS 3 IN 1 W S.T.D(3P)(1P) | FANCY FLOWER POTS MIXED | `PKT` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00454` | 533- CRACKLING FOUNTAIN SIVASAKTHI(3 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹200.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00455` | 534- JADUGAR UV.BOX AYYAN (4 P )( 1 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹260.00 | 1 | **1** | `APPROVED` | `override` |
| `00456` | 535- MANORANJAN U.V.BOX AYYAN(4 P)(1P) | FANCY FLOWER POTS MIXED | `PKT` | ₹260.00 | 1 | **1** | `APPROVED` | `override` |
| `00457` | 536- CAN SHOWER BIG TIN DABBA N.M.JYOTH | FANCY FLOWER POTS MIXED | `PKT` | ₹100.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00458` | 537- CAN SHOWER TIN DABBA SRI HARI(1P)1B | FANCY FLOWER POTS MIXED | `PKT` | ₹75.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00459` | 538- LEMON TREE CRA FOUNTION(1P)AYYAN | FANCY FLOWER POTS MIXED | `PKT` | ₹100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00460` | 539- GOLDEN WHISTE SMALL (2P)S.T.D | FANCY FLOWER POTS MIXED | `PKT` | ₹150.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00461` | 540- CHOTA BHAI F P MINI SIREN AYYAN(5P) | FANCY FLOWER POTS MIXED | `PKT` | ₹150.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00462` | 574- CRACKLING EXPRESS WHIP AYYAN | COL WHITH-MAGIC WHIP | `PKT` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00463` | 575- MAGIC WHIP S.T.D( 2 P) | COL WHITH-MAGIC WHIP | `PKT` | ₹89.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00464` | 576- 1000 COL MAGIC WHIP RAMASWAMI | COL WHITH-MAGIC WHIP | `BOX` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00472` | 546- PEACOCK DANCE VENKATESH (1 PKT) | FANCY FLOWER POTS- PEACOCK DANCN | `PKT` | ₹120.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00473` | 547- PEACOCK DANCE DURGESH(1 PKT) | FANCY FLOWER POTS- PEACOCK DANCN | `PKT` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00474` | 548- PEACOCK DANCE GOLD BIG GAYATHRI(1PK | FANCY FLOWER POTS- PEACOCK DANCN | `PKT` | ₹310.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00475` | 549- PEACOCK DANCE (4 COLOUR) AYYAN | FANCY FLOWER POTS- PEACOCK DANCN | `PKT` | ₹180.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00489` | 577- MERCURY FLASH MERCURY | PHOTO FLASH / HELICOPTER  / DRONE | `PCS` | ₹50.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00491` | 550- SADA MATKA ANAR OTHER (100P) | FANCY MATAKA ANAR | `PCS` | ₹15.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00492` | 551- MINI PEARL GUDIYA ( 5 PCS ) | FANCY MATAKA ANAR | `BOX` | ₹135.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00493` | 552- TIM TIM GUDIYA ( 5 PCS ) | FANCY MATAKA ANAR | `BOX` | ₹165.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00494` | 553- LITTLE STAR ANAR GUDIYA ( 5 PCS ) | FANCY MATAKA ANAR | `BOX` | ₹270.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00495` | 554- 2 IN 1 ANAR GUDIYA (10 PCS) | FANCY MATAKA ANAR | `BOX` | ₹325.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00496` | 555- GOLDEN STAR GUDIYA  ( 5PCS) | FANCY MATAKA ANAR | `BOX` | ₹270.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00497` | 556- ASHARFI GUDIYA ( 5 PCS) | FANCY MATAKA ANAR | `BOX` | ₹300.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00499` | 557- JASMINE GUDIYA ( 5PCS) | FANCY MATAKA ANAR | `BOX` | ₹300.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00501` | 558- DAZZLE GUDIYA ( 5 PCS) | FANCY MATAKA ANAR | `BOX` | ₹465.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00502` | 559- DELUXE GUDIYA ( 4 PCS) | FANCY MATAKA ANAR | `BOX` | ₹500.00 | 4 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00503` | 560- GIFT BOX GUDIYA ( 4 PCS) | FANCY MATAKA ANAR | `BOX` | ₹650.00 | 4 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00504` | 561- ASHARFI  GOLDEN STAR OTHER (10 PCS) | FANCY MATAKA ANAR | `BOX` | ₹240.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00505` | 562- MUTT PUTT ANAR MERCURY ( 5 PCS ) | FANCY MATAKA ANAR | `BOX` | ₹200.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00533` | 588- G C BIG T/MEENA( 10 P)(10P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00534` | 589- G C BIG GANESH ( 10 P)(10P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹35.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00535` | 590- G C BIG JENIS(10 P)(5P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹40.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00536` | 591- G C BIG W MERCURY(10 P)(5P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹44.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00537` | 592- G C BIG R/G S.T.D (25 P)(4P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹53.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00540` | 644- COCKTAL SPINER AYYAN | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹50.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00542` | 645- DISCO WHEEL GAYATHRI(10 PCS) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹76.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00543` | 646- DISCO WHEEL S.M.K.(10 PCS) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹85.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00544` | 647- SILVER GAINT WHEEL MERCURY (10P)(2P | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹165.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00564` | 707- 18 T STAR D/VADIVEL(10P) 10 P | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹15.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00565` | 708- 18 T STAR SRIPATHI(10P) 10 P | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹16.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00566` | 709- 18 T STAR T/MEENA (10P) 10 P | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹20.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00567` | 710- 48 T STAR (10P) SRIPATHI 10 P | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹50.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00568` | 711- 120 T STAR S.T.D (10P) 5 P | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹155.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00571` | 714- JIL JIL 1X10 PEC=1 BOX U.V BALAJI | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹155.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00609` | 594- G C BIG VENKATESH (25 PCS) (4P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹45.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00610` | 595- G C BIG T/MEENA (25 PCS) (W) (4P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹75.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00611` | 596- G C BIG GANESH (25 PCS) (4P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹80.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00614` | 735- BULLET BOMB MINI SRI ATHISAYA(10P) | ATOM BOMB | `PKT` | ₹14.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00615` | 736- MINI BULLET BOMB T/MEENA(10 P)10 | ATOM BOMB | `PKT` | ₹16.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00616` | 737- BULLET BOMB MINI SRIPATHI ( 10 P ) | ATOM BOMB | `PKT` | ₹18.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00617` | 738- BULLET BOMB MEDIUM T/MEENA( 10 P ) | ATOM BOMB | `PKT` | ₹21.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00618` | 739- BULLET BOMB MEDIUM APPLE( 10 P ) | ATOM BOMB | `PKT` | ₹21.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00619` | 740- SUPER BULLET BOMB AYYANAR ( 10 P ) | ATOM BOMB | `PKT` | ₹25.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00620` | 741- BULLET BOMB GANESH ( 10 P ) | ATOM BOMB | `PKT` | ₹27.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00621` | 742- BULLET BOMB BIG DLX T/MEENA ( 10 P | ATOM BOMB | `PKT` | ₹32.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00622` | 743- SUPER BULLET BOMB ( 10 P ) OVEEYA | ATOM BOMB | `PKT` | ₹39.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00624` | 745- SADDAM BOMB A1 | ATOM BOMB | `PKT` | ₹44.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00625` | 746- SADDAM BOMB AUGUST RATE TERKHEDA | ATOM BOMB | `PKT` | ₹47.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00626` | 747- SADDAM BOMB AUGUST RATE SANTOSH | ATOM BOMB | `PKT` | ₹48.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `00630` | 751- SOLDIER BOMB GREEN W/G (10 P)V.F.I | ATOM BOMB | `PKT` | ₹75.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00631` | 752- JHANSI BOMB GREEN W/F(10P)MALATI'S | ATOM BOMB | `PKT` | ₹80.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00688` | 598- G C ASOKA T/MEENA (10 P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹40.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00691` | 122- RAJDHANI RAIL(10 PCS)AYYANAR (10 P) | ASST CARTOON & RAIL | `PKT` | ₹65.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00692` | 123- FIGHTER ANIL | ASST CARTOON & RAIL | `PKT` | ₹82.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00707` | 138- GANGA JAMUNA SRI PATHI(5P) | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹45.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00744` | 541- MINI SIREM F. POT COCK ( 3 PCS ) | FANCY FLOWER POTS MIXED | `PKT` | ₹175.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00745` | 542- BIG SIREM F. POT COCK ( 3 PCS ) | FANCY FLOWER POTS MIXED | `PKT` | ₹280.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00746` | 543- FLY BEES MIX ( 1 P) I.N | FANCY FLOWER POTS MIXED | `PKT` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00747` | 544- SUPER STAR CRACKLING ( 1 P ) AYYAN | FANCY FLOWER POTS MIXED | `PKT` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00758` | 599- G C ASOKA AYYANAR(10 P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹50.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00760` | 648- LOTUS WHEEL I. N (5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹315.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00761` | 649- SUN FLOWER WHEEL I. N (10 PCS) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹255.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00769` | 600- G C ASOKA W MERCURY(10 P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹67.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00772` | 782- 100 LAR JAYEM | GARLAND & LAR | `PKT` | ₹24.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00773` | 783- 200 LAR JAYEM | GARLAND & LAR | `PKT` | ₹38.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00774` | 784- 300 LAR JAYEM | GARLAND & LAR | `BOX` | ₹72.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00775` | 785- 600 LAR JAYEM | GARLAND & LAR | `BOX` | ₹95.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00777` | 787- 1000 WALA LAR KALUGU( 350) | GARLAND & LAR | `BOX` | ₹100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00778` | 788- 1000 WALA LAR JAYEM ( 400) AUGUST | GARLAND & LAR | `BOX` | ₹115.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00779` | 789- 1000 WALA LAR JAYEM ( 400) SEPTEMBE | GARLAND & LAR | `BOX` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00848` | 231- 12 CM RED LX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹17.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00866` | 158- STRIPPED BIJALI ROSE(50 PCS)10 BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹11.50 | 50 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00876` | 601- G C ASOKA BIG SIZE GANESH(10 P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹72.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00886` | 991- 1 3/4 25 SHOT 5 DIEFERENT MIX S.T.D | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00887` | 992- 2' PIPE 30 SHOT M. COL WOW STAR | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00888` | 993- 1/2 PIPE 50 SHOT'S BEUTY S.T.D | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹2550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00889` | 994- 30 SHOT PEACOCK DANCE I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `00890` | 995- 3 X 12 VANDE MATARAM 3 COL MERCURY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1320.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `00925` | 602- G C ASOKA S.T.D (10 P) (5P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹88.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `01167` | 139- GANGA JAMUNA OVEETA(5P) | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹52.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `01175` | 140- GANGA JAMUNA FLOWER BOMB AYYANAR | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹60.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `01176` | 141- GANGA JAMUNA MERCURY( 5 P) | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹65.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `01989` | 112- ROLL CAPS S.T.D. | ROLL AND DOT CAPS | `PKT` | ₹80.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02042` | 281- 12 CM PLAIN ASOK ( 2 P) | ASOK SPARKLERS | `PKT` | ₹35.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02081` | 142- MAGIC FOUNTAIN OVEEYA(10 PCS) | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹120.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02082` | 113- DOT CAPS RATHANA | ROLL AND DOT CAPS | `PKT` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02107` | 1109- MISSILE GUN 75203 YUG (1 PCS) | 8 SHOT'S MISSIEL GUN & FANCY GUN | `PCS` | ₹14.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02108` | 1110- MISSILE GUN DY787 YUG  (1 PCS) | 8 SHOT'S MISSIEL GUN & FANCY GUN | `PCS` | ₹20.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02109` | 1111- 5 - STAR SMALL VERO TOVE SOM | 8 SHOT'S MISSIEL GUN & FANCY GUN | `PCS` | ₹21.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02122` | 450- FLOWER POTS BIG K.V.S | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02124` | 603- G C ASOKA SPINNER W JENIS (10 P) | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹75.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX)RACHNA | RING CAPS AND MISSILE | `PKT` | ₹6.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX) AYYAN | RING CAPS AND MISSILE | `PKT` | ₹6.50 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02154` | 1119- RING CAPS (1OOPKT= 1 BOX)GOKUL | RING CAPS AND MISSILE | `PKT` | ₹7.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02155` | 1120- RING CAPS (1OOPKT= 1 BOX)COCK | RING CAPS AND MISSILE | `PKT` | ₹7.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02157` | 1121- MISSILE SIREN(127X1)TITANIC ORIGIN | RING CAPS AND MISSILE | `PKT` | ₹65.00 | 1 | **1** | `APPROVED` | `override` |
| `02275` | 282- 12 CM COLOUR ASOK ( 2 P) | ASOK SPARKLERS | `PKT` | ₹40.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02519` | 1065- HAND RIBAN PAPER MIX 1 BOX 'KING'S | CONFETTI & PAPER SHOTS | `PCS` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02520` | 1066- 40 CM PARTY POPPER HAND WALA(1P)JA | CONFETTI & PAPER SHOTS | `PCS` | ₹25.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02525` | 1087- BULLET ROCKET YUG ( 36 PCS) | GUNS & PISTOLS | `PCS` | ₹108.00 | 36 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02660` | 666- BABY ROCKET RAJ LAXMI (10P) | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹30.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02664` | 143- ULTA PULTA FLOWER BOMB AYYAN | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02665` | 283- 15 CM PLAIN ASOK ( 2 P) | ASOK SPARKLERS | `PKT` | ₹60.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02667` | 284- 30 CM PLAIN ASOK ( 2 P) | ASOK SPARKLERS | `PKT` | ₹60.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02668` | 285- 30 CM COL ASOK ( 2 P) | ASOK SPARKLERS | `PKT` | ₹70.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02669` | 567- DANCING BUTTERFLY R/G.(10P) VANAJA | COLOUR - DANCING BUTTERFLY | `PKT` | ₹45.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02670` | 568- DANCING BUTTERFLY R/G UV.BOX S.M.K | COLOUR - DANCING BUTTERFLY | `PKT` | ₹46.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `02671` | 569- DANCING BUTTERFLY AYYAN ( 10 P) | COLOUR - DANCING BUTTERFLY | `PKT` | ₹125.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02672` | 670- PYRO DANCE BUTTERFLY SUNSHINE( 10P) | COLOUR - DANCING BUTTERFLY | `PKT` | ₹140.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02673` | 571- COL CHAN. BUTTERFLY S.T.D (10P) | COLOUR - DANCING BUTTERFLY | `PKT` | ₹132.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02676` | 667- COLOUR ROCKET AYYANAR (10P) ) | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹48.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02677` | 668- RAINBOW ROCKET S.T.D (10P) | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹130.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02679` | 670- ROCKET BOMB (10P) 5P N.M.JYOTHI | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹45.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02680` | 671- ROCKET BOMB (10P) 5P AYYANAR | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹55.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02681` | 672- ROCKET BOMB (10P) 5P GANESH | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹58.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02709` | 196- 12 CM PLAIN LEO | SARAVANA SPARKLERS | `PKT` | ₹20.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02710` | 197- 30 CM GREEN SARAVANA (2 P) | SARAVANA SPARKLERS | `PKT` | ₹25.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02711` | 198- 30 CM RED SARAVANA (2 P) | SARAVANA SPARKLERS | `PKT` | ₹27.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02712` | 199- 30 CM SILVER DROPS SARAVANA | SARAVANA SPARKLERS | `PKT` | ₹27.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `02756` | 606- G C SPL (10 P) VENKATESH | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹36.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02764` | 451- FLOWER POTS BIG N.M JYOTHI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹50.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02765` | 232- 12 CM 2 IN 1 CLASSIC(5 P) | CLASSIC SPARKLERS | `PKT` | ₹17.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02779` | 286- FANCY SPARKLERS LOLLY POP | ASOK SPARKLERS | `PKT` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02782` | 287- DANCING UMRELA OWL | ASOK SPARKLERS | `PKT` | ₹165.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02783` | 288- SPINNIG SPARKLERS KALLIAMAL | ASOK SPARKLERS | `PKT` | ₹190.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02797` | 578- PHOTO FLASH VENKATESH | PHOTO FLASH / HELICOPTER  / DRONE | `PCS` | ₹52.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02832` | 182- 9 CM 2 IN 1 CLASSIC(10DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹120.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02841` | 233- 12 CM 4 IN 1 LX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹22.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02852` | 607- G C SPL (10 P) T/MEENA | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹56.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02856` | 715- JIL JIL 1X10 PEC=1 BOX SRIPATH | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹160.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02884` | 579- DISCO FLASH S.T.D | PHOTO FLASH / HELICOPTER  / DRONE | `PCS` | ₹80.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `02885` | 580- SKY SCRAPPER DRONE MERCURY ( 5 P ) | PHOTO FLASH / HELICOPTER  / DRONE | `PCS` | ₹125.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02886` | W 30 SHOTS M. COL. U V BOX AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹380.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02887` | W 60 SHOTS M. COL. U V BOX AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹760.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02888` | W 120 SHOTS M. COL. U V BOX AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹1520.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02889` | W 15 SHOTS M. COL. U V BOX N.S.V | OFF SEASON LIST 2025-26 | `PKT` | ₹290.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02890` | W 25 SHOTS M. COL. U V BOX N.S.V | OFF SEASON LIST 2025-26 | `PKT` | ₹410.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02891` | W 60 SHOTS M. COL. U V BOX N.S.V | OFF SEASON LIST 2025-26 | `PKT` | ₹870.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02892` | W 100 SHOTS M.COL. U V BOX N.S.V | OFF SEASON LIST 2025-26 | `PKT` | ₹1480.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02893` | W 30 SHOTS M. COL.RAJ | OFF SEASON LIST 2025-26 | `PKT` | ₹330.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02894` | W 1000 LAR HALF ANBARSI | OFF SEASON LIST 2025-26 | `PKT` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02895` | W 2000 LAR HALF ANBARSI | OFF SEASON LIST 2025-26 | `PKT` | ₹250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02896` | W 5000 LAR HALF ANBARSI | OFF SEASON LIST 2025-26 | `PKT` | ₹625.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02897` | W 2 1/2" F. PIPE(3 PCS)AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹225.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02898` | W 1000 LAR AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹310.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02899` | W 2000 LAR AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹620.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02900` | W 5000 LAR AYYANAR | OFF SEASON LIST 2025-26 | `PKT` | ₹1550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02901` | W 30 SHOTS M. COL. U V BOX I.N | OFF SEASON LIST 2025-26 | `PKT` | ₹550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02902` | W 120 SHOTS RANG DE BASANTI I.N | OFF SEASON LIST 2025-26 | `PKT` | ₹2300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02903` | W 120 SHOTS TRANSFORMER I.N | OFF SEASON LIST 2025-26 | `PKT` | ₹2400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02904` | W 1000 LAR CLASSIC MUGUNTH | OFF SEASON LIST 2025-26 | `PKT` | ₹155.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `02905` | W 1000 LAR (600 COUNTING) S.K.M | OFF SEASON LIST 2025-26 | `PKT` | ₹180.00 | 1 | **1** | `APPROVED` | `override` |
| `03003` | 716- JIL JIL 1X10 PEC=1BOX T/MEENA | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹270.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03088` | 114- R & G MATCH BOX SHANTHI(600DABBA) | MATCH BOX | `BUNDLE` | ₹500.00 | 1 | **1** | `APPROVED` | `override` |
| `03089` | 183- 7 CM PLAIN M.R.P. (10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹80.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03090` | 184- 7 CM COL SARAVANA(10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹90.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03091` | 185- 7 CM GREEN SARAVANA (10 DABBI=1BOX | 9 CM SPARKLERS | `BOX` | ₹105.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03092` | 186- 7 CM RED M.R.P. (10 DABBI=1BOX | 9 CM SPARKLERS | `BOX` | ₹120.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03093` | 187- 7 CM COL VASANTHA(10 DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹95.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03094` | 188- 7 CM PLAIN GOLD S.T.D(10DABBI=1BOX | 9 CM SPARKLERS | `BOX` | ₹180.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03095` | 200- 50 CM PLAIN PIPE SARAVANA ( 1 P ) | SARAVANA SPARKLERS | `PKT` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03096` | 234- 12 CM  5 IN 1(GIFT BOX)CLASSIC | CLASSIC SPARKLERS | `PKT` | ₹110.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03097` | 235- 15 CM PLAIN AB MAGIC CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹22.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03098` | 236- 15 CM PLAIN DLX CLASSIC(5 P) | CLASSIC SPARKLERS | `PKT` | ₹25.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03099` | 237- 15 CM PLAIN BOXE(2P CELLEPHO CLASSI | CLASSIC SPARKLERS | `PKT` | ₹26.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03100` | 238- 15 CM COL AB MAGIC CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹25.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03101` | 239- 15 CM COL DLX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹27.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03102` | 240- 15 CM COL BOXE(2P CELLEPHONE)CLASSI | CLASSIC SPARKLERS | `PKT` | ₹29.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03103` | 241- 15 CM GREEN CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹23.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03104` | 242- 15 CM RED CLASSIC  (5 P) | CLASSIC SPARKLERS | `PKT` | ₹27.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03105` | 243- 15 CM 2 IN 1 CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹29.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03107` | 245- 15 CM 2IN1 BOXE(2P CELLEPHON CLASSI | CLASSIC SPARKLERS | `PKT` | ₹31.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03108` | 246- 15 CM MIX TRIX CLASSIC | CLASSIC SPARKLERS | `PKT` | ₹34.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03109` | 247- 15 CM SKY PARK (GIFT BOX)CLASSIC | CLASSIC SPARKLERS | `PKT` | ₹135.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03110` | 248- 30 CM PLAIN AB MAGIC CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹22.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03111` | 249- 30 CM PLAIN DLX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹25.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03112` | 250- 30 CM PLAIN BOXE(2P CELLEPHO CLASSI | CLASSIC SPARKLERS | `PKT` | ₹26.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03175` | 581- SUPER DRONE W AYYAN( 5 PCS) | PHOTO FLASH / HELICOPTER  / DRONE | `PKT` | ₹170.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03176` | 582- HELICOPTER AYYAN ( 5PCS) | PHOTO FLASH / HELICOPTER  / DRONE | `PKT` | ₹80.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03177` | 583- HELICOPTER R. KRISHNA.( 5PCS) | PHOTO FLASH / HELICOPTER  / DRONE | `PKT` | ₹75.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03179` | 585- HELICOPTER ANIL( 5PCS) | PHOTO FLASH / HELICOPTER  / DRONE | `PKT` | ₹100.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03180` | 586- HELICOPTER SUNSHINE( 10 PCS) | PHOTO FLASH / HELICOPTER  / DRONE | `PKT` | ₹290.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03208` | 608- G C SPL (10 P) GANESH | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹57.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03210` | 610- G C SPL (10 P)(1P)W COLOUR JENIS | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹70.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03211` | 611- G C SPL (10 P)(1P) MERCURY | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹82.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03212` | 612- G C SPL W (10 P) I.N | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹90.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03213` | 613- G C SPL (10 P) (5 P) SUNSHINE | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹94.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03214` | 614- 45 CM G C SPL (10 P) COCK | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹124.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03216` | 696- WHISTLING ROCKET K.M.RAJA(10P)2P | FANCY ROCKETS | `PKT` | ₹115.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03217` | 697- WHISTLING ROCKET UV BOX KABILESH | FANCY ROCKETS | `PKT` | ₹135.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03218` | 698- WHISTLING ROCKET MERCURY(10P)2P- | FANCY ROCKETS | `PKT` | ₹200.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03219` | 699- WHISTLING ROCKET ANIL(10P)2P- | FANCY ROCKETS | `PKT` | ₹227.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03220` | 700- SILVER JET ROCKET S.T.D (10 P) 2 P | FANCY ROCKETS | `PKT` | ₹225.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03221` | 701- ROHINI ROCKET S.T.D (10 P) 2 P | FANCY ROCKETS | `PKT` | ₹227.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03222` | 702- MULTI COLOUR ROCKET MERCURY ( 6PCS) | FANCY ROCKETS | `PKT` | ₹113.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03223` | 703- GOLDEN WILLOW ROC.COCK ( 10P)1P | FANCY ROCKETS | `PKT` | ₹470.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03224` | 704- MULTI MUSIC ROCKET ANIL (1BOX)1B | FANCY ROCKETS | `PKT` | ₹353.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03225` | 705- PARACHUTE ROCKET AYYAN (4 P) 2 P | FANCY ROCKETS | `PKT` | ₹375.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03226` | 706- PARACHUTE ROCKET S.T.D ( 5 PCS) 1 | FANCY ROCKETS | `PKT` | ₹575.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03229` | 719- 7 CM PENCIL VIRBALAJI ( 10 P ) 10 P | PENCILS & FANCY TORCHES, | `PKT` | ₹20.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03230` | 720- 7 CM PENCIL T/MEENA ( 10 P ) 10 P | PENCILS & FANCY TORCHES, | `PKT` | ₹24.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03231` | 721- 10 CM PENCIL VIRBALAJI ( 10 P ) 10 | PENCILS & FANCY TORCHES, | `PKT` | ₹36.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03232` | 722- 10 CM PENCIL T/MEENA ( 10 P ) 10 P | PENCILS & FANCY TORCHES, | `PKT` | ₹45.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03233` | 723- 12 CM PENCIL VIRBALAJI ( 10 P ) | PENCILS & FANCY TORCHES, | `PKT` | ₹43.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03234` | 144- MAGIC FOUNTAIN MAGHTY BOMB COCK | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹175.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03235` | 145- THE GREAT SPLENDOUR S.T.D( 1 P ) | JEE BOOM BAA & CHIT PUT,GANGA JAMUNA & M | `PKT` | ₹70.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03265` | 753- L. B. BOMB GREEN W/F (10 P) B.F.W. | ATOM BOMB | `PKT` | ₹80.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03266` | 754- LALKAR BOMB GREEN W/F(10 P) B.F.W | ATOM BOMB | `PKT` | ₹85.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03267` | 755- LALKAR BOMB FOIL W/F(10 P) B.F.W | ATOM BOMB | `PKT` | ₹90.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03271` | 759- BHUCHAL BOMB SHAKTI | ATOM BOMB | `PKT` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03272` | 760- THUNDER BOMB GREEN (10 P) S.T.D | ATOM BOMB | `PKT` | ₹130.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03273` | 761- MAHAKAL BOMB SHAKTI | ATOM BOMB | `PKT` | ₹130.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03274` | 762- MARSHAL BLACK BOMB GREEN S.Q. SHAKT | ATOM BOMB | `PKT` | ₹140.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03275` | 763- V.I.P BOMB GREEN S.Q (6 P) SHAKTI | ATOM BOMB | `PKT` | ₹140.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03280` | 768- TOP TIGER 1 NO FANCY F.W | ATOM BOMB | `PKT` | ₹45.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03281` | 769- TOP TIGER 4 NO FANCY F.W | ATOM BOMB | `PKT` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03283` | 771- TOP TIGER 5 NO FANCY F.W | ATOM BOMB | `PKT` | ₹145.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03284` | 772- TOP TIGER 6 NO FANCY F.W | ATOM BOMB | `PKT` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03285` | 773- SHER SHIKAR 6 NO FANCY F.W | ATOM BOMB | `PKT` | ₹160.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03286` | 774- SIMBA 6 NO FANCY F.W | ATOM BOMB | `PKT` | ₹170.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03287` | 775- SHER SHIKAR GOLD 6 NO B. R. F.W | ATOM BOMB | `PKT` | ₹180.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03288` | 776- JUNGLE TOP TIGER GOLD 6 NO B. R. F. | ATOM BOMB | `PKT` | ₹180.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `03294` | 790- 1000 WALA LAR JAYEM ( 400) OCTOBER | GARLAND & LAR | `BOX` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03295` | 791- 1000 WALA LAR JAYEM ( 400) NOVEMBER | GARLAND & LAR | `BOX` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03296` | 792- 1000 WALA LAR U.V.BOX ANBARSI GRAND | GARLAND & LAR | `BOX` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03297` | 793- 1000 WALA LAR U.V.BOX GAJA | GARLAND & LAR | `BOX` | ₹140.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03298` | 794- 1000 WALA LAR UV.BOX TAJ RED MUGUND | GARLAND & LAR | `BOX` | ₹145.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03299` | 795- 1000 WALA LAR FULL COUNTING MUGUND | GARLAND & LAR | `BOX` | ₹180.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03300` | 796- 1000 WALA LAR FULL COUNTING | GARLAND & LAR | `BOX` | ₹180.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03301` | 797- 1000 WALA LAR FULL COUNTING S.K.M | GARLAND & LAR | `BOX` | ₹185.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03302` | 798- 1000 WALA LAR FUSE COUNTING AYYANAR | GARLAND & LAR | `BOX` | ₹300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03306` | 802- 2000 WALA LAR KALUGU | GARLAND & LAR | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03307` | 803- 2000 WALA LAR ( 400 ) AUGUST JAYEM | GARLAND & LAR | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03308` | 804- 2000 WALA LAR ( 400) SEPTEMBER JAYE | GARLAND & LAR | `BOX` | ₹250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03309` | 805- 2000 WALA LAR ( 400) OCTOBER JAYEM | GARLAND & LAR | `BOX` | ₹260.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03310` | 806- 2000 WALA LAR ( 400) NOVEMBER JAYEM | GARLAND & LAR | `BOX` | ₹260.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03311` | 807- 2000 WALA LAR ANBARSI | GARLAND & LAR | `BOX` | ₹260.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03312` | 808- 2000 WALA LAR GAJA | GARLAND & LAR | `BOX` | ₹280.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03313` | 809- 2000 WALA LAR FULL COUNTING MUGUND | GARLAND & LAR | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03314` | 810- 2000 WALA LAR FULL COUNTING | GARLAND & LAR | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03315` | 811- 2000 WALA LAR FULL COUNTING S.K.M | GARLAND & LAR | `BOX` | ₹370.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03316` | 812- 2000 WALA LAR FUSE-FULL COUN.AYYANA | GARLAND & LAR | `BOX` | ₹600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03320` | 816- 5000 WALA LAR KALUGU | GARLAND & LAR | `BOX` | ₹500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03321` | 817- 5000 WALA LAR ( 400 ) AUGUST JAYEM | GARLAND & LAR | `BOX` | ₹575.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03322` | 818- 5000 WALA LAR ( 400) SEPTEMBER JAYE | GARLAND & LAR | `BOX` | ₹625.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03323` | 819- 5000 WALA LAR ( 400) OCTOBER JAYEM | GARLAND & LAR | `BOX` | ₹650.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03324` | 820- 5000 WALA LAR ( 400) NOVEMBER JAYEM | GARLAND & LAR | `BOX` | ₹650.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03325` | 821- 5000 WALA LAR GRAND U.V.BOX ANBARSI | GARLAND & LAR | `BOX` | ₹650.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03326` | 822- 5000 WALA LAR U.V.BOX GAJA | GARLAND & LAR | `BOX` | ₹700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03327` | 823- 5000 WALA LAR U.V.BOX | GARLAND & LAR | `BOX` | ₹900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03328` | 824- 5000 WALA LAR FULL COUNTING S.K.M | GARLAND & LAR | `BOX` | ₹925.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03329` | 825- 5000 WALA LAR FUSE U.V.BOX EVEREST | GARLAND & LAR | `BOX` | ₹1050.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03330` | 826- 5000 WALA LAR FUSE AYYANAR | GARLAND & LAR | `BOX` | ₹1500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03334` | 830- 10000 WALA LAR U.V.BOX GAJA | GARLAND & LAR | `BOX` | ₹1200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03335` | 831- 10000 WALA LAR JAYEM | GARLAND & LAR | `BOX` | ₹1150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03336` | 832- 10000 WALA LAR( 400 ) AUGUST JAYEM | GARLAND & LAR | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03337` | 833- 10000 WALA LAR( 400) SEPTEMBER JAYE | GARLAND & LAR | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03338` | 834- 10000 WALA LAR(400) OCTOBER JAYEM | GARLAND & LAR | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03339` | 835- 10000 WALA LAR FULL COUNTING S.K.M | GARLAND & LAR | `BOX` | ₹1850.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03340` | 836- 10000 WALA LAR FULL COUNTING EVERES | GARLAND & LAR | `BOX` | ₹2100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `03341` | 837- 10000 WALA LAR S.T.D | GARLAND & LAR | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04004` | 840- 6 SHOTS BIG ROYAL-SALUTE AYYAN | SHOTS & MULTISHOTS | `BOX` | ₹420.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04005` | 841- 7 SHOTS OTHER(5 PCS) (5P) | SHOTS & MULTISHOTS | `BOX` | ₹65.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04006` | 842- 7 SHOTS J.K (5 PCS) (5P) | SHOTS & MULTISHOTS | `BOX` | ₹80.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04007` | 843- 7 SHOTS MERCURY (5 PCS) (5P) | SHOTS & MULTISHOTS | `BOX` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04008` | 844- 7 SHOTS I.N (5 PCS) (5P) | SHOTS & MULTISHOTS | `BOX` | ₹136.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04009` | 845- 7 SHOTS ANIL (5 PCS) (5P) | SHOTS & MULTISHOTS | `BOX` | ₹170.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04012` | 848- 7 SHOTS OTHER (10 PCS) | SHOTS & MULTISHOTS | `BOX` | ₹180.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04013` | 849- | SHOTS & MULTISHOTS | `BOX` | ₹0.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04014` | 850- 7 SHOTS I. N.(10 PCS | SHOTS & MULTISHOTS | `BOX` | ₹270.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04015` | 851- 7 SHOTS MERCURY(10 PCS) | SHOTS & MULTISHOTS | `BOX` | ₹250.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04016` | 852- 7 SHOTS SIGNAL ROCKET COCK(15 PCS) | SHOTS & MULTISHOTS | `BOX` | ₹500.00 | 15 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04018` | 854- 12 SHOTS R/G RIDER U.V.SQUARE APPLE | SHOTS & MULTISHOTS | `BOX` | ₹105.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04019` | 855- 12 SHOTS SQ. R/G RIDER SQUARE AYYAN | SHOTS & MULTISHOTS | `BOX` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04020` | 856- 12 SHOTS SQ. R/G U.V. SQUARE MORI | SHOTS & MULTISHOTS | `BOX` | ₹135.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04021` | 857- 12 SHOTS  SQ. R/G RIDER SQUARE ANIL | SHOTS & MULTISHOTS | `BOX` | ₹185.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04022` | 858- 12 SHOTS  SQ. R/G RIDER SQUARE COCK | SHOTS & MULTISHOTS | `BOX` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04023` | 859- 12 SHOTS  SQ. COL COMBO PACK SONY | SHOTS & MULTISHOTS | `BOX` | ₹1000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04026` | 1058- SNOW SPRAY WHITE TAIWAN | COLOUR DHUA | `PKT` | ₹22.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04028` | 1060- COL SMOKE DHUA 5COL(5P)SUP.KING | COLOUR DHUA | `PKT` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04029` | 1061- COL SMOKE DHUA ORANGE COL SUP.KING | COLOUR DHUA | `PKT` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04030` | 1062- COL SMOKE DHUA YELLOW COL SUP.KING | COLOUR DHUA | `PKT` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04032` | 1068- 4 SHOTS PAPER FANTASIA KIARA | CONFETTI & PAPER SHOTS | `BOX` | ₹135.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04033` | 1069- 8 SHOTS PAPER KBC KIARA | CONFETTI & PAPER SHOTS | `BOX` | ₹240.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04034` | 1070- 8 SHOTS PAPER BONANZA AISHWARYA | CONFETTI & PAPER SHOTS | `BOX` | ₹250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04035` | 1071- 16 SHOTS PAPER COL MAGIC S.T.D | CONFETTI & PAPER SHOTS | `BOX` | ₹220.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04036` | 1072- 21 SHOTS PAPER CENTURY PEOPLES | CONFETTI & PAPER SHOTS | `BOX` | ₹750.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04037` | 1074- POP POP MULTI COLOUR AUGUST ORIGIN | POP - POP | `PKT` | ₹5.25 | 1 | **1** | `DEFAULT` | `fallback` |
| `04041` | 1078- POP POP COLOUR BIG BAHUBALI | POP - POP | `PKT` | ₹0.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | POP - POP | `PKT` | ₹6.00 | 1 | **1** | `APPROVED` | `override` |
| `04043` | 1080- MATCHIS ONE SOUND AUGUST M.V.10PKT | POP - POP | `BOX` | ₹67.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04045` | 1088- YOGESH BLACK GUN REX ( 12 PCS) | GUNS & PISTOLS | `PKT` | ₹7.00 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04046` | 1089- TOM COLOUR YUG ( 12 PCS ) | GUNS & PISTOLS | `PCS` | ₹7.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04047` | 1090- V-30 COLOUR VISHNU (12 PCS) | GUNS & PISTOLS | `PCS` | ₹12.10 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04048` | 1091- ROBOT BLACK S-61 SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹12.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04049` | 1092- V-301 COLOUR VISHNU ( 10 PCS) | GUNS & PISTOLS | `PCS` | ₹12.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04050` | 1093- V-35 BLACK VISHNU(10 PCS) | GUNS & PISTOLS | `PCS` | ₹15.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04051` | 1094- 86 BLACK SOM(12 PCS) | GUNS & PISTOLS | `PCS` | ₹17.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04052` | 1095- 86 COLOUR SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹23.00 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04053` | 1096- NICE BLACK SOM(12 PCS) | GUNS & PISTOLS | `PCS` | ₹18.00 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04054` | 1097- NICE COLOUR SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹23.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04055` | 1098- VATMAN BLACK SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹21.00 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04056` | 1099- VATMAN COLOUR SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹26.00 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04057` | 1100- DOLPHIN BLACK SOM(6 PCS) | GUNS & PISTOLS | `PCS` | ₹29.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04058` | 1101- DOLPHIN COLOUR SOM (6 PCS) | GUNS & PISTOLS | `PCS` | ₹37.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04059` | 1102- TIGER BLACK SOM(12 PCS) | GUNS & PISTOLS | `PCS` | ₹61.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04060` | 1103- TIGER COLOUR SOM (12 PCS) | GUNS & PISTOLS | `PCS` | ₹67.50 | 12 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04061` | 1104- S-151 COLOUR SOM | GUNS & PISTOLS | `PCS` | ₹86.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04062` | 1105- SPIDER BLACK SOM ( 3 PCS) | GUNS & PISTOLS | `PCS` | ₹89.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04063` | 1106- SPIDER COLOUR SOM  ( 3 PCS) | GUNS & PISTOLS | `PCS` | ₹97.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04064` | 1107- CAMANDO BLACK SOM ( 3 PCS) | GUNS & PISTOLS | `PCS` | ₹102.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04065` | 1108- CAMANDO COLOUR SOM ( 3 PCS) | GUNS & PISTOLS | `PCS` | ₹109.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04094` | 1084- PATANG BALLOON (10 P) KING'S | POP - POP | `BOX` | ₹16.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04095` | 1085- G-11 MACHIS GUN (1 PCS )VISHNU | POP - POP | `BOX` | ₹50.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04101` | 1112- 5 - STAR BIG RING SOM | 8 SHOT'S MISSIEL GUN & FANCY GUN | `PCS` | ₹30.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04109` | 1073- MONEY RAIN ( 1 PCS) MERCURY | CONFETTI & PAPER SHOTS | `BOX` | ₹115.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04125` | 862- 12 SHOTS M.COL SQUARE S. R. M | SHOTS & MULTISHOTS | `BOX` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04153` | 777- LADEN BOMB 6 NO B. R. F.W | ATOM BOMB | `PKT` | ₹180.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04192` | 115- R & G MATCH BOX RAYAL(600 DABBA) | MATCH BOX | `BUNDLE` | ₹500.00 | 1 | **1** | `APPROVED` | `override` |
| `04193` | 116- ANCHOR MAGIC POTS (5 IN 1 )SHANTHI | MATCH BOX | `PKT` | ₹55.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04194` | 117- GEM MEGA ( 10 PKT ) 3 COL SHANTHI | MATCH BOX | `PKT` | ₹145.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04195` | 118- WONDER CRACKLING ( 10 PCS) SHANTHI | MATCH BOX | `PKT` | ₹210.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04204` | 126- BIG NAGGOLI ANA-CONDA(100X1= 1 BOX | SERPANTS & NAGGOLI | `BOX` | ₹70.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04205` | 127- JEE BOOM BAA SQUARE LAKSHMI | SERPANTS & NAGGOLI | `BOX` | ₹62.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04206` | 128- JEE BOOM BAA HEXA GLITERING LAKSHMI | SERPANTS & NAGGOLI | `BOX` | ₹65.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04207` | 189- 7 CM COL GOLD S.T.D(10DABBI=1BOX) | 9 CM SPARKLERS | `BOX` | ₹150.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04224` | 201- 50 CM COL PIPE SARAVANA ( 1 P ) | SARAVANA SPARKLERS | `PKT` | ₹135.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04225` | 202- 50 CM MULTIMIX PIPE SARAVANA ( 1 P | SARAVANA SPARKLERS | `PKT` | ₹140.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04226` | 203- 75 CM PLAIN PIPE SARAVANA ( 1 P ) | SARAVANA SPARKLERS | `PKT` | ₹150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04227` | 204- 75 CM COL PIPE SARAVANA ( 1 P ) | SARAVANA SPARKLERS | `PKT` | ₹165.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04228` | 205- 75 CM MULTIMIX PIPE SARAVANA ( 1 P | SARAVANA SPARKLERS | `PKT` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04231` | 208- 11 CM PLAIN SHRIBABA CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹9.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04232` | 209- 10 CM COL CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹13.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04233` | 210- 12 CM PLAIN CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹22.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04234` | 211- 12 CM COL CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹23.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04235` | 212- 12 CM  50 X 50 CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹23.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04236` | 213- 12 CM 5 IN 1 (5 PKT) CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04237` | 214- 15 CM PLAIN CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹32.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04238` | 215- 15 CM COL CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹33.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04239` | 216- 15 CM  50 X 50 (5 PCS)CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹35.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04240` | 217- 15 CM 2 IN 1 CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹35.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04241` | 218- 30 CM PLAIN CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹32.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04242` | 219- 30 CM COL CHANDRA | SARAVANA SPARKLERS | `PKT` | ₹33.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04246` | 251- 30 CM COL AB MAGIC CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹25.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04247` | 252- 30 CM COL DLX CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹27.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04248` | 253- 30 CM COL BOXE(2P CELLEPHON CLASSIC | CLASSIC SPARKLERS | `PKT` | ₹29.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04249` | 254- 30 CM GREEN CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹23.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04251` | 256- 30 CM RED CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹27.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04253` | 258- 30 CM 2 IN 1 CLASSIC (5 P) | CLASSIC SPARKLERS | `PKT` | ₹27.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04254` | 259- 30 CM 2 IN 1 BOXE(2P CELLEPHO CLASS | CLASSIC SPARKLERS | `PKT` | ₹29.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04255` | 260- 30 CM  MLLENIUM MIX CLASSIC(10X1BOX | CLASSIC SPARKLERS | `PKT` | ₹200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04256` | 261- 40 CM STAR CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04257` | 262- 40 CM FISH CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04258` | 263- 40 CM LAMP  CLASSIC( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04259` | 264- 40 CM X-MAS CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04260` | 265- 50 CM PLAIN SPL CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹92.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04261` | 266- 50 CM COL SPL CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04262` | 267- 50 CM PLAIN PIPE CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹92.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04263` | 268- 50 CM COL PIPE CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04264` | 269- 100 CM PLAIN SPL CLASSIC  ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04265` | 270- 100 CM COL SPL CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04266` | 271- 100 CM PLAIN PIPE CLASSIC( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04267` | 272- 100 CM COL PIPE CLASSIC ( 1 P ) | CLASSIC SPARKLERS | `PKT` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04301` | 159- STRIPPED BIJALI MERCURY(50PCS)10BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹25.50 | 10 | **10** | `APPROVED` | `override` |
| `04302` | 160- STRIPPED BIJALI ROSE(100PCS)10BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹21.50 | 10 | **10** | `APPROVED` | `override` |
| `04303` | 161- STRIPPED BIJALI AYYANAR(100PCS)10BA | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹32.00 | 10 | **10** | `APPROVED` | `override` |
| `04305` | 163- STRIPPED BIJALI GAINT S.T.D(100PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹50.00 | 10 | **10** | `APPROVED` | `override` |
| `04306` | 164- STRIPPED BIJALI S.T.D(100PCS)10 | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹60.00 | 10 | **10** | `APPROVED` | `override` |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹11.00 | 50 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04310` | 168- GOLD BIJALI COCK (50 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹35.50 | 50 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04311` | 169- GOLD BIJALI OTHER (100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹20.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹21.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04313` | 171- GOLD BIJALI GIANT OVEEYA(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹44.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04314` | 172- GOLD BIJALI APPLE(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹27.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04315` | 173- GOLD BIJALI SRIPATHI(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹30.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04316` | 174- GOLD BIJALI AYYANAR(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹37.50 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04317` | 175- GOLD BIJALI COCK(100 PCS ) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹67.00 | 100 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04318` | 176- BASKET BOMB SINGADA RAVINDRA(10 BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹62.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04341` | 296- 28 CHORSA TURKEY  RAJLAXMI(50P= 1 B | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹13.50 | 50 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04342` | 297- 28 CHORSA (25PCS) VELVAN | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹14.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04343` | 298- 32 CHORSA MIX RED-GOA SUN(50P=1BUND | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹12.50 | 50 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04346` | 301- 28 GAINT CHORSA (25 P) K.R.K | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹17.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04347` | 302- 28 GAINT CHORSA (25 P) AJITKUMAR | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹18.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04348` | 303- 28 GAINT CHORSA (25 P) SELVI | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹19.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04349` | 304- 28 GAINT CHORSA (25 P)DURGESH | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹19.50 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04350` | 305- 28 SUP GAINT CHORSA N.M.JYOTHI(25P) | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹24.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04351` | 316- 50 DLX RAGURAM ( 5 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹52.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04352` | 317- 50 DLX GANESH DURAI( 5 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹80.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04353` | 318- 100 DLX GANESH DURAI( 1 P) | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹160.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04356` | 321- 4' 24 DLX THE WASP BALAJI | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹70.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04357` | 322- 4' 32 DLX THE G ROOT BALAJI | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹93.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04358` | 323- 4' 40 DLX DOCTER STRANGE BALAJI | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹115.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04359` | 324- 4' 50 DLX THE MARVEL BALAJI | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹145.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04360` | 325- 4' 80 DLX GUARDIANS OF GALAXY BALAJ | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹240.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04361` | 326- 4' 100 DLX LOVE AND THUNDER BALAJI | 2 3/4 , 4' DELUXE PATALA | `PKT` | ₹300.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04370` | 342- 3 1/2 GREEN PARROT W/F VELVAN (10 P | ONE SOUND DHAMAKA | `PKT` | ₹15.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04371` | 343- 3 1/2  PEACOCK 9 CM  S.T.D( 10 P | ONE SOUND DHAMAKA | `PKT` | ₹24.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04372` | 344- 3 1/2 DLX KURVI GANESH (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹25.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04373` | 345- 3 1/2 GREEN PARROT W/F B.F.W (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹25.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04374` | 346- 3 1/2 JAWAN AYYAN (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹27.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04377` | 349- 4  MIX LABEL DURGESH (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹14.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04378` | 350- 4 GREEN PARROT SADA VELAVAN(10 PCS) | ONE SOUND DHAMAKA | `PKT` | ₹14.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04379` | 351- 4 GREEN PARROT SRIPATHI (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹16.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04380` | 352- 4  LADY T/MEENA  (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹16.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04381` | 353- 4 MICKEY MOUSE BALAJI( 10 P) | ONE SOUND DHAMAKA | `PKT` | ₹16.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04382` | 354- 4 GREEN PARROT VELAVAN (10 P) W/F | ONE SOUND DHAMAKA | `PKT` | ₹18.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04383` | 355- 4 ELEPHANT I.N (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹18.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04384` | 356- 4 GREEN PARROT SADA PONMALAR(10P) | ONE SOUND DHAMAKA | `PKT` | ₹19.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04385` | 357- 4  MIX LABEL AYYANAR (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹21.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04386` | 358- 4 PARROT COCK (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹22.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04387` | 359- 4 GREEN PARROT W/F V.F.I(10 P) | ONE SOUND DHAMAKA | `PKT` | ₹32.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04388` | 360- 4 KING AYYAN (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹32.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04389` | 361- 10 CM PEACOCK COLF S.T.D( 10 P) | ONE SOUND DHAMAKA | `PKT` | ₹34.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04390` | 362- 4 GREEN PARROT W/F B.F.W (10 P) | ONE SOUND DHAMAKA | `PKT` | ₹35.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04393` | 365- 4 DLX DHAMAKA OTHER | ONE SOUND DHAMAKA | `PKT` | ₹21.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04394` | 366- 4 DLX HULK JAYMURGAN | ONE SOUND DHAMAKA | `PKT` | ₹22.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04395` | 367- 4 DLX ELEPHANT I.N | ONE SOUND DHAMAKA | `PKT` | ₹23.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04396` | 368- 4 DLX PARROT SADA VELAVAN | ONE SOUND DHAMAKA | `PKT` | ₹26.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04397` | 369- 4 DLX TIGER (12 PLY)BALAJI | ONE SOUND DHAMAKA | `PKT` | ₹26.50 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04398` | 370- 4 DLX GREEN PARROT SADA PONMALAR | ONE SOUND DHAMAKA | `PKT` | ₹27.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04399` | 371- 4 DLX  DRAGON(10 PLY)AMBIKA | ONE SOUND DHAMAKA | `PKT` | ₹28.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04400` | 372- 4 DLX PARROT W/F ( 10 P)VELAVAN | ONE SOUND DHAMAKA | `PKT` | ₹29.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04401` | 373- 4 DLX MIX LABLE W/F (12 PLY)S.K.M | ONE SOUND DHAMAKA | `PKT` | ₹35.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04405` | 377- 4 SUP DLX MIX LABEL(10P)AYYANAR | ONE SOUND DHAMAKA | `PKT` | ₹27.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04406` | 378- 4 SUP DLX GREEN PARROT SADA PONMALA | ONE SOUND DHAMAKA | `PKT` | ₹30.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04407` | 379- 4 SUP DLX GREEN PARROT W/F V.F.I(10 | ONE SOUND DHAMAKA | `PKT` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04408` | 380- 4 SUP DLX GREEN PARROT W/F B.F.W(10 | ONE SOUND DHAMAKA | `PKT` | ₹45.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04409` | 381- 4 SUP DLX GREEN PARROT W/F AYYAN(10 | ONE SOUND DHAMAKA | `PKT` | ₹58.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04411` | 383- 5 DLX JALLIKATTI DURGESH (10P) | ONE SOUND DHAMAKA | `PKT` | ₹27.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04412` | 384- 5 DLX MOTTA CARCKERS COCK | ONE SOUND DHAMAKA | `PKT` | ₹30.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04413` | 385- 5 DLX  ELEPHANT(10P) JAYMURGAN | ONE SOUND DHAMAKA | `PKT` | ₹31.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04414` | 386- 5 DLX  W/F ( 12 PLY ) S.K.M | ONE SOUND DHAMAKA | `PKT` | ₹32.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04415` | 387- 5 DLX WARRIOR BALAJI | ONE SOUND DHAMAKA | `PKT` | ₹33.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04416` | 388- 6 DLX SPIDERMAN PADMA PRIYA | ONE SOUND DHAMAKA | `PKT` | ₹33.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04417` | 389- 6 DLX ARABIAN BALAJI | ONE SOUND DHAMAKA | `PKT` | ₹46.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04418` | 390- 6 DLX ( 12 PLY ) S.K.M | ONE SOUND DHAMAKA | `PKT` | ₹46.50 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04419` | 391- 5 DLX  (10P) ( 12 PLY ) S.NARAYANA | ONE SOUND DHAMAKA | `PKT` | ₹30.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04420` | 392- 6 DLX  (10P) ( 12 PLY ) S.NARAYANA | ONE SOUND DHAMAKA | `PKT` | ₹38.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04421` | 393- 4 DLX GOLD CHOTA BHEAM JAYMURGAN | ONE SOUND DHAMAKA | `PKT` | ₹21.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04422` | 394- 4 DLX GOLD TIGER SRIPATHI | ONE SOUND DHAMAKA | `PKT` | ₹25.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04423` | 395- 4 SUP DLX GOLD KARUDA (10P) AYYANAR | ONE SOUND DHAMAKA | `PKT` | ₹35.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04424` | 396- 4 SUP DLX GOLD ELEPHANT (10P)I.N | ONE SOUND DHAMAKA | `PKT` | ₹57.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04428` | 403- 2 SOUND DHAMAKA ANIL (10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹32.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04429` | 404- 2 SOUND DHAMAKA S.T.D (10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹36.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04430` | 405- 2 SOUND DHAMAKA MERCURY (10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹42.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04433` | 408- 3 SOUND DHAMAKA NM JYOTHI(10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹28.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04434` | 409- 3 SOUND DHAMAKA RATHANAA(10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹34.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04435` | 410- 3 SOUND DHAMAKA I.N. (10P) | TWO & THREE SOUND DHAMAKA | `PKT` | ₹40.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04460` | 452- FLOWER POTS BIG T/MEENA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹55.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04461` | 453- FLOWER POTS BIG AYYANAR | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹68.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04462` | 454- FLOWER POTS BIG OVEEYA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹78.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04463` | 455- FLOWER POTS BIG MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹80.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04464` | 456- FLOWER POTS BIG COCK | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹124.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04465` | 457- FLOWER POTS BIG S.T.D | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹135.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04468` | 460- FLOWER POTS SPECIAL G.P.M | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹45.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04469` | 461- FLOWER POTS SPECIAL K.V.S | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹45.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04470` | 462- FLOWER POTS SPECIAL SRI SAI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹50.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04471` | 463- FLOWER POTS SPECIAL NM JYOTHI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹60.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04472` | 464- FLOWER POTS SPECIAL ANBARSI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹60.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04473` | 465- FLOWER POTS SPECIAL T/MEENA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹65.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04474` | 466- FLOWER POTS SPECIAL AYYANAR | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹102.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04475` | 467- FLOWER POTS SPECIAL OVEEYA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹105.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04476` | 468- FLOWER POTS SPECIAL MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹106.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04477` | 469- FLOWER POTS SPECIAL I.N | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹110.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04478` | 470- FLOWER POTS SPECIAL S.T.D | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹180.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04479` | 471- FLOWER POTS SPECIAL COCK | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹220.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04482` | 474- FLOWER POTS ASHOKA K.V.S | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹55.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04483` | 475- FLOWER POTS ASHOKA SRI SAI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹62.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04484` | 476- FLOWER POTS ASHOKA ANBARSI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹69.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04485` | 477- FLOWER POTS ASHOKA NM JYOTHI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹70.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04486` | 478- FLOWER POTS ASHOKA T/MEENA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹83.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04487` | 479- FLOWER POTS ASHOKA SRIPATHI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹85.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04488` | 480- FLOWER POTS ASHOKA OVEEYA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹140.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04489` | 481- FLOWER POTS ASHOKA MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04493` | 485- FLOWER POTS GAINT AYYANAR | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04494` | 486- FLOWER POTS GAINT I. N. | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹155.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04495` | 487- FLOWER POTS GAINT MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹202.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04496` | 488- FLOWER POTS GAINT COL.KOTI MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹250.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04497` | 489- FLOWER POTS GAINT S.T.D | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹325.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04499` | 491- FLOWER POTS COL KOTI UV.BOX OTHER | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹110.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04500` | 492- FLOWER POTS COL KOTI UV.BOX ROJAPOO | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹135.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04501` | 493- FLOWER POTS COL KOTI UV.BOX RAJLAXM | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹140.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04502` | 494- FLOWER POTS COL KOTI UV.BOX T/MEENA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04503` | 495- FLOWER POTS COL KOTI UV.BOX GOVINDA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹165.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04504` | 496- FLOWER POTS COL KOTI AYYANAR | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04507` | 499- F. POTS COL KOTI DLX LONG ATHISAYA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹155.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04508` | 500- FLOWER POTS DLX (10 P) OVEEYA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹150.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04509` | 501- FLOWER POTS DLX (10 P) GOVINDA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹245.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04510` | 502- FLOWER POTS COL KOTI DLX(10P)ANIL | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹375.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04511` | 503- FLOWER POTS DLX COL KOTI(10P)SONNY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹350.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04512` | 504- FLOWER POTS DLX COL KOTI (10 P)I.N | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹355.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04513` | 505- FLOWER POTS MEGA DLX (10 P)MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹290.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04514` | 506- F P MEGA DLX  (10 P) VIRABALAJI | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹420.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04515` | 507- F P MEGA DLX GREEN BERRY(1P)SONNY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04518` | 510- FLOWER POT DLX (5 PCS )GOVINDA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04519` | 511- FLOWER POT DLX (5 PCS )MERCURY | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹175.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04520` | 512- FLOWER POT DLX (5 PCS )S.T.D | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹240.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04563` | 563- OMG POTS ANAR MERCURY ( 5 PCS ) | FANCY MATAKA ANAR | `BOX` | ₹315.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04564` | 564- CROWN JEWEL'S ANAR MERCURY( 5 PCS) | FANCY MATAKA ANAR | `BOX` | ₹625.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04565` | 565- CELEBRATION PACK ANAR MERCURY(4 | FANCY MATAKA ANAR | `BOX` | ₹825.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04574` | 615- G C SPL (10 P) (5 P) S.T.D | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹150.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04576` | 617- G C SPL SPINNER WHEEL(10P) AYYANAR | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹75.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04577` | 618- G C SPL SPINNER WHEEL YASO | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹90.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04578` | 619- HOT WHEEL SPL I.N | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹106.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04580` | 621- G C DLX  (10 P) 5 P VENKATESH | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹75.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04581` | 622- G C DLX  (10 P) 5 P T/MEENA | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹95.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04583` | 624- G C DLX  (10 P) 5 P MERCURY | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹125.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04584` | 625- G C DLX  (10 P) 5 P COLOUR W JENIS | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹115.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04585` | 626- G C DLX  W (10 P) 5 P I.N | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹130.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04586` | 627- G C DLX  (10 P) 5 P GANESH | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹140.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04587` | 628- G C DLX  (10 P) 5 P ANIL | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹160.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04588` | 629- G C DLX  (10 P) 5 P SUNSHINE | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹165.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04589` | 630- G C DLX  (10 P) 5 P S.T.D | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹195.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04590` | 631- 70 CM G C DLX  (10 P) 5 P COCK | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹210.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04592` | 633- G C DLX  U.V. BOX (10 P) 5 P I.N | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹135.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04593` | 634- G C DLX  PLASTIC (10 P) 5 P JAGUAR | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹110.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04594` | 635- G C DLX  SPINNER WHEEL YASO | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹110.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04595` | 636- G C DLX SPINNER ( 10 P )AYYANAR | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹160.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04596` | 637- G C DLX  SPINNER(10P) 5P CORONATION | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹175.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04600` | 641- G C SUP DLX  (10 P) 5 P MERCURY | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹190.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04601` | 642- G C SUP DLX  (10 P) 5 P S.T.D | GROUND CHAKKAR BIG,ASHOKA,SPL,DLX,SUP DL | `PKT` | ₹215.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04613` | 650- SUDARSHAN CHAKKAR ANIL ( 6 P) 1P | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹153.00 | 1 | **1** | `APPROVED` | `override` |
| `04614` | 651- TWIN SPIN S.T.D(5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹94.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04615` | 652- MASKA CHASKA I. N ( 5 P ) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04616` | 653- GIANT WHEEL AYYAN (5 PCS) (1P) BIG | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹175.00 | 1 | **1** | `APPROVED` | `override` |
| `04617` | 654- LOTUS WHEEL M.K.R. (5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹170.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04618` | 655- MUSICAL WHEEL MERCURY (5 PCS) ( 2 P | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹102.50 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04619` | 656- WHISTLING WHEEL COCK (5 PCS) (10P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹125.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04620` | 657- WHIZZ WHEEL S.T.D (5 PCS) (10P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹139.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04621` | 658- TITANIC WHEEL DURGESH ( 5P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹130.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04622` | 659- TOP TUCKER AYYAN ( 5 P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹80.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04623` | 660- MANORANJAN CHAKAR WITH-FLOW ANIL | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹265.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04624` | 661- SWASTIK WHEEL S.T.D (5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹285.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04625` | 662- SKY  WHEEL AYYAN (5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹345.00 | 1 | **1** | `APPROVED` | `override` |
| `04626` | 663- SPINNER BAMBARA LAVANYA ( 10 P ) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹85.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04627` | 664- LOTUS WHEEL (5 PCS) AYYAN | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04628` | 665- STAR WHEEL (10 PCS) AYYAN | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹156.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04634` | 673- ROCKET BOMB (10P) 5P S.T.D | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹144.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04636` | 675- SILVER ROCKET(10P)5P AYYANAR | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹75.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04638` | 677- LUNIK ROCKET(NO SOUND )GURU JYOTHI | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹70.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04639` | 678- LUNIK ROCKET (10 P) 2P T/MEENA | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹80.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04640` | 679- EXPO ROCKET (10 P) 2P GANESH | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹85.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04641` | 680- LUNIK ROCKET (10 P) 2P MERCURY | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹112.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04643` | 682- LUNIK ROCKET (10 P) 2P AYYANAR | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹130.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04645` | 684- 2 SOUND ROCKET(NO SOUND GURU JYOTHI | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹72.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04646` | 685- 2 SOUND ROCKET (10 P) 2P T/MEENA | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹82.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04647` | 686- 2 SOUND ROCKET (10 P) 2P AYYANAR | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹120.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04649` | 688- 2 SOUND ROCKET (10 P) 2P GANESH | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹125.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04650` | 689- 2 SOUND ROCKET (10 P) 2P MERCURY | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹132.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04665` | 717- JIL JIL 1X10 PEC=1BOX COCK | TWINKLING STAR 18" & 48"&  JIL JIL | `PKT` | ₹405.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04679` | 724- 15 CM PENCIL VIRBALAJI ( 10 P ) | PENCILS & FANCY TORCHES, | `PKT` | ₹53.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04680` | 725- 18 CM PENCIL VIRBALAJI ( 10 P ) | PENCILS & FANCY TORCHES, | `PKT` | ₹68.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04683` | 728- CORONATION CANDLE B.F.W ( 10P) 1P | PENCILS & FANCY TORCHES, | `PKT` | ₹95.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04684` | 729- MULTI COLOUR CANDLE S.T.D (10P) 5P | PENCILS & FANCY TORCHES, | `PKT` | ₹99.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04685` | 730- WHISTLING PIPER SONY ( 5 P ) | PENCILS & FANCY TORCHES, | `PKT` | ₹285.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04686` | 731- CHENDA MELAM AYYAN( 2 P) 1 P | PENCILS & FANCY TORCHES, | `PKT` | ₹245.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04687` | 732- HAND SHOWER MARIESWARAN ( 3 P ) | PENCILS & FANCY TORCHES, | `PKT` | ₹185.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04688` | 733- SUPERB TORCH  2 PCS)I.N | PENCILS & FANCY TORCHES, | `PKT` | ₹175.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04772` | 863- 12 SHOTS M.COL U.V.SQ. STAR GALAXY | SHOTS & MULTISHOTS | `BOX` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04773` | 864- 12 SHOTS M.COL BIG BOX SQ KINGSTARS | SHOTS & MULTISHOTS | `BOX` | ₹165.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04774` | 865- 12 SHOTS M.COL HEXA KINGSTARS | SHOTS & MULTISHOTS | `BOX` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04778` | 869- 15 SHOTS M. COL. LONG GURUVI | SHOTS & MULTISHOTS | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04779` | 870- 15 SHOTS M.COL. LONG U.V.BOX BALAJI | SHOTS & MULTISHOTS | `BOX` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04780` | 871- 15 SHOTS M.COL. LONG U.V.BOX V.G.M | SHOTS & MULTISHOTS | `BOX` | ₹245.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04781` | 872- 16 SHOTS M.COL. LONG TEMPLE RUN | SHOTS & MULTISHOTS | `BOX` | ₹550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04782` | 873- 16 SHOT R/G MINES SUN | SHOTS & MULTISHOTS | `BOX` | ₹290.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04783` | 874- 20 SHOTS M. COL.JOLLY JINGLE COCK | SHOTS & MULTISHOTS | `BOX` | ₹275.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04785` | 876- 25 SHOTS SQUARE(AI) KINGSTARS | SHOTS & MULTISHOTS | `BOX` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04786` | 877- 25 SHOTS SQUARE U.V.BOX APPLE | SHOTS & MULTISHOTS | `BOX` | ₹190.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04787` | 878- 25 SHOTS  LONG U.V.BOX BALAJI | SHOTS & MULTISHOTS | `BOX` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04788` | 879- 25 SHOTS  LONG DREAM BLAST GEMINI | SHOTS & MULTISHOTS | `BOX` | ₹180.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04790` | 881- 25 SHOTS M.COL LITTLE BEES SQ COCK | SHOTS & MULTISHOTS | `BOX` | ₹335.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04791` | 882- 25 SHOTS M.COL MAN PASAND SQ ANIL | SHOTS & MULTISHOTS | `BOX` | ₹445.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04793` | 884- 25 SHOTS LONG BOX M. COL KINGSTARS | SHOTS & MULTISHOTS | `BOX` | ₹320.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04795` | 886- 25 SHOTS LONG BOX M.COL ANTHEM ANIL | SHOTS & MULTISHOTS | `BOX` | ₹573.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04796` | 887- 25 SHOTS LONG BOX M.COL MIX MERCURY | SHOTS & MULTISHOTS | `BOX` | ₹560.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04797` | 888- 25 SHOTS LONG BOX LION KING SONY | SHOTS & MULTISHOTS | `BOX` | ₹530.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04798` | 889- 25 SHOTS LONG BOX TROY SONY | SHOTS & MULTISHOTS | `BOX` | ₹530.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04800` | 891- 30 SHOTS M. COL.U.V.BOX 3MIX VELVAN | SHOTS & MULTISHOTS | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04801` | 892- 30 SHOTS M. COL. GURU | SHOTS & MULTISHOTS | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04802` | 893- 30 SHOTS M. COL. U V BOX ELITE | SHOTS & MULTISHOTS | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04803` | 894- 30 SHOTS M.COL. U V BOX VETRIVELVAN | SHOTS & MULTISHOTS | `BOX` | ₹375.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04804` | 895- 30 SHOTS M. COL. U V BOX R. G. | SHOTS & MULTISHOTS | `BOX` | ₹375.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04805` | 896- 30 SHOTS M. COL. U V BOX V. G. M. | SHOTS & MULTISHOTS | `BOX` | ₹380.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04806` | 897- 30 SHOTS M. COL. LAZER VEERA | SHOTS & MULTISHOTS | `BOX` | ₹390.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04807` | 898- 30 SHOTS M. COL. DRAGON SURIYAN | SHOTS & MULTISHOTS | `BOX` | ₹400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04808` | 899- 30 SHOTS M. COL. AYYANAR | SHOTS & MULTISHOTS | `BOX` | ₹420.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04810` | 901- 30 SHOTS M. COL. + CRACKLING THIRU | SHOTS & MULTISHOTS | `BOX` | ₹420.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04811` | 902- 30 SHOTS M. COL. COCK | SHOTS & MULTISHOTS | `BOX` | ₹640.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04812` | 903- 30 SHOTS M. COL. MERCURY | SHOTS & MULTISHOTS | `BOX` | ₹650.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04813` | 904- 30 SHOTS M. COL. S. T. D. | SHOTS & MULTISHOTS | `BOX` | ₹775.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04814` | 905- 30 SHOTS 2 COLOUR S.R.R. | SHOTS & MULTISHOTS | `BOX` | ₹320.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04817` | 908- 50 SHOTS M. COL. SQUARE WINSTAR | SHOTS & MULTISHOTS | `BOX` | ₹330.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04819` | 910- 50 SHOTS LONG DISCO SAJ | SHOTS & MULTISHOTS | `BOX` | ₹325.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04820` | 911- 50 SHOT LONG WINSTAR | SHOTS & MULTISHOTS | `BOX` | ₹375.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04824` | 915- 50 SHOTS M.COL.SQ. DIL KHUSH ANIL | SHOTS & MULTISHOTS | `BOX` | ₹890.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04825` | 916- 50 SHOTS LONG SHADES OF FREED ANIL | SHOTS & MULTISHOTS | `BOX` | ₹1020.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04826` | 917- 50 SHOTS M.COL. LONG 3MIX LABE SONY | SHOTS & MULTISHOTS | `BOX` | ₹1170.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04828` | 919- 60 SHOTS M. COL PENCIL | SHOTS & MULTISHOTS | `BOX` | ₹680.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04829` | 920- 60 SHOTS M. COL U.V. BOX BALAJI | SHOTS & MULTISHOTS | `BOX` | ₹690.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04830` | 921- 60 SHOTS M. COL U.V. BOX VELVAN | SHOTS & MULTISHOTS | `BOX` | ₹700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04831` | 922- 60 SHOTS M. COL U.V. BOX GURU JYOTH | SHOTS & MULTISHOTS | `BOX` | ₹720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04832` | 923- 60 SHOTS M. COL U.V. BOX R. G | SHOTS & MULTISHOTS | `BOX` | ₹750.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04833` | 924- 60 SHOTS M. COL U.V. BOX VETRIVELVA | SHOTS & MULTISHOTS | `BOX` | ₹740.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04834` | 925- 60 SHOTS M. COL U.V. BOX V.G.M | SHOTS & MULTISHOTS | `BOX` | ₹760.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04835` | 926- 60 SHOTS M. COL SURIYAN | SHOTS & MULTISHOTS | `BOX` | ₹800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04836` | 927- 60 SHOTS M. COL AYYANAR | SHOTS & MULTISHOTS | `BOX` | ₹840.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04837` | 928- 60 SHOTS M. COL + CRACKLING THIRU | SHOTS & MULTISHOTS | `BOX` | ₹840.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04838` | 929- 60 SHOTS M. COL MERCURY | SHOTS & MULTISHOTS | `BOX` | ₹1140.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04839` | 930- 60 SHOTS M. COL COCK | SHOTS & MULTISHOTS | `BOX` | ₹1150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04840` | 931- 60 SHOTS M. COL MIX -3 SELLS S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹1275.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04841` | 932- 60 SHOTS M. COL 30-30 LONG ANIL | SHOTS & MULTISHOTS | `BOX` | ₹1230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04842` | 933- 60 SHOTS M. COL U.V. BOX N.S.V. | SHOTS & MULTISHOTS | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04846` | 937- 80 SHOTS 3 COL. SQUARE S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹1700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04847` | 938- 80 SHOTS M. COL. SUNSHINE | SHOTS & MULTISHOTS | `BOX` | ₹1520.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04848` | 939- 100 SHOT CRACKLING LONG SAJ | SHOTS & MULTISHOTS | `BOX` | ₹700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04850` | 941- 100 SHOT M. COL. U.V. BOX VELVAN | SHOTS & MULTISHOTS | `BOX` | ₹1200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04851` | 942- 100 SHOT M. COL. U.V. BOX V.G.M | SHOTS & MULTISHOTS | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04852` | 943- 100 SHOT M.COL. U.V.BOX VETRIVELVAN | SHOTS & MULTISHOTS | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04853` | 944- 100 SHOT M. COL. ANIL | SHOTS & MULTISHOTS | `BOX` | ₹1700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04854` | 945- 100 SHOTS M. COL. MERCURY | SHOTS & MULTISHOTS | `BOX` | ₹1760.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04855` | 946- 100 SHOTS M. COL. S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹1860.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04856` | 947- 100 SHOTS M. COL. SUNSHINE | SHOTS & MULTISHOTS | `BOX` | ₹1900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04857` | 948- 100 SHOTS 1 1/4 PIPE SAGUN MORI | SHOTS & MULTISHOTS | `BOX` | ₹2150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04858` | 949- 100 SHOTS SIREN SINGING BIRDS S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹2200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04859` | 950- 100 SHOT M.COL. LONG U.V.BOX N.S.V | SHOTS & MULTISHOTS | `BOX` | ₹1600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04862` | 953- 120 SHOTS M. COL U.V.BOX VELVAN | SHOTS & MULTISHOTS | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04863` | 954- 120 SHOTS M. COL PENCIL | SHOTS & MULTISHOTS | `BOX` | ₹1360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04864` | 955- 120 SHOTS M. COL VETRIVELVAN | SHOTS & MULTISHOTS | `BOX` | ₹1500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04865` | 956- 120 SHOTS M. COL R.G. | SHOTS & MULTISHOTS | `BOX` | ₹1500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04866` | 957- 120 SHOTS M. COL SURIYAN | SHOTS & MULTISHOTS | `BOX` | ₹1600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04867` | 958- 120 SHOTS M. COL V.G.M | SHOTS & MULTISHOTS | `BOX` | ₹1520.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04868` | 959- 120 SHOTS M. COL AYYANAR | SHOTS & MULTISHOTS | `BOX` | ₹1680.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04869` | 960- 120 SHOTS M. COL + CRACKLING THIRU | SHOTS & MULTISHOTS | `BOX` | ₹1680.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04870` | 961- 120 SHOTS M. COL  MIXED S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹2160.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04871` | 962- 120 SHOTS ENJOY FUN ANIL | SHOTS & MULTISHOTS | `BOX` | ₹2200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04872` | 963- 120 SHOTS STAR SHOW SUNSHINE | SHOTS & MULTISHOTS | `BOX` | ₹2300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04873` | 964- 120 SHOTS RANG DE BASANTI I.N | SHOTS & MULTISHOTS | `BOX` | ₹2600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04874` | 965- 120 SHOTS TRANSFORMER I.N | SHOTS & MULTISHOTS | `BOX` | ₹2780.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04877` | 968- 160 SHOTS ROAD SHOW SUNSHINE | SHOTS & MULTISHOTS | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04878` | 969- 200 SHOTS M. COL N.S.V. | SHOTS & MULTISHOTS | `BOX` | ₹3350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04880` | 971- 240 SHOTS M. COL PENCIL | SHOTS & MULTISHOTS | `BOX` | ₹2720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04881` | 972- 240 SHOTS M.COL U.V.BOX GURU JYOTHI | SHOTS & MULTISHOTS | `BOX` | ₹2880.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04882` | 973- 240 SHOTS M. COL V.G.M | SHOTS & MULTISHOTS | `BOX` | ₹3040.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04883` | 974- 240 SHOTS M. COL AYYANAR | SHOTS & MULTISHOTS | `BOX` | ₹3360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04884` | 975- 240 SHOTS M. COL COCK | SHOTS & MULTISHOTS | `BOX` | ₹4300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04885` | 976- 240 SHOTS M. COL BADIYA HAI ANIL | SHOTS & MULTISHOTS | `BOX` | ₹4300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04886` | 977- 240 SHOTS M. COL HOODI BABA ANIL | SHOTS & MULTISHOTS | `BOX` | ₹4500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04887` | 978- 240 SHOTS ROMANCE I.N | SHOTS & MULTISHOTS | `BOX` | ₹5040.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04888` | 979- 240 SHOTS RAINBOW DANCE S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹5300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04889` | 980- 240 SHOTS CLASSIC NIGHT AYYAN | SHOTS & MULTISHOTS | `BOX` | ₹5500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04890` | 981- 240 SHOTS ENJOY I.N | SHOTS & MULTISHOTS | `BOX` | ₹5550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04891` | 982- 240 SHOTS ARABIAN DELIGHT AYYAN | SHOTS & MULTISHOTS | `BOX` | ₹6150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04892` | 983- 250 SHOTS PARADISE S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹5200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04895` | 986- 500 SHOTS M. COL MERCURY | SHOTS & MULTISHOTS | `BOX` | ₹8500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04896` | 987- 500 SHOTS M. COL I. N. | SHOTS & MULTISHOTS | `BOX` | ₹10050.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04897` | 988- 500 SHOTS M. COL S.T.D | SHOTS & MULTISHOTS | `BOX` | ₹11700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04898` | 996- 10 X 30 VOLCANO SONNY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹2250.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04899` | 997- 100 SHOT'S 10X10 SIZZLING LIYA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04900` | 998- 100 SHOT'S 10X10 PEACOCK LIYA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04901` | 999- 100 SHOT'S 10X10 TAIL LIGHT LIYA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04902` | 1000- 100 SHOT'S 10X10 THUNDER LIYA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹4500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04903` | 1001- 100 SHOT'S 10X10 TAIL LIGHT CHOLA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04904` | 1002- 100 SHOT'S 10X10 FAN CAKE SONY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹4000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04905` | 1003- 100 SHOT'S 10X10 NIGHT RIDER AYYAN | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04906` | 1004- 24 SHOT 3" PIPE OSCAR I. N. | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹8800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04907` | 1005- 50 SHOT 5X10 PENDULUM RAIDER I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04908` | 1006- 50 SHOT 5 X 10 TWISTER I. N. | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹5500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04909` | 1007- 70 SHOT 7 X 10 DIGITAL RAIN I. N. | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04910` | 1008- 18 HAND SHOT ( 2 PCS ) M.INDIA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹400.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04911` | 1009- 288 HAND SHOT M.INDIA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04912` | 1010- 888 HAND SHOT M.INDIA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹3200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04914` | 1012- 5 KA DHUM ( 5 P) ANIL | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹155.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04915` | 1013- SKY SHOT (10 P ) COCK | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹86.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04916` | 1014- PENTA SKY COCK | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹165.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04917` | 1015- CHHOTA FANCY 5 IN 1 I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹270.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04918` | 1016- TOP-TEN ( 10 P ) COCK | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹350.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04919` | 1017- 1 3/4 FANCY PIPE 5 MIX COL SHREEHA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹29.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04920` | 1018- 1 3/4 FANC PIPE SUP.STAR 5COL STD | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹60.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04921` | 1019- 2 1/2 F. P. MIX COL(1P)TERKHADA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹55.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04922` | 1020- 2 1/2 F. P. MIX COL UV.BOX | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹75.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04923` | 1021- 2 1/2 F. P. 5COL UV.BOX BALAJI | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹75.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `04924` | 1022- 2 1/2 F. P. (3P)6COL MIX W THUNIVU | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹175.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04925` | 1023- 2 1/2 F. P. (3P)6COL MIX U BALAJI | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹180.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04926` | 1024- 2 1/2 F. P. (2P)6COL MIX U | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹190.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04927` | 1025- 2 1/2 F. P. (3PCS) MIX COL AYYANAR | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹225.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04928` | 1026- 3 FANCY PIPE (2 PCS) SONY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹850.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04929` | 1027- 2 1/2 F. P. (3P)MIX COL 7 STEP I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹500.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04930` | 1028- 2 1/2 F. P. (3P)3 IN 1 BLOSSOM COC | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹422.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04931` | 1029- PARACHUTE NIGHTOUT ( 3 P ) COCK | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹400.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04932` | 1030- 2 1/2 F. P.LONG(3P)MIX COL.MERCURY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹455.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04933` | 1031- 2 FANCY PIPE 2 COLOUR S.R.R | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹46.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `04935` | 1033- 3  FANCY PIPE (1P) 2 COLOUR S.R.R | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04936` | 1034- 3  FANCY PIPE (1P) MIX COL | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04937` | 1035- 3  FANCY PIPE (1P) UV BOX BALAJI | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹220.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04938` | 1036- 3  FANCY PIPE (1P) MIX COL AYYANAR | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04939` | 1037- 3  FANCY PIPE (1P) 5 COL MIX I. N. | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹375.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04941` | 1039- 3  FANCY PIPE (2P) MIX COL MERCURY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹600.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04942` | 1040- 3  FANCY PIPE (3P) MIX COL MERCURY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹940.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04944` | 1042- 3 1/2 F.P.(1P)COL WITH CRAC. S.R.M | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04945` | 1043- 3 1/2 FANCY PIPE (1P) 5COL SANTOSH | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹220.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04946` | 1044- 3 1/2 FANCY PIPE (1P) 5COL JAWA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04948` | 1046- 3 1/2 F. P. YELLOW ANGEL(1P)ANIL | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹310.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04949` | 1047- 3 1/2 F. P. ITS FLYING (1P)ANIL | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹415.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04950` | 1048- 3 1/2 F. P. DOUBLE BALL (1P)S.R.M | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹340.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04952` | 1063- 15 SHOT 3 COL R.R | COLOUR DHUA | `PKT` | ₹550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `04953` | 1064- SKYDER 9 SHOT M. COL SUP.KING | COLOUR DHUA | `PKT` | ₹2000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05002` | 1113- MISSILE GUN R-751 SOM (1 PCS) | 8 SHOT'S MISSIEL GUN & FANCY GUN | `PCS` | ₹32.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05003` | 1114- HUNTER GUN WITH RING CAP AYYAN 1BO | 8 SHOT'S MISSIEL GUN & FANCY GUN | `BOX` | ₹100.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05004` | 1115- PUBG GUN ( 5 P X 1 PKT )T PANDYAN | 8 SHOT'S MISSIEL GUN & FANCY GUN | `BOX` | ₹90.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05011` | 1124- CUTTING PAPER M-COL MIX- 2KG M.IND | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹110.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05012` | 1125- CUTTING SPL,COL,RED,GREEM,YELLOW M | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05013` | 1126- CUTTING WHITE,PINK,BLUE,ORING M.IN | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05014` | 1127- CHAMKI PAPER CHAMKI WALA M.INDIA | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹140.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05015` | 1128- 2 COL MIX DILVER & GOLD M.INDIA | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹170.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05016` | 1129- CONFETTI PARER BLAST (1 P)SUP.KIN | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹125.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05017` | 1130- 1 3/4 SKY SHOT GUN WALA('KING'S 10 | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹750.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05018` | 1131- COL.IGNITOR 6COL COLD PYRO P.G.S 6 | ALL FESTIVAIS & EVENT FANCY ITEM | `KG-1` | ₹80.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05019` | 1132- GOLD PYRO BLACK RIDER BEST | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹100.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05020` | 1133- COLD PYRO BLACK R.R.R ( 10 P) | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹110.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05021` | 1134- COLD PYRO YELLO BOX TAIWIN( 10 P) | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹120.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05022` | 1135- COLD PYRO WHITE BOX RED RUSSIAN(10 | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05023` | 1136- NAAGARA FALLS ( 25 PCS) P.G | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹1200.00 | 25 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05025` | 1138- PAPER BLAST STAND | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹450.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05026` | 1139- COLD PYRO BLACK GUN PENCIL CELL | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05028` | 1140- COLD PYRO L.A.D GUN PENCIL CELL | ALL FESTIVAIS & EVENT FANCY ITEM | `BOX` | ₹200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05029` | 1141- COLD PYRO GUN CHARGING WALA | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05030` | 1142- PEPAR CUTTING BLOWER MEDIUM GUN | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹12000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05031` | 1143- PEPAR CUTTING BLOWER BIG GUN | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹12000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05032` | 1144- CUTTING PAPER BLOWER MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹9000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05033` | 1145- C.O.2 GUN | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹9000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05034` | 1146- L.E.D GUN | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹10000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05035` | 1147- 3 IN 1 GOLD PYRO GUN | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹9000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05036` | 1148- FAN WHEEL MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹7500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05037` | 1149- ZIG ZAG MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹9000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05038` | 1150- HAND FAN WHEEL MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹7700.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05039` | 1151- BUBBLE MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹1500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05040` | 1152- FOGGER MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹5200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05041` | 1153- DANCING RING MACHINE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹12000.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05042` | 1154- GOLD PYRO MACHINE 8 POINT | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹5500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05043` | 1155- GOLD PYRO MACHINE 24 POINT | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹6500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05044` | 1156- GOLD PYRO MACHINE 24 POINT | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹8500.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05045` | 1157- BALOON FUSE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹20.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05046` | 1158- PAPER BLAST FUSE | ALL FESTIVAIS & EVENT FANCY ITEM | `PCS` | ₹25.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05053` | 1161- 12 SHOT JUNGLE BOOK VELVAN (NO.G.N | NO GUARRANTY & NO WARRANTY | `PKT` | ₹70.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05054` | 1162- F. POT COL. KOTI 'MIX(NO.G.NO.W) | NO GUARRANTY & NO WARRANTY | `BOX` | ₹60.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05055` | 1163- 600 LAR COL FOG WALA (NO.G.NO.W) | NO GUARRANTY & NO WARRANTY | `PKT` | ₹50.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05166` | 1049- 3 1/2 F. P. DOUBLE BALL (1P)SILVER | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05186` | 989- 500 SHOTS M. COL AYYAN | SHOTS & MULTISHOTS | `BOX` | ₹12950.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05187` | 990- 510 SHOTS M. COL GONIN 10 ANIL | SHOTS & MULTISHOTS | `BOX` | ₹10500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05402` | 513- FLOWER POTS SUP DLX (2 P)SUPER | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹65.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05403` | 514- FLOWER POTS SUP DLX (2 P) GOVINDA | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹75.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05404` | 515- FLOWER POTS RANG BARAAT (2 P)COCK | FLOWER POTS COL KOTI, MEGA DLX, SUP DLX | `PKT` | ₹405.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05425` | 691- 3 SOUND ROCKET(NO SOUND GURU JYOTHI | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹74.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05426` | 692- 3 SOUND ROCKET (10 P) 2P T/MEENA | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹85.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05427` | 693- 3 SOUND ROCKET (10 P) 2P AYYANAR | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹135.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05428` | 694- 3 SOUND ROCKET (10 P) 2P GANESH | ROCKETS BOMB,LUNIK ROCKETS, 2 & 3 SOUND | `PKT` | ₹140.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05458` | 1050- 4"  F. P.(1P) 5 MIXED UV BOK R.S | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05459` | 1051- 4"  F. P.(2P) 3 COL. MIXED MERCURY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹860.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05460` | 1052- 4"  F. P.(2P) 8 COL MIX UV BOX I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1100.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05461` | 1053- 4"  DLX F.P.(2P) 12 COL.MIXED SONY | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹950.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05462` | 1054- 4"  F.P.(2P)DOUBLE BALL UV.BOX I.N | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹1230.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05463` | 1055- 4"  F.P.(1P)4COL MIX 12 STEP LIYA | F.P ALL FESTIVAIS - MEGA SHOT'S,MINI FAS | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05932` | W 25 SHOTS M COL WINSTAR | OFF SEASON LIST 2025-26 | `BOX` | ₹330.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05933` | W 1000 LAR (800 COUNTING) S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 1 | **1** | `APPROVED` | `override` |
| `05934` | W 2000 LAR U.V. BOX  ANBARASI | OFF SEASON LIST 2025-26 | `BOX` | ₹250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05935` | W 2000 LAR CLASSIC MUGUNTH | OFF SEASON LIST 2025-26 | `BOX` | ₹310.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05936` | W 2000 LAR ( 1200 COUNTING) S.K.M. | OFF SEASON LIST 2025-26 | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05937` | W 2000 LAR ( 1600 COUNTING) S.K.M. | OFF SEASON LIST 2025-26 | `BOX` | ₹400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05938` | W 5000 LAR U.V. BOX  ANBARASI | OFF SEASON LIST 2025-26 | `BOX` | ₹625.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05939` | W 5000 LAR  600 COUNTING S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹850.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05940` | W 5000 LAR  800 COUNTING S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹1000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05941` | W 10000 LAR U.V. BOX  ANBARASI | OFF SEASON LIST 2025-26 | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05942` | W 10000 LAR FULL COUNTING  S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹1700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05943` | W 10000 LAR BIG FULL COUNTING  S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹2000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05944` | W 10000 LAR FUSE FULL COUNTING  EVEREST | OFF SEASON LIST 2025-26 | `BOX` | ₹2800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05946` | W 30 SHOTS M. COL. GEMS | OFF SEASON LIST 2025-26 | `BOX` | ₹370.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05947` | W 60 SHOTS M. COL. GEMS | OFF SEASON LIST 2025-26 | `BOX` | ₹740.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05948` | W 60 SHOTS M. COL. MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05949` | W 60 SHOTS M. COL 30-30 ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹1250.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05950` | W COL SMOKE DHUA  COL (5 P) SUP.KING | OFF SEASON LIST 2025-26 | `BOX` | ₹120.00 | 5 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05951` | W 5000 LAR FUSE  FULL COUNTING EVEREST | OFF SEASON LIST 2025-26 | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05952` | W SADDAM BOMB NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹49.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05953` | W 4 F. PIPE (2 PCS)  I. N. | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05954` | W 3 F P (1P) AYYANAR | OFF SEASON LIST 2025-26 | `BOX` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05955` | W 3 1/2 F P (1P) JAWA | OFF SEASON LIST 2025-26 | `BOX` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05956` | W 1000 LAR UV BOX FULL COUNTING MUGUNTH | OFF SEASON LIST 2025-26 | `BOX` | ₹180.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05957` | W 2000 LAR UV BOX FULL COUNTING MUGUNTH | OFF SEASON LIST 2025-26 | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05958` | W 5000 LAR UV BOX FULL COUNTING MUGUNTH | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05959` | W 10000 LAR SELVIS | OFF SEASON LIST 2025-26 | `BOX` | ₹1450.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05960` | W SPARKULAR MACHINE POWDER | OFF SEASON LIST 2025-26 | `PKT` | ₹910.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `05961` | W 12 SHOTS HEXA COL.AYYANAR | OFF SEASON LIST 2025-26 | `BOX` | ₹135.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05962` | W 1000 LAR EVEREST | OFF SEASON LIST 2025-26 | `BOX` | ₹280.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05963` | W 1000 LAR TAJ( FULL COUNTING ) PANDYA | OFF SEASON LIST 2025-26 | `BOX` | ₹170.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05969` | W 12 SHOTS SQUARE COL S .K. M | OFF SEASON LIST 2025-26 | `BOX` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05970` | W 12 SHOTS SQ ROLLING MORI | OFF SEASON LIST 2025-26 | `BOX` | ₹130.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05971` | W 12 SHOTS SQUARE COL COMBOPACK(6) SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05972` | W 12 SHOTS HEXA COL SELVI | OFF SEASON LIST 2025-26 | `BOX` | ₹120.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05973` | W 12 SHOTS HEXA SILVIR MINES WINSTAR | OFF SEASON LIST 2025-26 | `BOX` | ₹135.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05974` | W 15 SHOTS M. COL APPU PAPPU WINSTAR | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05975` | W 15 SHOTS M. COL FESTIWAL GURUVI | OFF SEASON LIST 2025-26 | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05976` | W 16 SHOTS M.COL M.COL FAIRY TALE SUN | OFF SEASON LIST 2025-26 | `BOX` | ₹290.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05979` | W 25 SHOTS LONG CRACKLING NEW OTHER | OFF SEASON LIST 2025-26 | `BOX` | ₹165.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05980` | W 25 SHOTS LONG ANTHEM  ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹450.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05981` | W 25 SHOTS LONG LION KING SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹460.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05982` | W 25 SHOTS LONG TROY SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹460.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05983` | W 25 SHOTS S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹410.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05984` | W 30 SHOTS M. COL. SHIVAKASHI | OFF SEASON LIST 2025-26 | `BOX` | ₹320.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05985` | W 30 SHOTS M. COL. S.K.Y. | OFF SEASON LIST 2025-26 | `BOX` | ₹330.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05986` | W 30 SHOTS M. COL. WINSTARS | OFF SEASON LIST 2025-26 | `BOX` | ₹340.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05987` | W 30 SHOTS M. COL. CHOLA | OFF SEASON LIST 2025-26 | `BOX` | ₹400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05991` | W 50 SHOTS LONG CRACK SAJ | OFF SEASON LIST 2025-26 | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05992` | W 50 SHOTS LONG GIADIATOR SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹890.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05993` | W 50 SHOTS LONG KING CROWN SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹890.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05994` | W 50 SHOTS LONG AVATAR SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹890.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05996` | W 60 SHOTS M.COL. SHIVAKASHI | OFF SEASON LIST 2025-26 | `BOX` | ₹640.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05997` | W 60 SHOTS M.COL. CHOLA | OFF SEASON LIST 2025-26 | `BOX` | ₹800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05998` | W 80 SHOTS 3 COL SEUS MIXED S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹1175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `05999` | W 80 SHOTS M.COL POP SHOW SUNSHINE | OFF SEASON LIST 2025-26 | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06000` | W 100 SHOTS CRACK SAJ | OFF SEASON LIST 2025-26 | `BOX` | ₹600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06001` | W 100 SHOTS M.COL OTHER | OFF SEASON LIST 2025-26 | `BOX` | ₹1025.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06002` | W 100 SHOTS M.COL MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹1500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06003` | W 100 SHOTS M.COL FUN JOY ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹1630.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06004` | W 100 SHOTS M.COL ULTRA DLX SUNSHINE | OFF SEASON LIST 2025-26 | `BOX` | ₹1825.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06005` | W 100 SHOTS M.COL BIG SAGUN MORI | OFF SEASON LIST 2025-26 | `BOX` | ₹1950.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06006` | W 100 SHOTS M.COL SINGING BRIDS S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹1950.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06007` | W 100 SHOTS M.COL S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹1550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06008` | W 120 SHOTS M.COL  GODWAR SUGA PRIYA | OFF SEASON LIST 2025-26 | `BOX` | ₹1120.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06011` | W 120 SHOTS AYYANAR NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹1680.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06012` | W 120 SHOTS M.COL MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹1500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06013` | W 120 SHOTS M.COL U.V.BOX CHOLA | OFF SEASON LIST 2025-26 | `BOX` | ₹1600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06014` | W 120 SHOTS M.COL  HALDI MORI | OFF SEASON LIST 2025-26 | `BOX` | ₹1725.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06015` | W 120 SHOTS M.COL  STAR SHOW SUNSHINE | OFF SEASON LIST 2025-26 | `BOX` | ₹1900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06016` | W 120 SHOTS M.COL  ENJOY FUN ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹2000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06017` | W 120 SHOTS M.COL WEDDING SERIES S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹1720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06018` | W 160 SHOTS M.COL  ROAD SHOW SUNSHINE | OFF SEASON LIST 2025-26 | `BOX` | ₹2800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06020` | W 240 SHOTS M.COL PENCIL | OFF SEASON LIST 2025-26 | `BOX` | ₹2720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06022` | W 240 SHOTS M.COL AYYANAR | OFF SEASON LIST 2025-26 | `BOX` | ₹3040.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06023` | W 240 SHOTS M.COL CHOLA | OFF SEASON LIST 2025-26 | `BOX` | ₹3000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06024` | W 240 SHOTS M.COL HOODIBABA ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹4200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06025` | W 240 SHOTS M.COL ARABIAN AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹5160.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06026` | W 240 SHOTS M.COL CLASSIC NIGHT AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹4500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06027` | W 240 SHOTS M.COL RAINBOW DANCE S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹4400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06028` | W 250 SHOTS M.COL PARADISE S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹4300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06029` | W 252 SHOTS M.COL BADIYA HA ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹4000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06030` | W 500 SHOTS M.COL UNIVERSAL MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹7600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06031` | W 500 SHOTS M.COL SUBHA MANGAL AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹10900.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06032` | W 510 SHOTS M.COL GONE "N" 10 ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹8300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06033` | W 200 SHOTS M.COL  DAZE N.S.V | OFF SEASON LIST 2025-26 | `BOX` | ₹3000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06034` | W 25 SHOTS SUPER MIX S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹1140.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06035` | W 30 SHOTS PEACOCK DANCE I.N | OFF SEASON LIST 2025-26 | `BOX` | ₹1134.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06036` | W 50 SHOTS BEUTY S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹2200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06037` | W 3" 30 SHOTS M.COL BIG SELVI | OFF SEASON LIST 2025-26 | `BOX` | ₹1750.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06038` | W VOLCANO( 10X 30 SHOT) SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹2300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06039` | W 3 X 12 VANDE MATARAM 3 COL MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹1195.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06040` | W 100 SHOT 10 X 10 PEACOCK LIYA | OFF SEASON LIST 2025-26 | `BOX` | ₹3500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06041` | W 100 SHOT 10 X 10 SIZZLING LIYA | OFF SEASON LIST 2025-26 | `BOX` | ₹3000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06042` | W 100 SHOT 10 X 10 TAIL LIGHT CHOLA | OFF SEASON LIST 2025-26 | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06043` | W 100 SHOT 10 X 10 TAIL LIGHT LIYA | OFF SEASON LIST 2025-26 | `BOX` | ₹3500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06044` | W 100 SHOT 10 X 10 FAN CAKE SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹3800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06045` | W 2' 32 SHOT SHIKARI - SHAMBU ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹3850.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06046` | W 100 SHOT 10 X 10 SHOTS THUNDER LIYA | OFF SEASON LIST 2025-26 | `BOX` | ₹4000.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06047` | W 100 SHOT 10 X 10 NIGHT RIDER AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹3800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06048` | W TOP- TEN ( 10 P ) COCK | OFF SEASON LIST 2025-26 | `BOX` | ₹285.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06049` | W 1 1/4 POGO MIXED ( 10 P) 2 PCS AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹58.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06051` | W 2 1/2 F PIPE FIVE  MIX ( 1 P) TERKHA | OFF SEASON LIST 2025-26 | `BOX` | ₹55.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06052` | W 2 1/2 F PIPE UV BOX SIVAKASHI  ( 1 P) | OFF SEASON LIST 2025-26 | `BOX` | ₹75.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06053` | W 2 1/2 F PIPE MIX UV BOX ( 3 P) | OFF SEASON LIST 2025-26 | `BOX` | ₹165.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06054` | W 2 1/2 F PIPE  BALAJI ( 3 P) | OFF SEASON LIST 2025-26 | `BOX` | ₹175.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06055` | W 2 1/2 F P 3 STEP SURYAKALA (1P) | OFF SEASON LIST 2025-26 | `BOX` | ₹150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06056` | W 2 1/2 F PIPE MEGAL ( 3 P ) MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹445.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06057` | W 3 F PIPE LIGHT AND HOT MIX ( 2P )AN | OFF SEASON LIST 2025-26 | `BOX` | ₹685.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06058` | W 3 F PIPE BIG SIZZ MIXD ( 2P ) MERCU | OFF SEASON LIST 2025-26 | `BOX` | ₹580.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06059` | W 3 1/2 F P 3 COL MIXED ( 1 P ) A GARDE | OFF SEASON LIST 2025-26 | `UNIT` | ₹190.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06062` | W 3 1/2 F P FIVE COL MIX ( 1 P ) JAWA | OFF SEASON LIST 2025-26 | `BOX` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06063` | W 3 1/2 F P FIVE COL MIX ( 1 P) AYYANAR | OFF SEASON LIST 2025-26 | `BOX` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06064` | W 3 1/2 F P BIG SIZECOL MIX(1 P) AYYAN | OFF SEASON LIST 2025-26 | `BOX` | ₹310.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06065` | W 3 1/2 F P YELLOW ANGEL (1 P) ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹310.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06066` | W 3 1/2 F P ITS FLYING (1 P) ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹416.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06067` | W 3 1/2 F P DOUBLE BALL (1 P) JAWA | OFF SEASON LIST 2025-26 | `BOX` | ₹300.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06068` | W 3 1/2 F P DOUBLE BALL (2 P) SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹750.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06069` | W 3 1/2 F P STEPS (1 P) I. N. | OFF SEASON LIST 2025-26 | `BOX` | ₹275.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06071` | W 4 F PIPE TIN PIPI(1P) 6 COL RISING STA | OFF SEASON LIST 2025-26 | `BOX` | ₹280.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06072` | W 4 F P 3 COL MIXED ( 2 P) W MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹850.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06073` | W 4 F P 3 COL MIXED ( 2 P) W  I.N | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06074` | W 4 F P DLX 15 COL MIXED ( 2 P)  SONY | OFF SEASON LIST 2025-26 | `BOX` | ₹900.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06077` | W 5 F P JOKER ( 1 P)ANIL | OFF SEASON LIST 2025-26 | `BOX` | ₹617.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06078` | W SNOW SPRAY WHITE TAIWAN | OFF SEASON LIST 2025-26 | `BOX` | ₹22.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06079` | W COL SMOKE DHUA SPL. ORANGE COL SUP-KIN | OFF SEASON LIST 2025-26 | `BOX` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06080` | W COL SMOKE DHUA  ORANGE  5P SUP-KING | OFF SEASON LIST 2025-26 | `BOX` | ₹125.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06081` | W 15 SHOT M.COL DHUA R.R. | OFF SEASON LIST 2025-26 | `BOX` | ₹550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06082` | W SKYDER 9 SHOT M. COL SUO.KING | OFF SEASON LIST 2025-26 | `BOX` | ₹1800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06083` | W YELLO, BLUE, PINK[ GREEN 4 VER SUP.KIN | OFF SEASON LIST 2025-26 | `BOX` | ₹1800.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06084` | W 40 CM MIX PARTY POPPER 5 VER JOY | OFF SEASON LIST 2025-26 | `BOX` | ₹27.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06085` | W THROWING COLRIBBON THROW KING | OFF SEASON LIST 2025-26 | `BOX` | ₹34.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06086` | W 4 SHOTS PAPER FANTASIA KIARA | OFF SEASON LIST 2025-26 | `BOX` | ₹120.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06087` | W 8 SHOTS PAPER KBC KIARA | OFF SEASON LIST 2025-26 | `BOX` | ₹225.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06088` | W 8 SHOTS PAPER BONANZA ASISHWARYA | OFF SEASON LIST 2025-26 | `BOX` | ₹240.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06089` | W 16 SHOTS PAPER COL MAGIC S.T.D | OFF SEASON LIST 2025-26 | `BOX` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06090` | W 21 SHOTS PAPER CENTURY PEOPLES | OFF SEASON LIST 2025-26 | `BOX` | ₹695.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06091` | W 30 SHOT M. COL. PRINCE | OFF SEASON LIST 2025-26 | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06092` | W 7 SHOT ( 10 P ) MERCURY | OFF SEASON LIST 2025-26 | `BOX` | ₹210.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06093` | W 120 SHOTS M. COL. WINSTAR | OFF SEASON LIST 2025-26 | `BOX` | ₹1360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06094` | W 500 SHOTS M.COL  N.S.V | OFF SEASON LIST 2025-26 | `BOX` | ₹6500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06095` | W 5000 LAR CLASSIC MUGUNTH | OFF SEASON LIST 2025-26 | `BOX` | ₹775.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06096` | W SADDAM W/F MIX LABLE | OFF SEASON LIST 2025-26 | `PKT` | ₹36.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `06097` | W SADDAM W/F SANTOSH | OFF SEASON LIST 2025-26 | `PKT` | ₹40.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06098` | W 2 1/2" F. PIPE 2 IN 1 ( 2 P )CORNATION | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06099` | W 18 SHOT ROMANCANDLE ( 2P) | OFF SEASON LIST 2025-26 | `BOX` | ₹400.00 | 2 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06100` | W 30 SHOT M. COL CITY MALL | OFF SEASON LIST 2025-26 | `BOX` | ₹350.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06101` | W 30 SHOT M.COL PENCIL | OFF SEASON LIST 2025-26 | `BOX` | ₹320.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06102` | W LADEN BOMB  6 NO B. R | OFF SEASON LIST 2025-26 | `BOX` | ₹190.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06103` | W SHER SHIKAR 6 NO  B.R. | OFF SEASON LIST 2025-26 | `BOX` | ₹170.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06104` | W GOLDEN TOP TIGER 6 NO FANCY | OFF SEASON LIST 2025-26 | `BOX` | ₹170.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06105` | W JHANSI BOMB GREEN MALATI'S | OFF SEASON LIST 2025-26 | `BOX` | ₹85.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06106` | W 5000 LAR (600) COUNTING SANTHANMARI | OFF SEASON LIST 2025-26 | `BOX` | ₹950.00 | 1 | **1** | `APPROVED` | `override` |
| `06107` | W 10 SHOTS M.COL.MIX I.N | OFF SEASON LIST 2025-26 | `BOX` | ₹290.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06108` | W 2 1/2  F. PIPE MIX ( 1 P ) LONG I.N | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06109` | W 288 SHOT NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹1150.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06110` | W 2 KG. COL.CLOUD WITH FOG MIX CYLINDER | OFF SEASON LIST 2025-26 | `CYLINDER` | ₹550.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06111` | W 4 KG. COL.CLOUD WITH FOG MIX CYLINDER | OFF SEASON LIST 2025-26 | `CYLINDER` | ₹750.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06112` | W 6 KG. COL.CLOUD WITH FOG MIX CYLINDER | OFF SEASON LIST 2025-26 | `CYLINDER` | ₹850.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06113` | W TOP TIGER 6 NO | OFF SEASON LIST 2025-26 | `PKT` | ₹140.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06114` | W 1000 LAR KALUGU | OFF SEASON LIST 2025-26 | `BOX` | ₹100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06115` | W 2000 LAR KALUGU | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06116` | W 5000 LAR KALUGU | OFF SEASON LIST 2025-26 | `BOX` | ₹500.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06117` | W 10000 LAR JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹1100.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06118` | W 30 SHOT M. COM J.J.F.W. | OFF SEASON LIST 2025-26 | `BOX` | ₹375.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06119` | W 30 SHOT M. COM  GURU JOTHY | OFF SEASON LIST 2025-26 | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06120` | W 60 SHOT M. COM  GURU JOTHY | OFF SEASON LIST 2025-26 | `BOX` | ₹720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06121` | W 240 SHOT M. COM  GURU JOTHY | OFF SEASON LIST 2025-26 | `BOX` | ₹2880.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06122` | W 1000 LAR JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹110.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06123` | W 2000 LAR JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹220.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06124` | W 120 SHOT M. COM  GURU JOTHY | OFF SEASON LIST 2025-26 | `BOX` | ₹1440.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06125` | W 5000 LAR JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹550.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06126` | W 12 SHOT KINGSTAR'S | OFF SEASON LIST 2025-26 | `BOX` | ₹160.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06127` | W 25 SHOTS SQUARE APPLE | OFF SEASON LIST 2025-26 | `BOX` | ₹175.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06128` | W LADEN BOMB  NEW 6 NO B. R | OFF SEASON LIST 2025-26 | `BOX` | ₹170.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06129` | W 60 SHOTS M. COL. PENCIL | OFF SEASON LIST 2025-26 | `BOX` | ₹640.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06130` | W 60 SHOTS M COL TRENDS | OFF SEASON LIST 2025-26 | `BOX` | ₹700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06131` | W 50 SHOTS M. COL. BIG  I.N | OFF SEASON LIST 2025-26 | `BOX` | ₹680.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06132` | W 1000 LAR TAJ/SELVIS | OFF SEASON LIST 2025-26 | `BOX` | ₹140.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06133` | W 2000 LAR TAJ/SELVIS | 10 CHORSA | `BOX` | ₹280.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06134` | W COLD PYRO R&G BOX 3.M.35.S (6P) | OFF SEASON LIST 2025-26 | `BOX` | ₹80.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06135` | W COLD PYRO YELLO BOX 3.M.30.S(10P) | OFF SEASON LIST 2025-26 | `BOX` | ₹120.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06136` | W SPARKULAR GUN SADI-(CELL) | OFF SEASON LIST 2025-26 | `BOX` | ₹150.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06137` | W SPARKULAR GUN PENCIL-(CELL) | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06138` | W 30 SHOTS AYYANAR NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06139` | W 60 SHOTS AYYANAR NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹800.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06140` | W 15 SHOTS M. COL. DAY TRIP BALAJI | OFF SEASON LIST 2025-26 | `BOX` | ₹220.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06141` | W 30 SHOTS M. COL. WHITE HEAVEN BALAJI | OFF SEASON LIST 2025-26 | `BOX` | ₹335.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06142` | W 60 SHOTS M. COL. CROSS FIT BALAJI | OFF SEASON LIST 2025-26 | `BOX` | ₹670.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06143` | W 60 SHOT M. COL CITY MALL | OFF SEASON LIST 2025-26 | `BOX` | ₹700.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06144` | W 120 SHOT M. COL CITY MALL | OFF SEASON LIST 2025-26 | `BOX` | ₹1400.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06146` | W 3 1/2 F P  J J ( 1 P) | OFF SEASON LIST 2025-26 | `BOX` | ₹210.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06147` | W 1000 LAR NEW JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹115.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06148` | W 2000 LAR NEW JAYEM | OFF SEASON LIST 2025-26 | `BOX` | ₹230.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06149` | W 5000 LAR NEW JAYAM | OFF SEASON LIST 2025-26 | `BOX` | ₹575.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06150` | W MULTICOLOR PAPER | OFF SEASON LIST 2025-26 | `1 KG` | ₹105.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06151` | W CHAMKI  PAPER | OFF SEASON LIST 2025-26 | `1 KG` | ₹120.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06152` | W 120 SHOT M.COL NEW AYYANAR | OFF SEASON LIST 2025-26 | `BOX` | ₹1600.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06153` | W 3 1/2 F P DOUBLE BALL CHERRY (1P) | OFF SEASON LIST 2025-26 | `BOX` | ₹320.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06154` | W 120 SHOTS NEW PENCIL | OFF SEASON LIST 2025-26 | `BOX` | ₹1360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06155` | W 4 F. PIPE (1 P) 12 STEP UV.BOX | OFF SEASON LIST 2025-26 | `BOX` | ₹370.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06156` | W 2 1/2 F PIPE  MIX BIG  ( 3 P) | OFF SEASON LIST 2025-26 | `BOX` | ₹375.00 | 3 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06157` | W COLD PYRO BOX 3.M.35.S (6P) | OFF SEASON LIST 2025-26 | `BOX` | ₹100.00 | 6 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06158` | W 30 SHOTS M. COL. VETRI VELAVAN | OFF SEASON LIST 2025-26 | `BOX` | ₹380.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06159` | W 60 SHOTS M. COL. VETRI VELAVAN | OFF SEASON LIST 2025-26 | `BOX` | ₹760.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06160` | W 120 SHOTS M. COL. VETRI VELAVAN | OFF SEASON LIST 2025-26 | `BOX` | ₹1520.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06161` | W 30 SHOTS M. COL.ELITE | OFF SEASON LIST 2025-26 | `BOX` | ₹360.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06162` | W 60 SHOTS M. COL.ELITE | OFF SEASON LIST 2025-26 | `BOX` | ₹720.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06163` | W 3 1/2 F P FIVE COL MIX ( 1 P ) BALAJI | OFF SEASON LIST 2025-26 | `BOX` | ₹180.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06164` | W 2 30  SHOT  M. COM | OFF SEASON LIST 2025-26 | `BOX` | ₹3200.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06165` | W 60 SHOTS M COL AYYANAR NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹840.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06166` | W 30 SHOTS M COL AYYANAR NEW | OFF SEASON LIST 2025-26 | `BOX` | ₹420.00 | 1 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06171` | 129- KIT-KAT(10 P)YUVA | SERPANTS & NAGGOLI | `PKT` | ₹18.50 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06172` | 130- DRAGON FIGHTER U.V.BOX VIRABALAJI | SERPANTS & NAGGOLI | `PKT` | ₹19.50 | 1 | **1** | `DEFAULT` | `fallback` |
| `06173` | 131- KIT-KAT (10 P) RAJHARISH | SERPANTS & NAGGOLI | `PKT` | ₹20.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06174` | 132- KIT-KAT(10 P)U.V.BOX VETRI | SERPANTS & NAGGOLI | `PKT` | ₹21.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06175` | 133- KIT-KAT BIG(10 P)TIRUMINIK | SERPANTS & NAGGOLI | `PKT` | ₹32.00 | 10 | **1** | `UNVERIFIED_HEURISTIC` | `heuristic` |
| `06176` | 134- CHIT PUT MERCURY | SERPANTS & NAGGOLI | `PKT` | ₹55.00 | 1 | **1** | `DEFAULT` | `fallback` |
| `06177` | 135- POP POP CRACKLING AYYAN | SERPANTS & NAGGOLI | `PKT` | ₹46.50 | 1 | **1** | `DEFAULT` | `fallback` |
