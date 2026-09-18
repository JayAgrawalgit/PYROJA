# PYROJA Product Packaging Rules Business Review Worksheet

**Target Audience:** Business Owner / Inventory Manager / Showroom Lead  
**Date Generated:** September 19, 2026  
**Active Fiscal Year:** D2627  

> [!IMPORTANT]
> **How to Use This Worksheet:**
> - **Under the Hardened Rule Policy**, all products without an approved explicit rule currently enforce a pack multiple of `1` on wholesale orders. This guarantees that unverified heuristics will **never** reject or block an order.
> - To enforce a pack multiple on wholesale orders (e.g., requiring wholesale buyers to purchase in multiples of 10 or 50), the business owner must review the suggested pack multiple and check **[x] Approve**.
> - Once signed off, approved rules are added to `sync-service/app/data/catalog_pack_rules.json` with `status: "APPROVED"` and `enabled: true`.

---

## Section 1: Currently Approved Explicit Enforcements (32 Products)

These rules are already active in `catalog_pack_rules.json` and verified against historical `SALETRN.DBF` sales records.

| Code | Product Description | Brand | FoxPro UOM | Rate (₹) | Enforced Pack | Status | Historical Verification Notes |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `00079` | 119- ASST CARTOON(10 PCS)DURGESH (1P) | ASST CARTOON & RAIL | `PKT` | ₹13.50 | **1** | `APPROVED` | Dual parenthetical: (10 PCS) (1P). Inner pack is 1P. |
| `00082` | 124- BIG NAGGOLI PANDYAN BLACK(100X1=1 B | SERPANTS & NAGGOLI | `BUNDLE` | ₹150.00 | **1** | `APPROVED` | Big Naggoli bundle (100X1=1 B). Billed per bundle in SALETRN. |
| `00083` | 125- BIG NAGGOLI PANDYAN RED(100X1= 1BOX | SERPANTS & NAGGOLI | `BUNDLE` | ₹155.00 | **1** | `APPROVED` | Big Naggoli bundle (100X1= 1BOX). Billed per bundle in SALETRN. |
| `00178` | 148- RED BIJALI ROSE (100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹17.50 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00180` | 149- MINI RED BIJALI CAT BRAND(100 PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹58.00 | **10** | `APPROVED` | Mini Red Bijali 10 bags outer case pack. |
| `00181` | 150- RED BIJALI AYYANAR (100 PCS) 10 BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹30.00 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00182` | 151- RED BIJALI GANESH(100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹41.00 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00183` | 152- RED BIJALI S.T.D.(100 PCS ) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹53.00 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00184` | 153- RED BIJALI SONY (100 PCS) 10 BAGS | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹60.00 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00185` | 154- RED BIJALI VIMAL(100 P)10 BAG 1 3/4 | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹65.00 | **10** | `APPROVED` | Red Bijali 10 bags outer case pack. |
| `00186` | 290- 10 CHORASA MUNNA DURGESH(100P=1BUND | 10 CHORSA | `BUNDLE` | ₹335.00 | **1** | `APPROVED` | 10 Chorsa bundle (100P=1BUND). Billed per bundle in SALETRN. |
| `00187` | 291- 10 GAINT JAWAN GEMS (100P=1BUNDLE ) | 10 CHORSA | `BUNDLE` | ₹360.00 | **1** | `APPROVED` | 10 Gaint Jawan bundle (100P=1BUNDLE). Billed per bundle in SALETRN. |
| `00223` | 293- 16 CHORSA B GROUP (50P= 1 BUNDEL) | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹7.25 | **50** | `APPROVED` | 16 Chorsa bundle (50P=1 BUNDEL). Billed in multiples of 50 packets in SALETRN. |
| `00224` | 294- 28 CHORSA K.R.K (50P= 1 BUNDEL) | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹12.00 | **50** | `APPROVED` | 28 Chorsa bundle (50P=1 BUNDEL). Sold in multiples of 50 packets. |
| `00225` | 295- 28 CHORSA TAJ  T/MEENA (50P= 1 BUND | 28 -CHORSA & 28-GAINT CHORSA | `PKT` | ₹13.25 | **50** | `APPROVED` | 28 Chorsa bundle (50P=1 BUNDEL). Sold in multiples of 50 packets. |
| `00455` | 534- JADUGAR UV.BOX AYYAN (4 P )( 1 P) | FANCY FLOWER POTS MIXED | `PKT` | ₹260.00 | **1** | `APPROVED` | Dual parenthetical: (4 P )( 1 P). Inner pack is 1P. |
| `00456` | 535- MANORANJAN U.V.BOX AYYAN(4 P)(1P) | FANCY FLOWER POTS MIXED | `PKT` | ₹260.00 | **1** | `APPROVED` | Dual parenthetical: (4 P)(1P). Inner pack is 1P. |
| `02157` | 1121- MISSILE SIREN(127X1)TITANIC ORIGIN | RING CAPS AND MISSILE | `PKT` | ₹65.00 | **1** | `APPROVED` | Missile repeater (127X1). Multi-shot tube count, sold as 1 unit. |
| `02905` | W 1000 LAR (600 COUNTING) S.K.M | OFF SEASON LIST 2025-26 | `PKT` | ₹180.00 | **1** | `APPROVED` | Lar garland (1000 LAR). Sold per garland box. |
| `03088` | 114- R & G MATCH BOX SHANTHI(600DABBA) | MATCH BOX | `BUNDLE` | ₹500.00 | **1** | `APPROVED` | Matchbox bundle (600 DABBA). Billed per bundle, not individual dabba. |
| `04042` | 1079- DHAGA (80 DABBI) INDIA | POP - POP | `PKT` | ₹6.00 | **1** | `APPROVED` | Dhaga bundle (80 DABBI). Billed per packet/bundle. |
| `04192` | 115- R & G MATCH BOX RAYAL(600 DABBA) | MATCH BOX | `BUNDLE` | ₹500.00 | **1** | `APPROVED` | Matchbox bundle (600 DABBA). Billed per bundle. |
| `04301` | 159- STRIPPED BIJALI MERCURY(50PCS)10BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹25.50 | **10** | `APPROVED` | Stripped Bijali 10 bags outer case pack. |
| `04302` | 160- STRIPPED BIJALI ROSE(100PCS)10BAG | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹21.50 | **10** | `APPROVED` | Stripped Bijali 10 bags outer case pack. |
| `04303` | 161- STRIPPED BIJALI AYYANAR(100PCS)10BA | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹32.00 | **10** | `APPROVED` | Stripped Bijali 10 bags outer case pack. |
| `04305` | 163- STRIPPED BIJALI GAINT S.T.D(100PCS) | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹50.00 | **10** | `APPROVED` | Stripped Bijali 10 bags outer case pack. |
| `04306` | 164- STRIPPED BIJALI S.T.D(100PCS)10 | RED , STRIPPED, GOLD BIJALI.BASKET BOMB | `BAG` | ₹60.00 | **10** | `APPROVED` | Stripped Bijali 10 bags outer case pack. |
| `04613` | 650- SUDARSHAN CHAKKAR ANIL ( 6 P) 1P | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹153.00 | **1** | `APPROVED` | Dual pack indicator: (6 P) 1P. Inner pack is 1P. |
| `04616` | 653- GIANT WHEEL AYYAN (5 PCS) (1P) BIG | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹175.00 | **1** | `APPROVED` | Dual parenthetical: (5 PCS) (1P). Inner pack is 1P. |
| `04625` | 662- SKY  WHEEL AYYAN (5 PCS) (1P) | FANCY - CHAKKAR / WHEELS / SPINNERS | `PKT` | ₹345.00 | **1** | `APPROVED` | Dual parenthetical: (5 PCS) (1P). Inner pack is 1P. |
| `05933` | W 1000 LAR (800 COUNTING) S.K.M | OFF SEASON LIST 2025-26 | `BOX` | ₹200.00 | **1** | `APPROVED` | Lar garland (1000 LAR). Sold per garland box. |
| `06106` | W 5000 LAR (600) COUNTING SANTHANMARI | OFF SEASON LIST 2025-26 | `BOX` | ₹950.00 | **1** | `APPROVED` | Lar garland (5000 LAR). Sold per garland box. |

---

## Section 2: Products with Heuristic Suggestions > 1 (407 Products)

For each item below, guarded heuristic parsing extracted a pack tag from the product name (e.g., `(10 P)`, `(5 P)`).
**Current Enforced Value is `1` (orders will NOT be blocked).** Review and indicate whether to enforce this multiple for wholesale orders:

| Code | Product Description | FoxPro UOM | Rate (₹) | Suggested | Current Enforced | Proposed Business Action | Notes / Reason |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `00080` | 120- ASST CARTOON BEN TEN(25P)AYYANAR 4P | `PKT` | ₹55.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00081` | 121- SNAKE CARTOON(25P)SAMLL AYYANAR 4P | `PKT` | ₹55.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00109` | 178- 9 CM PLAIN INDRA (10 DABBI=1BOX) | `BOX` | ₹65.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00110` | 179- 9 CM COL INDRA (10 DABBI=1BOX) | `BOX` | ₹69.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00111` | 180- 9 CM PLAIN CLASSIC (10DABBI=1 | `BOX` | ₹78.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00112` | 181- 9 CM COL CLASSIC (10 DABBI=1BOX) | `BOX` | ₹89.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00120` | 195- 10 CM SILVER DROPS SARAVANA(5P) | `PKT` | ₹15.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00132` | 221- 10 CM PLAIN CLASSIC (5 P) | `PKT` | ₹12.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00133` | 222- 10 CM COL CLASSIC (5 P) | `PKT` | ₹13.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00134` | 223- 10 CM GREEN CLASSIC (5 P) | `PKT` | ₹13.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00136` | 224- 10 CM RED CLASSIC(5 P) | `PKT` | ₹13.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00137` | 225- 10 CM 2 IN 1 CLASSIC(5 P) | `PKT` | ₹13.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00138` | 226- 12 CM PLAIN LX CLASSIC (5 P) | `PKT` | ₹14.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00139` | 227- 12 CM COL LX CLASSIC (5 P) | `PKT` | ₹15.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00140` | 228- 12 CM PLAIN DLX CLASSIC (5 P) | `PKT` | ₹16.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00142` | 229- 12 CM COL DLX CLASSIC (5 P) | `PKT` | ₹17.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00143` | 230- 12 CM GREEN LX CLASSIC (5 P) | `PKT` | ₹14.75 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00144` | 276- 10 CM PLAIN ASOK ( 5 P) | `PKT` | ₹20.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00145` | 277- 10 CM COL ASOK ( 5 P) | `PKT` | ₹23.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00147` | 278- 10 CM GREEN ASOK ( 5 P) | `PKT` | ₹28.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00148` | 279- 10 CM RED ASOK ( 5 P) | `PKT` | ₹30.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00149` | 280- 10 CM 4 COLOUR ASOK ( 5 P) | `PKT` | ₹28.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00250` | 308- 20 DLX KING GANESH DURAI( 10 P) | `PKT` | ₹25.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00251` | 309- 20 DLX BALAJI( 10 P) | `PKT` | ₹37.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00252` | 310- 24 DLX RAGURAM ( 10 P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00253` | 311- 24 DLX GANESH DURAI( 10 P) | `PKT` | ₹32.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00254` | 312- 24 DLX COCK (10P) | `BOX` | ₹63.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00255` | 313- 28 DLX RAGURAM(10 P) | `PKT` | ₹37.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00256` | 314- 32 DLX KICK SHOT BALAJI( 5 P ) | `PKT` | ₹65.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00257` | 315- 48 DLX RAGURAM ( 5 P) | `PKT` | ₹50.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00288` | 329- 2' PARROT AYYANAR (25 PCS) | `PKT` | ₹5.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00289` | 330- 2 3/4 KURVI DURGESH (25 PCS) | `PKT` | ₹6.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00291` | 331- 2 3/4 KURVI VELVAN (10 PCS) | `PKT` | ₹7.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00292` | 332- 2 3/4 KURVI GEMS (25 P) | `PKT` | ₹7.75 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00293` | 333- 2 3/4 GREEN PARROT PONMALAR(25 P) | `PKT` | ₹9.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00294` | 334- 2 3/4 KURVI AYYANAR (25 P) | `PKT` | ₹9.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00297` | 337- 3 1/2 BEN TEN DURGESH/JAYA (15 P) | `PKT` | ₹9.50 | **15** | 1 | [ ] Approve (15)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00298` | 338- 3 1/2 JOKER SADA BAJAJI(10 P) | `PKT` | ₹10.75 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00299` | 339- 3 1/2 MIX LABEL SADA AYYANAR (10 P | `PKT` | ₹13.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00300` | 340- 3 1/2 GREEN PARROT PONMALAR (10 P) | `PKT` | ₹14.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00301` | 341- 3 1/2 ELEPHANT I.N(10 P) | `PKT` | ₹14.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00325` | 399- 2 SOUND DHAMAKA RAJHARISH(10P) | `PKT` | ₹22.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00326` | 400- 2 SOUND DHAMAKA NM JYOTHI(10P) | `PKT` | ₹25.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00328` | 402- 2 SOUND DHAMAKA I.N. (10P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00368` | 413- 2 LXM DHAMAKA GENIUS (25 P) | `PKT` | ₹5.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00370` | 415- 3 1/2 LXM DHAMAKA AYYANAR (10 P) | `PKT` | ₹13.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00371` | 416- 3 1/2 LXM DHAMAKA I.N(10 P) | `PKT` | ₹14.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00372` | 417- 3 1/2 LXM DHAMAKA AMBIKA(10 P) | `PKT` | ₹15.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00374` | 419- 3 1/2 LXM DHAMAKA S.T.D ( 10 P) | `PKT` | ₹24.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00381` | 426- 4' LXM DHAMAKA I.N ( 10 P) | `PKT` | ₹18.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00382` | 427- 4' LXM DHAMAKA AYYANAR ( 10 P) | `PKT` | ₹21.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00383` | 428- 4' LXM DHAMAKA AYYAN ( 10 P) | `PKT` | ₹32.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00387` | 432- 4' DLX LXM DHAMAKA I.N ( 10 P) | `PKT` | ₹23.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00388` | 433- 4' DLX BAJ DHAMAKA T/MEENA( 10 P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00389` | 434- 4' DLX LXM DHAMAKA T/MEENA( 10 P) | `PKT` | ₹32.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00391` | 436- 4' DLX LXM DHAMAKA AYYANAR ( 10 P) | `PKT` | ₹35.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00395` | 439- 4 DLX GOLD LXM T/MEENA ( 10 P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00396` | 440- 4 DLX GOLD LXM AYYANAR( 10 P) | `PKT` | ₹35.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00427` | 444- FLOWER POTS SMALL RAJLAXMI(10 P) | `PKT` | ₹38.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00429` | 445- FLOWER POTS SMALL ARUDHARA(10 P) | `PKT` | ₹50.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00430` | 446- FLOWER POTS SMALL MURCURY(10 P) | `PKT` | ₹64.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00438` | 517- TRI COL FOUNTAIN RAJHARISH W (5 P) | `PKT` | ₹185.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00440` | 519- TRI COL FOUNTAIN MERCURY (10 P) | `PKT` | ₹265.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00441` | 520- TRI COL FOUNTAIN COCK (5 P) | `PKT` | ₹297.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00442` | 521- TRI COL FOUNTAIN S.T.D (5 P) | `PKT` | ₹375.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00443` | 522- TRI COL FOUNTAIN T/MEENA (5 P) | `PKT` | ₹235.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00445` | 524- COL FOG FOUNTAIN S.T.D.(5 P) (2P) | `PKT` | ₹77.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00446` | 525- JET FOUNTAIN W S.T.D(5 P) | `PKT` | ₹85.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00447` | 526- KIDDY'S JOY F P 5IN 1 AYYAN ( 5P) | `PKT` | ₹165.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00448` | 527- MINI POPPERS 5 IN 1 MERCURY( 5 P ) | `PKT` | ₹175.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00449` | 528- HAPPINESS F. POT 5 IN 1 S.T.D (5 P) | `PKT` | ₹265.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00450` | 529- TORA TORA F. POT 5 IN 1 AYYAN( 5 P | `PKT` | ₹355.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00454` | 533- CRACKLING FOUNTAIN SIVASAKTHI(3 P) | `PKT` | ₹200.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00460` | 539- GOLDEN WHISTE SMALL (2P)S.T.D | `PKT` | ₹150.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00461` | 540- CHOTA BHAI F P MINI SIREN AYYAN(5P) | `PKT` | ₹150.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00463` | 575- MAGIC WHIP S.T.D( 2 P) | `PKT` | ₹89.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00491` | 550- SADA MATKA ANAR OTHER (100P) | `PCS` | ₹15.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00492` | 551- MINI PEARL GUDIYA ( 5 PCS ) | `BOX` | ₹135.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00493` | 552- TIM TIM GUDIYA ( 5 PCS ) | `BOX` | ₹165.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00494` | 553- LITTLE STAR ANAR GUDIYA ( 5 PCS ) | `BOX` | ₹270.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00495` | 554- 2 IN 1 ANAR GUDIYA (10 PCS) | `BOX` | ₹325.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00496` | 555- GOLDEN STAR GUDIYA  ( 5PCS) | `BOX` | ₹270.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00497` | 556- ASHARFI GUDIYA ( 5 PCS) | `BOX` | ₹300.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00499` | 557- JASMINE GUDIYA ( 5PCS) | `BOX` | ₹300.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00501` | 558- DAZZLE GUDIYA ( 5 PCS) | `BOX` | ₹465.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00502` | 559- DELUXE GUDIYA ( 4 PCS) | `BOX` | ₹500.00 | **4** | 1 | [ ] Approve (4)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00503` | 560- GIFT BOX GUDIYA ( 4 PCS) | `BOX` | ₹650.00 | **4** | 1 | [ ] Approve (4)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00504` | 561- ASHARFI  GOLDEN STAR OTHER (10 PCS) | `BOX` | ₹240.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00505` | 562- MUTT PUTT ANAR MERCURY ( 5 PCS ) | `BOX` | ₹200.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00533` | 588- G C BIG T/MEENA( 10 P)(10P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00534` | 589- G C BIG GANESH ( 10 P)(10P) | `PKT` | ₹35.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00535` | 590- G C BIG JENIS(10 P)(5P) | `PKT` | ₹40.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00536` | 591- G C BIG W MERCURY(10 P)(5P) | `PKT` | ₹44.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00537` | 592- G C BIG R/G S.T.D (25 P)(4P) | `PKT` | ₹53.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00542` | 645- DISCO WHEEL GAYATHRI(10 PCS) | `PKT` | ₹76.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00543` | 646- DISCO WHEEL S.M.K.(10 PCS) | `PKT` | ₹85.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00544` | 647- SILVER GAINT WHEEL MERCURY (10P)(2P | `PKT` | ₹165.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00564` | 707- 18 T STAR D/VADIVEL(10P) 10 P | `PKT` | ₹15.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00565` | 708- 18 T STAR SRIPATHI(10P) 10 P | `PKT` | ₹16.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00566` | 709- 18 T STAR T/MEENA (10P) 10 P | `PKT` | ₹20.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00567` | 710- 48 T STAR (10P) SRIPATHI 10 P | `PKT` | ₹50.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00568` | 711- 120 T STAR S.T.D (10P) 5 P | `PKT` | ₹155.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00609` | 594- G C BIG VENKATESH (25 PCS) (4P) | `PKT` | ₹45.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00610` | 595- G C BIG T/MEENA (25 PCS) (W) (4P) | `PKT` | ₹75.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00611` | 596- G C BIG GANESH (25 PCS) (4P) | `PKT` | ₹80.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00614` | 735- BULLET BOMB MINI SRI ATHISAYA(10P) | `PKT` | ₹14.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00615` | 736- MINI BULLET BOMB T/MEENA(10 P)10 | `PKT` | ₹16.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00616` | 737- BULLET BOMB MINI SRIPATHI ( 10 P ) | `PKT` | ₹18.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00617` | 738- BULLET BOMB MEDIUM T/MEENA( 10 P ) | `PKT` | ₹21.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00618` | 739- BULLET BOMB MEDIUM APPLE( 10 P ) | `PKT` | ₹21.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00619` | 740- SUPER BULLET BOMB AYYANAR ( 10 P ) | `PKT` | ₹25.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00620` | 741- BULLET BOMB GANESH ( 10 P ) | `PKT` | ₹27.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00621` | 742- BULLET BOMB BIG DLX T/MEENA ( 10 P | `PKT` | ₹32.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00622` | 743- SUPER BULLET BOMB ( 10 P ) OVEEYA | `PKT` | ₹39.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00630` | 751- SOLDIER BOMB GREEN W/G (10 P)V.F.I | `PKT` | ₹75.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00631` | 752- JHANSI BOMB GREEN W/F(10P)MALATI'S | `PKT` | ₹80.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00688` | 598- G C ASOKA T/MEENA (10 P) | `PKT` | ₹40.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00691` | 122- RAJDHANI RAIL(10 PCS)AYYANAR (10 P) | `PKT` | ₹65.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00707` | 138- GANGA JAMUNA SRI PATHI(5P) | `PKT` | ₹45.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00744` | 541- MINI SIREM F. POT COCK ( 3 PCS ) | `PKT` | ₹175.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00745` | 542- BIG SIREM F. POT COCK ( 3 PCS ) | `PKT` | ₹280.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00758` | 599- G C ASOKA AYYANAR(10 P) | `PKT` | ₹50.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00761` | 649- SUN FLOWER WHEEL I. N (10 PCS) | `PKT` | ₹255.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00769` | 600- G C ASOKA W MERCURY(10 P) | `PKT` | ₹67.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00848` | 231- 12 CM RED LX CLASSIC (5 P) | `PKT` | ₹17.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00866` | 158- STRIPPED BIJALI ROSE(50 PCS)10 BAG | `BAG` | ₹11.50 | **50** | 1 | [ ] Approve (50)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00876` | 601- G C ASOKA BIG SIZE GANESH(10 P) | `PKT` | ₹72.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `00925` | 602- G C ASOKA S.T.D (10 P) (5P) | `PKT` | ₹88.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `01167` | 139- GANGA JAMUNA OVEETA(5P) | `PKT` | ₹52.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `01176` | 141- GANGA JAMUNA MERCURY( 5 P) | `PKT` | ₹65.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02042` | 281- 12 CM PLAIN ASOK ( 2 P) | `PKT` | ₹35.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02081` | 142- MAGIC FOUNTAIN OVEEYA(10 PCS) | `PKT` | ₹120.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02124` | 603- G C ASOKA SPINNER W JENIS (10 P) | `PKT` | ₹75.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX)RACHNA | `PKT` | ₹6.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX) AYYAN | `PKT` | ₹6.50 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02154` | 1119- RING CAPS (1OOPKT= 1 BOX)GOKUL | `PKT` | ₹7.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02155` | 1120- RING CAPS (1OOPKT= 1 BOX)COCK | `PKT` | ₹7.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02275` | 282- 12 CM COLOUR ASOK ( 2 P) | `PKT` | ₹40.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02525` | 1087- BULLET ROCKET YUG ( 36 PCS) | `PCS` | ₹108.00 | **36** | 1 | [ ] Approve (36)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02660` | 666- BABY ROCKET RAJ LAXMI (10P) | `PKT` | ₹30.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02665` | 283- 15 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02667` | 284- 30 CM PLAIN ASOK ( 2 P) | `PKT` | ₹60.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02668` | 285- 30 CM COL ASOK ( 2 P) | `PKT` | ₹70.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02669` | 567- DANCING BUTTERFLY R/G.(10P) VANAJA | `PKT` | ₹45.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02671` | 569- DANCING BUTTERFLY AYYAN ( 10 P) | `PKT` | ₹125.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02672` | 670- PYRO DANCE BUTTERFLY SUNSHINE( 10P) | `PKT` | ₹140.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02673` | 571- COL CHAN. BUTTERFLY S.T.D (10P) | `PKT` | ₹132.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02676` | 667- COLOUR ROCKET AYYANAR (10P) ) | `PKT` | ₹48.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02677` | 668- RAINBOW ROCKET S.T.D (10P) | `PKT` | ₹130.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02679` | 670- ROCKET BOMB (10P) 5P N.M.JYOTHI | `PKT` | ₹45.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02680` | 671- ROCKET BOMB (10P) 5P AYYANAR | `PKT` | ₹55.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02681` | 672- ROCKET BOMB (10P) 5P GANESH | `PKT` | ₹58.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02710` | 197- 30 CM GREEN SARAVANA (2 P) | `PKT` | ₹25.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02711` | 198- 30 CM RED SARAVANA (2 P) | `PKT` | ₹27.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02756` | 606- G C SPL (10 P) VENKATESH | `PKT` | ₹36.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02765` | 232- 12 CM 2 IN 1 CLASSIC(5 P) | `PKT` | ₹17.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02832` | 182- 9 CM 2 IN 1 CLASSIC(10DABBI=1BOX) | `BOX` | ₹120.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02841` | 233- 12 CM 4 IN 1 LX CLASSIC (5 P) | `PKT` | ₹22.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02852` | 607- G C SPL (10 P) T/MEENA | `PKT` | ₹56.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02885` | 580- SKY SCRAPPER DRONE MERCURY ( 5 P ) | `PCS` | ₹125.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `02897` | W 2 1/2" F. PIPE(3 PCS)AYYANAR | `PKT` | ₹225.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03089` | 183- 7 CM PLAIN M.R.P. (10 DABBI=1BOX) | `BOX` | ₹80.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03090` | 184- 7 CM COL SARAVANA(10 DABBI=1BOX) | `BOX` | ₹90.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03091` | 185- 7 CM GREEN SARAVANA (10 DABBI=1BOX | `BOX` | ₹105.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03092` | 186- 7 CM RED M.R.P. (10 DABBI=1BOX | `BOX` | ₹120.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03093` | 187- 7 CM COL VASANTHA(10 DABBI=1BOX) | `BOX` | ₹95.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03094` | 188- 7 CM PLAIN GOLD S.T.D(10DABBI=1BOX | `BOX` | ₹180.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03097` | 235- 15 CM PLAIN AB MAGIC CLASSIC (5 P) | `PKT` | ₹22.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03098` | 236- 15 CM PLAIN DLX CLASSIC(5 P) | `PKT` | ₹25.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03099` | 237- 15 CM PLAIN BOXE(2P CELLEPHO CLASSI | `PKT` | ₹26.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03100` | 238- 15 CM COL AB MAGIC CLASSIC (5 P) | `PKT` | ₹25.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03101` | 239- 15 CM COL DLX CLASSIC (5 P) | `PKT` | ₹27.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03102` | 240- 15 CM COL BOXE(2P CELLEPHONE)CLASSI | `PKT` | ₹29.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03103` | 241- 15 CM GREEN CLASSIC (5 P) | `PKT` | ₹23.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03104` | 242- 15 CM RED CLASSIC  (5 P) | `PKT` | ₹27.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03105` | 243- 15 CM 2 IN 1 CLASSIC (5 P) | `PKT` | ₹29.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03107` | 245- 15 CM 2IN1 BOXE(2P CELLEPHON CLASSI | `PKT` | ₹31.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03110` | 248- 30 CM PLAIN AB MAGIC CLASSIC (5 P) | `PKT` | ₹22.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03111` | 249- 30 CM PLAIN DLX CLASSIC (5 P) | `PKT` | ₹25.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03112` | 250- 30 CM PLAIN BOXE(2P CELLEPHO CLASSI | `PKT` | ₹26.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03175` | 581- SUPER DRONE W AYYAN( 5 PCS) | `PKT` | ₹170.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03176` | 582- HELICOPTER AYYAN ( 5PCS) | `PKT` | ₹80.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03177` | 583- HELICOPTER R. KRISHNA.( 5PCS) | `PKT` | ₹75.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03179` | 585- HELICOPTER ANIL( 5PCS) | `PKT` | ₹100.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03180` | 586- HELICOPTER SUNSHINE( 10 PCS) | `PKT` | ₹290.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03208` | 608- G C SPL (10 P) GANESH | `PKT` | ₹57.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03212` | 612- G C SPL W (10 P) I.N | `PKT` | ₹90.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03213` | 613- G C SPL (10 P) (5 P) SUNSHINE | `PKT` | ₹94.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03214` | 614- 45 CM G C SPL (10 P) COCK | `PKT` | ₹124.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03216` | 696- WHISTLING ROCKET K.M.RAJA(10P)2P | `PKT` | ₹115.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03218` | 698- WHISTLING ROCKET MERCURY(10P)2P- | `PKT` | ₹200.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03219` | 699- WHISTLING ROCKET ANIL(10P)2P- | `PKT` | ₹227.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03220` | 700- SILVER JET ROCKET S.T.D (10 P) 2 P | `PKT` | ₹225.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03221` | 701- ROHINI ROCKET S.T.D (10 P) 2 P | `PKT` | ₹227.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03222` | 702- MULTI COLOUR ROCKET MERCURY ( 6PCS) | `PKT` | ₹113.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03225` | 705- PARACHUTE ROCKET AYYAN (4 P) 2 P | `PKT` | ₹375.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03226` | 706- PARACHUTE ROCKET S.T.D ( 5 PCS) 1 | `PKT` | ₹575.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03229` | 719- 7 CM PENCIL VIRBALAJI ( 10 P ) 10 P | `PKT` | ₹20.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03230` | 720- 7 CM PENCIL T/MEENA ( 10 P ) 10 P | `PKT` | ₹24.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03231` | 721- 10 CM PENCIL VIRBALAJI ( 10 P ) 10 | `PKT` | ₹36.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03232` | 722- 10 CM PENCIL T/MEENA ( 10 P ) 10 P | `PKT` | ₹45.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03233` | 723- 12 CM PENCIL VIRBALAJI ( 10 P ) | `PKT` | ₹43.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03265` | 753- L. B. BOMB GREEN W/F (10 P) B.F.W. | `PKT` | ₹80.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03266` | 754- LALKAR BOMB GREEN W/F(10 P) B.F.W | `PKT` | ₹85.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03267` | 755- LALKAR BOMB FOIL W/F(10 P) B.F.W | `PKT` | ₹90.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03272` | 760- THUNDER BOMB GREEN (10 P) S.T.D | `PKT` | ₹130.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `03275` | 763- V.I.P BOMB GREEN S.Q (6 P) SHAKTI | `PKT` | ₹140.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04005` | 841- 7 SHOTS OTHER(5 PCS) (5P) | `BOX` | ₹65.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04006` | 842- 7 SHOTS J.K (5 PCS) (5P) | `BOX` | ₹80.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04007` | 843- 7 SHOTS MERCURY (5 PCS) (5P) | `BOX` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04008` | 844- 7 SHOTS I.N (5 PCS) (5P) | `BOX` | ₹136.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04009` | 845- 7 SHOTS ANIL (5 PCS) (5P) | `BOX` | ₹170.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04012` | 848- 7 SHOTS OTHER (10 PCS) | `BOX` | ₹180.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04014` | 850- 7 SHOTS I. N.(10 PCS | `BOX` | ₹270.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04015` | 851- 7 SHOTS MERCURY(10 PCS) | `BOX` | ₹250.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04016` | 852- 7 SHOTS SIGNAL ROCKET COCK(15 PCS) | `BOX` | ₹500.00 | **15** | 1 | [ ] Approve (15)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04028` | 1060- COL SMOKE DHUA 5COL(5P)SUP.KING | `PKT` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04045` | 1088- YOGESH BLACK GUN REX ( 12 PCS) | `PKT` | ₹7.00 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04046` | 1089- TOM COLOUR YUG ( 12 PCS ) | `PCS` | ₹7.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04047` | 1090- V-30 COLOUR VISHNU (12 PCS) | `PCS` | ₹12.10 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04048` | 1091- ROBOT BLACK S-61 SOM (12 PCS) | `PCS` | ₹12.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04049` | 1092- V-301 COLOUR VISHNU ( 10 PCS) | `PCS` | ₹12.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04050` | 1093- V-35 BLACK VISHNU(10 PCS) | `PCS` | ₹15.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04051` | 1094- 86 BLACK SOM(12 PCS) | `PCS` | ₹17.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04052` | 1095- 86 COLOUR SOM (12 PCS) | `PCS` | ₹23.00 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04053` | 1096- NICE BLACK SOM(12 PCS) | `PCS` | ₹18.00 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04054` | 1097- NICE COLOUR SOM (12 PCS) | `PCS` | ₹23.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04055` | 1098- VATMAN BLACK SOM (12 PCS) | `PCS` | ₹21.00 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04056` | 1099- VATMAN COLOUR SOM (12 PCS) | `PCS` | ₹26.00 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04057` | 1100- DOLPHIN BLACK SOM(6 PCS) | `PCS` | ₹29.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04058` | 1101- DOLPHIN COLOUR SOM (6 PCS) | `PCS` | ₹37.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04059` | 1102- TIGER BLACK SOM(12 PCS) | `PCS` | ₹61.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04060` | 1103- TIGER COLOUR SOM (12 PCS) | `PCS` | ₹67.50 | **12** | 1 | [ ] Approve (12)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04062` | 1105- SPIDER BLACK SOM ( 3 PCS) | `PCS` | ₹89.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04063` | 1106- SPIDER COLOUR SOM  ( 3 PCS) | `PCS` | ₹97.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04064` | 1107- CAMANDO BLACK SOM ( 3 PCS) | `PCS` | ₹102.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04065` | 1108- CAMANDO COLOUR SOM ( 3 PCS) | `PCS` | ₹109.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04094` | 1084- PATANG BALLOON (10 P) KING'S | `BOX` | ₹16.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04194` | 117- GEM MEGA ( 10 PKT ) 3 COL SHANTHI | `PKT` | ₹145.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04195` | 118- WONDER CRACKLING ( 10 PCS) SHANTHI | `PKT` | ₹210.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04207` | 189- 7 CM COL GOLD S.T.D(10DABBI=1BOX) | `BOX` | ₹150.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04236` | 213- 12 CM 5 IN 1 (5 PKT) CHANDRA | `PKT` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04239` | 216- 15 CM  50 X 50 (5 PCS)CHANDRA | `PKT` | ₹35.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04246` | 251- 30 CM COL AB MAGIC CLASSIC (5 P) | `PKT` | ₹25.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04247` | 252- 30 CM COL DLX CLASSIC (5 P) | `PKT` | ₹27.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04248` | 253- 30 CM COL BOXE(2P CELLEPHON CLASSIC | `PKT` | ₹29.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04249` | 254- 30 CM GREEN CLASSIC (5 P) | `PKT` | ₹23.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04251` | 256- 30 CM RED CLASSIC (5 P) | `PKT` | ₹27.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04253` | 258- 30 CM 2 IN 1 CLASSIC (5 P) | `PKT` | ₹27.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04254` | 259- 30 CM 2 IN 1 BOXE(2P CELLEPHO CLASS | `PKT` | ₹29.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS) | `BAG` | ₹11.00 | **50** | 1 | [ ] Approve (50)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04310` | 168- GOLD BIJALI COCK (50 PCS) | `BAG` | ₹35.50 | **50** | 1 | [ ] Approve (50)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04311` | 169- GOLD BIJALI OTHER (100 PCS) | `BAG` | ₹20.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS) | `BAG` | ₹21.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04313` | 171- GOLD BIJALI GIANT OVEEYA(100 PCS) | `BAG` | ₹44.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04314` | 172- GOLD BIJALI APPLE(100 PCS) | `BAG` | ₹27.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04315` | 173- GOLD BIJALI SRIPATHI(100 PCS) | `BAG` | ₹30.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04316` | 174- GOLD BIJALI AYYANAR(100 PCS) | `BAG` | ₹37.50 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04317` | 175- GOLD BIJALI COCK(100 PCS ) | `BAG` | ₹67.00 | **100** | 1 | [ ] Approve (100)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04341` | 296- 28 CHORSA TURKEY  RAJLAXMI(50P= 1 B | `PKT` | ₹13.50 | **50** | 1 | [ ] Approve (50)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04342` | 297- 28 CHORSA (25PCS) VELVAN | `PKT` | ₹14.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04343` | 298- 32 CHORSA MIX RED-GOA SUN(50P=1BUND | `PKT` | ₹12.50 | **50** | 1 | [ ] Approve (50)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04346` | 301- 28 GAINT CHORSA (25 P) K.R.K | `PKT` | ₹17.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04347` | 302- 28 GAINT CHORSA (25 P) AJITKUMAR | `PKT` | ₹18.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04348` | 303- 28 GAINT CHORSA (25 P) SELVI | `PKT` | ₹19.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04349` | 304- 28 GAINT CHORSA (25 P)DURGESH | `PKT` | ₹19.50 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04350` | 305- 28 SUP GAINT CHORSA N.M.JYOTHI(25P) | `PKT` | ₹24.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04351` | 316- 50 DLX RAGURAM ( 5 P) | `PKT` | ₹52.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04352` | 317- 50 DLX GANESH DURAI( 5 P) | `PKT` | ₹80.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04370` | 342- 3 1/2 GREEN PARROT W/F VELVAN (10 P | `PKT` | ₹15.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04371` | 343- 3 1/2  PEACOCK 9 CM  S.T.D( 10 P | `PKT` | ₹24.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04372` | 344- 3 1/2 DLX KURVI GANESH (10 P) | `PKT` | ₹25.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04373` | 345- 3 1/2 GREEN PARROT W/F B.F.W (10 P) | `PKT` | ₹25.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04374` | 346- 3 1/2 JAWAN AYYAN (10 P) | `PKT` | ₹27.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04377` | 349- 4  MIX LABEL DURGESH (10 P) | `PKT` | ₹14.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04378` | 350- 4 GREEN PARROT SADA VELAVAN(10 PCS) | `PKT` | ₹14.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04379` | 351- 4 GREEN PARROT SRIPATHI (10 P) | `PKT` | ₹16.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04380` | 352- 4  LADY T/MEENA  (10 P) | `PKT` | ₹16.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04381` | 353- 4 MICKEY MOUSE BALAJI( 10 P) | `PKT` | ₹16.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04382` | 354- 4 GREEN PARROT VELAVAN (10 P) W/F | `PKT` | ₹18.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04383` | 355- 4 ELEPHANT I.N (10 P) | `PKT` | ₹18.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04384` | 356- 4 GREEN PARROT SADA PONMALAR(10P) | `PKT` | ₹19.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04385` | 357- 4  MIX LABEL AYYANAR (10 P) | `PKT` | ₹21.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04386` | 358- 4 PARROT COCK (10 P) | `PKT` | ₹22.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04387` | 359- 4 GREEN PARROT W/F V.F.I(10 P) | `PKT` | ₹32.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04388` | 360- 4 KING AYYAN (10 P) | `PKT` | ₹32.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04389` | 361- 10 CM PEACOCK COLF S.T.D( 10 P) | `PKT` | ₹34.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04390` | 362- 4 GREEN PARROT W/F B.F.W (10 P) | `PKT` | ₹35.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04400` | 372- 4 DLX PARROT W/F ( 10 P)VELAVAN | `PKT` | ₹29.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04405` | 377- 4 SUP DLX MIX LABEL(10P)AYYANAR | `PKT` | ₹27.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04411` | 383- 5 DLX JALLIKATTI DURGESH (10P) | `PKT` | ₹27.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04413` | 385- 5 DLX  ELEPHANT(10P) JAYMURGAN | `PKT` | ₹31.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04423` | 395- 4 SUP DLX GOLD KARUDA (10P) AYYANAR | `PKT` | ₹35.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04424` | 396- 4 SUP DLX GOLD ELEPHANT (10P)I.N | `PKT` | ₹57.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04428` | 403- 2 SOUND DHAMAKA ANIL (10P) | `PKT` | ₹32.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04429` | 404- 2 SOUND DHAMAKA S.T.D (10P) | `PKT` | ₹36.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04430` | 405- 2 SOUND DHAMAKA MERCURY (10P) | `PKT` | ₹42.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04433` | 408- 3 SOUND DHAMAKA NM JYOTHI(10P) | `PKT` | ₹28.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04434` | 409- 3 SOUND DHAMAKA RATHANAA(10P) | `PKT` | ₹34.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04435` | 410- 3 SOUND DHAMAKA I.N. (10P) | `PKT` | ₹40.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04508` | 500- FLOWER POTS DLX (10 P) OVEEYA | `PKT` | ₹150.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04509` | 501- FLOWER POTS DLX (10 P) GOVINDA | `PKT` | ₹245.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04510` | 502- FLOWER POTS COL KOTI DLX(10P)ANIL | `PKT` | ₹375.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04511` | 503- FLOWER POTS DLX COL KOTI(10P)SONNY | `PKT` | ₹350.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04512` | 504- FLOWER POTS DLX COL KOTI (10 P)I.N | `PKT` | ₹355.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04513` | 505- FLOWER POTS MEGA DLX (10 P)MERCURY | `PKT` | ₹290.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04514` | 506- F P MEGA DLX  (10 P) VIRABALAJI | `PKT` | ₹420.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04518` | 510- FLOWER POT DLX (5 PCS )GOVINDA | `PKT` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04519` | 511- FLOWER POT DLX (5 PCS )MERCURY | `PKT` | ₹175.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04520` | 512- FLOWER POT DLX (5 PCS )S.T.D | `PKT` | ₹240.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04563` | 563- OMG POTS ANAR MERCURY ( 5 PCS ) | `BOX` | ₹315.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04564` | 564- CROWN JEWEL'S ANAR MERCURY( 5 PCS) | `BOX` | ₹625.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04574` | 615- G C SPL (10 P) (5 P) S.T.D | `PKT` | ₹150.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04576` | 617- G C SPL SPINNER WHEEL(10P) AYYANAR | `PKT` | ₹75.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04580` | 621- G C DLX  (10 P) 5 P VENKATESH | `PKT` | ₹75.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04581` | 622- G C DLX  (10 P) 5 P T/MEENA | `PKT` | ₹95.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04583` | 624- G C DLX  (10 P) 5 P MERCURY | `PKT` | ₹125.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04584` | 625- G C DLX  (10 P) 5 P COLOUR W JENIS | `PKT` | ₹115.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04585` | 626- G C DLX  W (10 P) 5 P I.N | `PKT` | ₹130.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04586` | 627- G C DLX  (10 P) 5 P GANESH | `PKT` | ₹140.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04587` | 628- G C DLX  (10 P) 5 P ANIL | `PKT` | ₹160.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04588` | 629- G C DLX  (10 P) 5 P SUNSHINE | `PKT` | ₹165.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04589` | 630- G C DLX  (10 P) 5 P S.T.D | `PKT` | ₹195.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04590` | 631- 70 CM G C DLX  (10 P) 5 P COCK | `PKT` | ₹210.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04592` | 633- G C DLX  U.V. BOX (10 P) 5 P I.N | `PKT` | ₹135.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04593` | 634- G C DLX  PLASTIC (10 P) 5 P JAGUAR | `PKT` | ₹110.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04595` | 636- G C DLX SPINNER ( 10 P )AYYANAR | `PKT` | ₹160.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04596` | 637- G C DLX  SPINNER(10P) 5P CORONATION | `PKT` | ₹175.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04600` | 641- G C SUP DLX  (10 P) 5 P MERCURY | `PKT` | ₹190.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04601` | 642- G C SUP DLX  (10 P) 5 P S.T.D | `PKT` | ₹215.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04615` | 652- MASKA CHASKA I. N ( 5 P ) | `PKT` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04618` | 655- MUSICAL WHEEL MERCURY (5 PCS) ( 2 P | `PKT` | ₹102.50 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04619` | 656- WHISTLING WHEEL COCK (5 PCS) (10P) | `PKT` | ₹125.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04620` | 657- WHIZZ WHEEL S.T.D (5 PCS) (10P) | `PKT` | ₹139.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04621` | 658- TITANIC WHEEL DURGESH ( 5P) | `PKT` | ₹130.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04622` | 659- TOP TUCKER AYYAN ( 5 P) | `PKT` | ₹80.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04626` | 663- SPINNER BAMBARA LAVANYA ( 10 P ) | `PKT` | ₹85.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04627` | 664- LOTUS WHEEL (5 PCS) AYYAN | `PKT` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04628` | 665- STAR WHEEL (10 PCS) AYYAN | `PKT` | ₹156.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04634` | 673- ROCKET BOMB (10P) 5P S.T.D | `PKT` | ₹144.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04636` | 675- SILVER ROCKET(10P)5P AYYANAR | `PKT` | ₹75.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04639` | 678- LUNIK ROCKET (10 P) 2P T/MEENA | `PKT` | ₹80.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04640` | 679- EXPO ROCKET (10 P) 2P GANESH | `PKT` | ₹85.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04641` | 680- LUNIK ROCKET (10 P) 2P MERCURY | `PKT` | ₹112.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04643` | 682- LUNIK ROCKET (10 P) 2P AYYANAR | `PKT` | ₹130.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04646` | 685- 2 SOUND ROCKET (10 P) 2P T/MEENA | `PKT` | ₹82.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04647` | 686- 2 SOUND ROCKET (10 P) 2P AYYANAR | `PKT` | ₹120.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04649` | 688- 2 SOUND ROCKET (10 P) 2P GANESH | `PKT` | ₹125.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04650` | 689- 2 SOUND ROCKET (10 P) 2P MERCURY | `PKT` | ₹132.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04679` | 724- 15 CM PENCIL VIRBALAJI ( 10 P ) | `PKT` | ₹53.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04680` | 725- 18 CM PENCIL VIRBALAJI ( 10 P ) | `PKT` | ₹68.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04684` | 729- MULTI COLOUR CANDLE S.T.D (10P) 5P | `PKT` | ₹99.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04685` | 730- WHISTLING PIPER SONY ( 5 P ) | `PKT` | ₹285.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04687` | 732- HAND SHOWER MARIESWARAN ( 3 P ) | `PKT` | ₹185.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04910` | 1008- 18 HAND SHOT ( 2 PCS ) M.INDIA | `BOX` | ₹400.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04914` | 1012- 5 KA DHUM ( 5 P) ANIL | `BOX` | ₹155.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04915` | 1013- SKY SHOT (10 P ) COCK | `BOX` | ₹86.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04918` | 1016- TOP-TEN ( 10 P ) COCK | `BOX` | ₹350.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04924` | 1022- 2 1/2 F. P. (3P)6COL MIX W THUNIVU | `BOX` | ₹175.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04925` | 1023- 2 1/2 F. P. (3P)6COL MIX U BALAJI | `BOX` | ₹180.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04926` | 1024- 2 1/2 F. P. (2P)6COL MIX U | `BOX` | ₹190.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04927` | 1025- 2 1/2 F. P. (3PCS) MIX COL AYYANAR | `BOX` | ₹225.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04928` | 1026- 3 FANCY PIPE (2 PCS) SONY | `BOX` | ₹850.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04929` | 1027- 2 1/2 F. P. (3P)MIX COL 7 STEP I.N | `BOX` | ₹500.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04930` | 1028- 2 1/2 F. P. (3P)3 IN 1 BLOSSOM COC | `BOX` | ₹422.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04931` | 1029- PARACHUTE NIGHTOUT ( 3 P ) COCK | `BOX` | ₹400.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04932` | 1030- 2 1/2 F. P.LONG(3P)MIX COL.MERCURY | `BOX` | ₹455.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04941` | 1039- 3  FANCY PIPE (2P) MIX COL MERCURY | `BOX` | ₹600.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `04942` | 1040- 3  FANCY PIPE (3P) MIX COL MERCURY | `BOX` | ₹940.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05004` | 1115- PUBG GUN ( 5 P X 1 PKT )T PANDYAN | `BOX` | ₹90.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05020` | 1133- COLD PYRO BLACK R.R.R ( 10 P) | `BOX` | ₹110.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05021` | 1134- COLD PYRO YELLO BOX TAIWIN( 10 P) | `BOX` | ₹120.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05023` | 1136- NAAGARA FALLS ( 25 PCS) P.G | `BOX` | ₹1200.00 | **25** | 1 | [ ] Approve (25)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05402` | 513- FLOWER POTS SUP DLX (2 P)SUPER | `PKT` | ₹65.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05403` | 514- FLOWER POTS SUP DLX (2 P) GOVINDA | `PKT` | ₹75.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05404` | 515- FLOWER POTS RANG BARAAT (2 P)COCK | `PKT` | ₹405.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05426` | 692- 3 SOUND ROCKET (10 P) 2P T/MEENA | `PKT` | ₹85.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05427` | 693- 3 SOUND ROCKET (10 P) 2P AYYANAR | `PKT` | ₹135.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05428` | 694- 3 SOUND ROCKET (10 P) 2P GANESH | `PKT` | ₹140.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05459` | 1051- 4"  F. P.(2P) 3 COL. MIXED MERCURY | `BOX` | ₹860.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05460` | 1052- 4"  F. P.(2P) 8 COL MIX UV BOX I.N | `BOX` | ₹1100.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05461` | 1053- 4"  DLX F.P.(2P) 12 COL.MIXED SONY | `BOX` | ₹950.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05462` | 1054- 4"  F.P.(2P)DOUBLE BALL UV.BOX I.N | `BOX` | ₹1230.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05950` | W COL SMOKE DHUA  COL (5 P) SUP.KING | `BOX` | ₹120.00 | **5** | 1 | [ ] Approve (5)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `05953` | W 4 F. PIPE (2 PCS)  I. N. | `BOX` | ₹900.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06048` | W TOP- TEN ( 10 P ) COCK | `BOX` | ₹285.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06049` | W 1 1/4 POGO MIXED ( 10 P) 2 PCS AYYAN | `BOX` | ₹58.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06053` | W 2 1/2 F PIPE MIX UV BOX ( 3 P) | `BOX` | ₹165.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06054` | W 2 1/2 F PIPE  BALAJI ( 3 P) | `BOX` | ₹175.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06056` | W 2 1/2 F PIPE MEGAL ( 3 P ) MERCURY | `BOX` | ₹445.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06057` | W 3 F PIPE LIGHT AND HOT MIX ( 2P )AN | `BOX` | ₹685.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06058` | W 3 F PIPE BIG SIZZ MIXD ( 2P ) MERCU | `BOX` | ₹580.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06068` | W 3 1/2 F P DOUBLE BALL (2 P) SONY | `BOX` | ₹750.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06072` | W 4 F P 3 COL MIXED ( 2 P) W MERCURY | `BOX` | ₹850.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06073` | W 4 F P 3 COL MIXED ( 2 P) W  I.N | `BOX` | ₹900.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06074` | W 4 F P DLX 15 COL MIXED ( 2 P)  SONY | `BOX` | ₹900.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06092` | W 7 SHOT ( 10 P ) MERCURY | `BOX` | ₹210.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06098` | W 2 1/2" F. PIPE 2 IN 1 ( 2 P )CORNATION | `BOX` | ₹200.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06099` | W 18 SHOT ROMANCANDLE ( 2P) | `BOX` | ₹400.00 | **2** | 1 | [ ] Approve (2)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06134` | W COLD PYRO R&G BOX 3.M.35.S (6P) | `BOX` | ₹80.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06135` | W COLD PYRO YELLO BOX 3.M.30.S(10P) | `BOX` | ₹120.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06156` | W 2 1/2 F PIPE  MIX BIG  ( 3 P) | `BOX` | ₹375.00 | **3** | 1 | [ ] Approve (3)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06157` | W COLD PYRO BOX 3.M.35.S (6P) | `BOX` | ₹100.00 | **6** | 1 | [ ] Approve (6)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06171` | 129- KIT-KAT(10 P)YUVA | `PKT` | ₹18.50 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06173` | 131- KIT-KAT (10 P) RAJHARISH | `PKT` | ₹20.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06174` | 132- KIT-KAT(10 P)U.V.BOX VETRI | `PKT` | ₹21.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |
| `06175` | 133- KIT-KAT BIG(10 P)TIRUMINIK | `PKT` | ₹32.00 | **10** | 1 | [ ] Approve (10)<br>[ ] Change: ___<br>[ ] Reject (1) | |

---

## Section 3: High-Risk / Flagged Commercial Edge Cases (62 Products)

These items require specific business policy decisions due to missing packaging tags, large bundle sizes, or ambiguous packaging units:

| Code | Product Description | FoxPro UOM | Rate (₹) | Suggested | Enforced | Commercial Risk / Flag | Action Required |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `00491` | 550- SADA MATKA ANAR OTHER (100P) | `PCS` | ₹15.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `00866` | 158- STRIPPED BIJALI ROSE(50 PCS)10 BAG | `BAG` | ₹11.50 | 50 | **1** | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02122` | 450- FLOWER POTS BIG K.V.S | `PKT` | ₹40.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02152` | 1117- RING CAPS (1OOPKT= 1 BOX)RACHNA | `PKT` | ₹6.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02153` | 1118- RING CAPS (1OOPKT= 1 BOX) AYYAN | `PKT` | ₹6.50 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02154` | 1119- RING CAPS (1OOPKT= 1 BOX)GOKUL | `PKT` | ₹7.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02155` | 1120- RING CAPS (1OOPKT= 1 BOX)COCK | `PKT` | ₹7.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02764` | 451- FLOWER POTS BIG N.M JYOTHI | `PKT` | ₹50.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02779` | 286- FANCY SPARKLERS LOLLY POP | `PKT` | ₹125.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `02783` | 288- SPINNIG SPARKLERS KALLIAMAL | `PKT` | ₹190.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04309` | 167- GOLD BIJALI A.G.S (50 PCS) | `BAG` | ₹11.00 | 50 | **1** | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04310` | 168- GOLD BIJALI COCK (50 PCS) | `BAG` | ₹35.50 | 50 | **1** | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04311` | 169- GOLD BIJALI OTHER (100 PCS) | `BAG` | ₹20.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04312` | 170- GOLD BIJALI A.G.S(100 PCS) | `BAG` | ₹21.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04313` | 171- GOLD BIJALI GIANT OVEEYA(100 PCS) | `BAG` | ₹44.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04314` | 172- GOLD BIJALI APPLE(100 PCS) | `BAG` | ₹27.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04315` | 173- GOLD BIJALI SRIPATHI(100 PCS) | `BAG` | ₹30.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04316` | 174- GOLD BIJALI AYYANAR(100 PCS) | `BAG` | ₹37.50 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04317` | 175- GOLD BIJALI COCK(100 PCS ) | `BAG` | ₹67.00 | 100 | **1** | High pack multiple (100) auto-extracted. Verify whether sold per packet (in multiples of 100) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04318` | 176- BASKET BOMB SINGADA RAVINDRA(10 BAG | `BAG` | ₹62.00 | 1 | **1** | BAG packaging item with suggested multiple 1. Confirm outer bag case size. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04341` | 296- 28 CHORSA TURKEY  RAJLAXMI(50P= 1 B | `PKT` | ₹13.50 | 50 | **1** | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04343` | 298- 32 CHORSA MIX RED-GOA SUN(50P=1BUND | `PKT` | ₹12.50 | 50 | **1** | High pack multiple (50) auto-extracted. Verify whether sold per packet (in multiples of 50) or per bundle. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04460` | 452- FLOWER POTS BIG T/MEENA | `PKT` | ₹55.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04461` | 453- FLOWER POTS BIG AYYANAR | `PKT` | ₹68.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04462` | 454- FLOWER POTS BIG OVEEYA | `PKT` | ₹78.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04463` | 455- FLOWER POTS BIG MERCURY | `PKT` | ₹80.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04464` | 456- FLOWER POTS BIG COCK | `PKT` | ₹124.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04465` | 457- FLOWER POTS BIG S.T.D | `PKT` | ₹135.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04468` | 460- FLOWER POTS SPECIAL G.P.M | `PKT` | ₹45.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04469` | 461- FLOWER POTS SPECIAL K.V.S | `PKT` | ₹45.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04470` | 462- FLOWER POTS SPECIAL SRI SAI | `PKT` | ₹50.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04471` | 463- FLOWER POTS SPECIAL NM JYOTHI | `PKT` | ₹60.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04472` | 464- FLOWER POTS SPECIAL ANBARSI | `PKT` | ₹60.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04473` | 465- FLOWER POTS SPECIAL T/MEENA | `PKT` | ₹65.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04474` | 466- FLOWER POTS SPECIAL AYYANAR | `PKT` | ₹102.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04475` | 467- FLOWER POTS SPECIAL OVEEYA | `PKT` | ₹105.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04476` | 468- FLOWER POTS SPECIAL MERCURY | `PKT` | ₹106.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04477` | 469- FLOWER POTS SPECIAL I.N | `PKT` | ₹110.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04478` | 470- FLOWER POTS SPECIAL S.T.D | `PKT` | ₹180.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04479` | 471- FLOWER POTS SPECIAL COCK | `PKT` | ₹220.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04482` | 474- FLOWER POTS ASHOKA K.V.S | `PKT` | ₹55.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04483` | 475- FLOWER POTS ASHOKA SRI SAI | `PKT` | ₹62.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04484` | 476- FLOWER POTS ASHOKA ANBARSI | `PKT` | ₹69.50 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04485` | 477- FLOWER POTS ASHOKA NM JYOTHI | `PKT` | ₹70.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04486` | 478- FLOWER POTS ASHOKA T/MEENA | `PKT` | ₹83.50 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04487` | 479- FLOWER POTS ASHOKA SRIPATHI | `PKT` | ₹85.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04488` | 480- FLOWER POTS ASHOKA OVEEYA | `PKT` | ₹140.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04489` | 481- FLOWER POTS ASHOKA MERCURY | `PKT` | ₹150.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04493` | 485- FLOWER POTS GAINT AYYANAR | `PKT` | ₹150.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04494` | 486- FLOWER POTS GAINT I. N. | `PKT` | ₹155.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04495` | 487- FLOWER POTS GAINT MERCURY | `PKT` | ₹202.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04496` | 488- FLOWER POTS GAINT COL.KOTI MERCURY | `PKT` | ₹250.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04497` | 489- FLOWER POTS GAINT S.T.D | `PKT` | ₹325.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04499` | 491- FLOWER POTS COL KOTI UV.BOX OTHER | `PKT` | ₹110.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04500` | 492- FLOWER POTS COL KOTI UV.BOX ROJAPOO | `PKT` | ₹135.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04501` | 493- FLOWER POTS COL KOTI UV.BOX RAJLAXM | `PKT` | ₹140.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04502` | 494- FLOWER POTS COL KOTI UV.BOX T/MEENA | `PKT` | ₹150.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04503` | 495- FLOWER POTS COL KOTI UV.BOX GOVINDA | `PKT` | ₹165.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `04504` | 496- FLOWER POTS COL KOTI AYYANAR | `PKT` | ₹200.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `05960` | W SPARKULAR MACHINE POWDER | `PKT` | ₹910.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `06136` | W SPARKULAR GUN SADI-(CELL) | `BOX` | ₹150.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |
| `06137` | W SPARKULAR GUN PENCIL-(CELL) | `BOX` | ₹200.00 | 1 | **1** | Multi-pack category (sparkler/chakkar/pot) with no parenthetical pack tag; safely defaulted to 1. Verify if inner box packing (e.g. 10 or 5) is required for wholesale orders. | [ ] Set Pack: ___<br>[ ] Keep 1 |

---

## Section 4: Business Owner Sign-Off Block

I have reviewed the packaging multiples and rule enforcements in this worksheet. The approved rules may be merged into `catalog_pack_rules.json` to govern wholesale validation for the upcoming fireworks sales season.

- **Reviewed By (Print Name):** _______________________________________
- **Signature:** _____________________________________________________
- **Date:** _________________________
- **Showroom Location:** _____________________________________________
