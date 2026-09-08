# Legacy-Only Showroom Navigation Architecture (Phase 2.6)
**System:** RAM FATAKA CENTER Wholesale & Retail POS  
**Data Source:** Visual FoxPro 6.0 Tables Exclusively (`COMPMST.DBF`, `ITEMMST.DBF`)  
**Design Principle:** Zero External Metadata — 100% Replication of Showroom Staff Selling Workflow  
**Document Status:** Production Design Specification

---

## 1. Executive Summary

This specification establishes a **legacy-only tablet navigation architecture** that mirrors the exact physical layout of the showroom and the traditional paper order pad used by sales staff at RAM FATAKA CENTER.

By analyzing the legacy database (`D2627`), we discovered that **`COMPMST.DBF`** (Company Master) is actually the master sequence for **Showroom Product Categories**, ordered by the serial number **`COMPMST.SR` (1 to 43)**. Furthermore, the 1,091 active sellable items in **`ITEMMST.DBF`** carry paper catalog item numbers prefixed into their names (e.g. `111-`, `178-`, `443-`, `588-`, `735-`, `840-`) that strictly align with these 43 showroom sections.

By organizing the tablet around `COMPMST.SR` and these embedded catalog numbers, the Android tablet POS functions as an **accelerated digital order pad**, allowing salesmen to guide buyers through showroom aisles with zero learning curve.

---

## 2. Showroom Section Hierarchy

The browsing hierarchy is derived strictly from FoxPro fields:

```
Level 1: Showroom Section (COMPMST.DBF)
         - Name: COMPMST.NAME (e.g. "FLOWER POTS COL KOTI, MEGA DLX")
         - Sort Key: COMPMST.SR (1 .. 43)
         - Link Key: COMPMST.CODE (e.g. "18")
                     │
                     ▼
Level 2: Product List (ITEMMST.DBF)
         - Filter: ITEMMST.CCODE == COMPMST.CODE
         - Filter: LEN(NAME) > 5 AND SRATE > 0 (Exclude placeholders)
         - Sort Key: Legacy Item Prefix (e.g. 443-, 444-, 445-)
         - Display: ITEMMST.CODE, ITEMMST.NAME, ITEMMST.PACK, ITEMMST.SRATE, ITEMMST.CQTY
                     │
                     ▼
Level 3: Quantity Input & Validation
         - Price: ITEMMST.SRATE (Wholesale Unit Rate)
         - Stock Badge: ITEMMST.CQTY (Available stock)
         - Step: +1 / +5 / +10 or Direct Numeric Keypad
```

---

## 3. Complete Showroom Section Map (Ordered by `COMPMST.SR`)

Below is the verified layout of all 42 active showroom sections in the database:

| Section # (`SR`) | Section Code (`CCODE`) | Showroom Category Title (`COMPMST.NAME`) | Active Items | Sample Catalog Items |
|:---:|:---:|---|:---:|---|
| **01** | `1` | `ROLL AND DOT CAPS` | 3 | `111- ROLL CAPS AGNI`, `112- ROLL CAPS S.T.D.` |
| **02** | `2` | `MATCH BOX` | 5 | `114- MATCH BOX SHANTHI`, `115- MATCH BOX RAYAL` |
| **03** | `3` | `ASST CARTOON & RAIL` | 5 | `119- ASST CARTOON(10 PCS)`, `120- BEN TEN(25P)` |
| **04** | `4` | `SERPANTS & NAGGOLI` (Snake Eggs) | 14 | `124- BIG NAGGOLI BLACK`, `125- BIG NAGGOLI RED` |
| **05** | `5` | `9 CM SPARKLERS` | 14 | `178- 9 CM PLAIN INDRA`, `179- 9 CM COL INDRA` |
| **06** | `6` | `SARAVANA SPARKLERS` (10 cm) | 29 | `192- 10 CM PLAIN LEO`, `193- 10 CM GREEN BHAWAN` |
| **07** | `7` | `CLASSIC SPARKLERS` (10 cm Deluxe) | 55 | `221- 10 CM PLAIN CLASSIC`, `222- 10 CM COL CLASSIC` |
| **08** | `9` | `ASOK SPARKLERS` (10 cm Standard) | 14 | `276- 10 CM PLAIN ASOK`, `277- 10 CM COL ASOK` |
| **09** | `11` | `RED, STRIPPED, GOLD BIJALI & BASKET BOMB` | 31 | `147- RED BIJALI (50 PCS)`, `148- RED BIJALI ROSE` |
| **10** | `12` | `10 CHORSA` (Small Crackers) | 4 | `290- 10 CHORASA MUNNA`, `291- 10 GAINT JAWAN` |
| **11** | `13` | `28 -CHORSA & 28-GAINT CHORSA` | 15 | `293- 16 CHORSA B GROUP`, `294- 28 CHORSA K.R.K` |
| **12** | `14` | `2 3/4 , 4' DELUXE PATALA` | 21 | `308- 20 DLX KING GANESH`, `309- 20 DLX BALAJI` |
| **13** | `15` | `ONE SOUND DHAMAKA` (Sound Crackers) | 70 | `329- 2' PARROT AYYANAR`, `330- 2 3/4 KURVI DURGESH` |
| **14** | `16` | `TWO & THREE SOUND DHAMAKA` | 14 | `399- 2 SOUND DHAMAKA`, `400- 2 SOUND DHAMAKA` |
| **15** | `17` | `GULAB KAMAL ONE SOUND DHAMAKA` | 30 | `413- 2 LXM DHAMAKA GENIUS`, `416- 3 1/2 DHAMAKA` |
| **16** | `18` | `FLOWER POTS COL KOTI, MEGA DLX, SUP DLX` | 74 | `443- FLOWER POTS SMALL`, `444- FLOWER POTS RAJLAXMI` |
| **17** | `19` | `FANCY FLOWER POTS MIXED` (Fountains) | 29 | `517- TRI COL FOUNTAIN`, `520- TRI COL COCK` |
| **18** | `20` | `COL WHITH-MAGIC WHIP` | 3 | `574- CRACKLING EXPRESS WHIP`, `575- MAGIC WHIP` |
| **19** | `21` | `FANCY FLOWER POTS- PEACOCK DANCN` | 4 | `546- PEACOCK DANCE VENKATESH`, `547- PEACOCK DURGESH` |
| **20** | `22` | `COLOUR - DANCING BUTTERFLY` | 7 | `567- DANCING BUTTERFLY R/G`, `568- DANCING BUTTERFLY` |
| **21** | `23` | `PHOTO FLASH / HELICOPTER / DRONE` | 11 | `577- MERCURY FLASH`, `578- PHOTO FLASH VENKATESH` |
| **22** | `24` | `FANCY MATAKA ANAR` | 17 | `550- SADA MATKA ANAR`, `551- MINI PEARL GUDIYA` |
| **23** | `25` | `GROUND CHAKKAR BIG, ASHOKA, SPL, DLX` | 56 | `588- G C BIG T/MEENA`, `589- G C BIG GANESH` |
| **24** | `26` | `FANCY - CHAKKAR / WHEELS / SPINNERS` | 22 | `644- COCKTAL SPINER`, `645- DISCO WHEEL GAYATHRI` |
| **25** | `27` | `ROCKETS BOMB, LUNIK ROCKETS, 2 & 3 SOUND` | 30 | `666- BABY ROCKET RAJ LAXMI`, `667- COLOUR ROCKET` |
| **26** | `28` | `FANCY ROCKETS` (Whistling / Sound) | 11 | `696- WHISTLING ROCKET K.M.RAJA`, `697- WHISTLING UV` |
| **27** | `29` | `TWINKLING STAR 18" & 48" & JIL JIL` | 12 | `707- 18 T STAR D/VADIVEL`, `708- 18 T STAR SRIPATHI` |
| **28** | `30` | `PENCILS & FANCY TORCHES` | 16 | `719- 7 CM PENCIL VIRBALAJI`, `720- 7 CM PENCIL T/MEENA` |
| **29** | `31` | `JEE BOOM BAA & CHIT PUT, GANGA JAMUNA` | 9 | `138- GANGA JAMUNA SRI PATHI`, `139- GANGA JAMUNA` |
| **30** | `32` | `ATOM BOMB` (Bullet, Hydro, Classic) | 47 | `735- BULLET BOMB MINI`, `740- HYDRO BOMB GREEN` |
| **31** | `33` | `GARLAND & LAR` (100 to 10,000 Crackers) | 58 | `782- 100 LAR JAYEM`, `785- 1000 LAR JAYEM` |
| **32** | `34` | `SHOTS & MULTISHOTS` (6, 12, 30, 60, 120) | 151 | `840- 6 SHOTS ROYAL SALUTE`, `902- 30 SHOT MULTI` |
| **33** | `35` | `F.P ALL FESTIVALS - MEGA SHOTS` | 67 | `991- 25 SHOT 5 DIFF S.T.D`, `992- 30 SHOT WOW STAR` |
| **34** | `36` | `COLOUR DHUA` (Smoke & Snow Sprays) | 7 | `1058- SNOW SPRAY WHITE`, `1060- COLOUR SMOKE 5 COL` |
| **35** | `37` | `CONFETTI & PAPER SHOTS` | 9 | `1065- HAND RIBBON PAPER`, `1066- 40 CM PARTY POPPER` |
| **36** | `38` | `POP - POP` | 13 | `1074- POP POP MULTI COLOUR`, `1075- POP POP MULTI` |
| **37** | `39` | `GUNS & PISTOLS` | 22 | `1087- BULLET ROCKET YUG`, `1088- YOGESH BLACK GUN` |
| **38** | `40` | `8 SHOT'S MISSILE GUN & FANCY GUN` | 8 | `1109- MISSILE GUN YUG`, `1110- MISSILE GUN DY787` |
| **39** | `41` | `RING CAPS AND MISSILE` | 7 | `1117- RING CAPS RACHNA`, `1118- RING CAPS AYYAN` |
| **40** | `42` | `ALL FESTIVALS & EVENT FANCY ITEM` | 37 | `1124- CUTTING PAPER M-COL`, `1125- CUTTING SPL COL` |
| **41** | `43` | `NO WARRANTY & NO GUARANTY` | 10 | `1161- 12 SHOT JUNGLE BOOK`, `1162- F. POT COL KOTI` |
| **42** | `50` | `OFF SEASON LIST 2025-26` | 253 | `W 30 SHOTS M. COL. UV`, `W 60 SHOTS M. COL. UV` |

---

## 4. Recommended Tablet User Experience & Screen Layout

The tablet layout is optimized for an assisted-selling workflow where the salesman holds the tablet in landscape orientation:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🏷️ RAM FATAKA CENTER POS   Customer: 01149 - NEW SHIVA BALAJI  [🔍 Search item / code] │
├──────────────────────────┬──────────────────────────────────────────┬──────────────────┤
│ SHOWROOM SECTIONS (SR)   │ SECTION 16: FLOWER POTS (74 Items)       │ ACTIVE ORDER (3) │
│                          │                                          │                  │
│ [1] Caps & Matches       │ ┌──────────────────────────────────────┐ │ 443- F.P. Small  │
│ [4] Serpents & Naggoli   │ │ 443- FLOWER POTS SMALL (10 P)        │ │  Qty: 15  ₹750.00│
│ [5] 9 CM Sparklers       │ │ Code: 00427 | Unit: PKT | Stock: 450 │ │                  │
│ [7] Classic Sparklers    │ │ Rate: ₹50.00                         │ │ 588- G C Big     │
│ [11] Bijali & Bombs      │ │ [-] [  15  ] [+]  [ +5 ] [ +10 ]     │ │  Qty: 10 ₹1200.00│
│ [15] One Sound Dhamaka   │ └──────────────────────────────────────┘ │                  │
│ ▶[16] FLOWER POTS (74)◀  │ ┌──────────────────────────────────────┐ │ 840- 6 Shots     │
│ [17] Fancy Fountains     │ │ 444- FLOWER POTS RAJLAXMI (10 P)     │ │  Qty:  2  ₹460.00│
│ [23] Ground Chakkars     │ │ Code: 00428 | Unit: PKT | Stock: 120 │ ├──────────────────┤
│ [27] Rockets             │ │ Rate: ₹60.00                         │ │ Subtotal:₹2410.00│
│ [30] Atom Bombs          │ │ [-] [   0  ] [+]  [ +5 ] [ +10 ]     │ │ Roundoff:   ₹0.00│
│ [31] Garlands & Lar      │ └──────────────────────────────────────┘ │ Total:   ₹2410.00│
│ [32] Multishots (151)    │                                          │                  │
│                          │ ┌──────────────────────────────────────┐ │ [Clear] [Review] │
│ [ ⬇ Scroll Sections ]    │ │ ⏩ SKIP TO NEXT SECTION (Chakkars)   │ │                  │
│                          │ └──────────────────────────────────────┘ │ [SUBMIT ORDER]   │
└──────────────────────────┴──────────────────────────────────────────┴──────────────────┘
```

### Key UI Features for Speed:
1. **Left Section Sidebar:** Displays sections ordered by `COMPMST.SR`. Highlighting the active section allows 1-tap jumping across aisles.
2. **Numeric Catalog Order in Grid:** Items are sorted by their legacy catalog prefix (`443-`, `444-`, `445-`) so the screen directly matches physical shelf labels.
3. **One-Tap Quick Steppers:** Buttons for `+1`, `+5`, `+10` allow rapid order entry for wholesale buyers without opening a keyboard dialog.
4. **"Skip to Next Section" Button:** Located at the bottom of the product list, allowing the salesman to immediately proceed to the next aisle with a single thumb press.
5. **Persistent Order Drawer:** On the right third of the screen, running totals and items are always visible to the buyer.

---

## 5. End-to-End Customer Session Simulation

### Scenario:
- **Customer:** Subhash Patil (Retail Shopkeeper from Arni, Code `00276`).
- **Staff:** Salesman Ramesh with Android Tablet.
- **Budget / Goal:** Mix of sparklers, flower pots, chakkars, and multishot cakes.

---

### Step 1: Customer Selection & Order Start
1. Staff launches tablet app.
2. Taps "Select Customer" $\to$ Searches `"BUTLE"` or code `"00276"` (`BUTLE FATAKA CENTER (ARNI)`).
3. Tablet initializes new draft: `draft_id = "TAB01-1049"`.
4. App automatically defaults to Section 1 (`ROLL AND DOT CAPS`).

---

### Step 2: Skipping Unwanted Sections
1. Staff asks: *"Roll caps ya match box chahiye?"*
2. Customer: *"Nahi, direct Sparklers dikhao."*
3. Staff taps **Section 5: `9 CM SPARKLERS`** on the left sidebar.
4. Catalog instantly scrolls to Section 5.

---

### Step 3: Adding Sparklers
1. Screen shows 14 sparkler varieties sorted by number:
   - `178- 9 CM PLAIN INDRA` (₹38.00 | Stock: 420 PKT)
   - `179- 9 CM COL INDRA` (₹42.00 | Stock: 310 PKT)
2. Customer: *"10 packet plain aur 10 packet color daal do."*
3. Staff taps `+10` on `178-` and `+10` on `179-`.
4. Right drawer updates:
   - 2 items | Total: ₹800.00.

---

### Step 4: Flowing to Flower Pots (Anar)
1. Staff asks: *"Anar kounsa daalu?"*
2. Staff taps **Section 16: `FLOWER POTS COL KOTI`**.
3. Section opens with 74 flower pot items.
4. Customer: *"Small Flower Pots 15 packet, aur Tri-Colour Cock 5 packet."*
5. Staff locates `443- FLOWER POTS SMALL (10 P)` (₹50.00), taps `+10` then `+5` (Qty = 15).
6. Staff jumps to Section 17 (`FANCY FLOWER POTS`), locates `520- TRI COL FOUNTAIN COCK (5 P)` (₹297.00), taps `+5`.
7. Drawer updates: 4 items | Total: ₹3,035.00.

---

### Step 5: Skipping Sound Crackers to Ground Chakkars
1. Customer: *"Rockets aur bombs nahi chahiye, Chakkar dikhao."*
2. Staff skips Sections 21–22 and taps **Section 23: `GROUND CHAKKAR BIG`**.
3. Customer picks `588- G C BIG T/MEENA (10 P)` (₹120.00).
4. Staff taps `+10` (Qty = 10).
5. Drawer updates: 5 items | Total: ₹4,235.00.

---

### Step 6: Sky Shots Selection
1. Customer: *"Ek accha 30-shot cake daalo."*
2. Staff taps **Section 32: `SHOTS & MULTISHOTS`** (151 items).
3. Staff types `"30"` in the in-section search bar.
4. Filtered list displays `902- 30 SHOTS MULTI COLOUR AYYAN` (₹650.00 | Stock: 45).
5. Staff taps `+2` (Qty = 2).
6. Drawer updates: 6 items | Total: ₹5,535.00.

---

### Step 7: Order Review & Placement
1. Staff taps **"Review Order"**.
2. Full-screen modal displays the 6 items, quantities, rates, and grand total: **₹5,535.00**.
3. Customer confirms: *"Haan, barabar hai."*
4. Staff taps **"SUBMIT ORDER"**.
5. App saves draft to local SQLite, marks status as `QUEUED`, and uploads to Windows Sync Service via `POST /api/orders`.
6. Order appears on Sync Service dashboard ready for native FoxPro billing (`IMPORT.PRG`).
