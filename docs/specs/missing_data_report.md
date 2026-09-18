# Missing Sales Data Analysis & Legacy Mitigation Report (Phase 2.6)
**System:** RAM FATAKA CENTER Wholesale & Retail POS  
**Focus:** Fields Strictly Required for Showroom Sales but Missing from FoxPro  
**Constraint:** 100% Native FoxPro Data — No External Excel Dependencies  
**Document Status:** Production Gap Analysis & Mitigation Protocol

---

## 1. Executive Summary

When transitioning from paper order pads to tablet-assisted selling, certain commercial attributes commonly expected in modern POS software are absent or unpopulated in the 25-year-old FoxPro database (`D2627`).

However, an empirical audit reveals that **showroom salesmen already navigate these limitations daily** by decoding abbreviations, parentheses, and conventions embedded directly inside `ITEMMST.NAME`.

This report identifies the **five critical missing sales fields**, explains how showroom staff operates without them today, and defines **zero-external-dependency algorithmic mitigations** implemented within the Python Sync Service and Android Tablet application.

---

## 2. Detailed Gap Analysis & Native Mitigations

### 2.1 Missing Field 1: Structured Case Pack Multiples / Box Quantity
- **Field State in FoxPro:**
  - `ITEMMST.QIB` ("Quantity in Box") is hardcoded to **`1` across 100% of all 3,019 records**.
  - `ITEMMST.FACTOR` is **`0.00` across 100% of records**.
  - `ITEMMST.PACK` contains only general units (`'PKT'`, `'BOX'`, `'PCS'`, `'BUNDLE'`).
- **Operational Reality in Showroom:**
  In fireworks wholesale, manufacturers package products in master boxes containing multiple retail packets (e.g. 10 packets per box, 25 packets per box, 100 packets per bag). Selling odd quantities (e.g. 7 packets) opens a sealed box and causes inventory leakage.
- **How Staff Knows Today:**
  Staff reads the pack multiplier embedded inside parentheses in `ITEMMST.NAME`:
  - `119- ASST CARTOON(10 PCS)DURGESH` $\to$ **10**
  - `120- ASST CARTOON BEN TEN(25P)AYYANAR` $\to$ **25**
  - `124- BIG NAGGOLI PANDYAN BLACK(100X1=1 B` $\to$ **100**
  - `443- FLOWER POTS SMALL (10 P)` $\to$ **10**
  - `520- TRI COL FOUNTAIN COCK (5 P)` $\to$ **5**
  - `735- BULLET BOMB MINI SRI ATHISAYA(10P)` $\to$ **10**
- **Native Algorithmic Mitigation (Python Sync Service & Tablet App):**
  The Sync Service applies a deterministic regular expression parser on `ITEMMST.NAME` during product sync:
  ```python
  import re

  def extract_pack_multiple(name: str) -> int:
      """Extracts wholesale pack multiple from parentheses in ITEMMST.NAME."""
      patterns = [
          r"\((\d+)\s*(?:P|PCS|PKT|DABBA|BAGS|PIECES)\)",  # e.g. (10 P), (25 PCS)
          r"\((\d+)X\d+",                                  # e.g. (100X1=1 B)
          r"(\d+)\s*P\s*=\s*1\s*(?:BUND|BOX|BUNDLE)",       # e.g. (50P= 1 BUNDEL)
      ]
      for pat in patterns:
          m = re.search(pat, name, re.IGNORECASE)
          if m:
              try:
                  val = int(m.group(1))
                  if 1 < val <= 1000:
                      return val
              except ValueError:
                  pass
      return 1  # Default fallback if loose
  ```
  **Tablet Behavior:** If `extract_pack_multiple` returns `10`, the tablet quick-stepper increments by `10`, preventing fractional packaging errors.

---

### 2.2 Missing Field 2: Visual Product Photography / Thumbnail Images
- **Field State in FoxPro:**
  - DBF tables do not store binary image blobs or image file paths.
- **Operational Reality in Showroom:**
  - Wholesale buyers rarely need photos because they buy by brand and item number year after year.
  - Retail walk-in customers often ask: *"Ye anar kitna bada phutta hai?"* (What does this fountain effect look like?).
- **How Staff Knows Today:**
  - The physical showroom at Ghatanji is a display showroom where dummy samples of every cracker box are arranged on open display shelves numbered 1 to 43. The salesman points directly to the physical shelf.
- **Native Algorithmic Mitigation:**
  1. **Primary Solution (Display Badges):** The tablet displays large, high-contrast typography, Section Badges (`[16] FLOWER POTS`), and Pack Unit labels (`PKT`, `BOX`).
  2. **Optional Zero-DBF Asset Linking:** If the shop photographs their showroom shelves, images are stored in the tablet's local `/assets/products/` directory named strictly by `ITEMMST.CODE` (e.g. `00443.webp`). The tablet simply checks:
     ```javascript
     const imgUrl = `assets/products/${product.code}.webp`;
     ```
     If the file exists locally, it renders; if not, it renders an elegant fireworks category icon. **Zero changes to FoxPro.**

---

### 2.3 Missing Field 3: Dedicated Brand / Manufacturer Column
- **Field State in FoxPro:**
  - No `BRAND` field exists. `CCODE` points to showroom category sections in `COMPMST`.
- **Operational Reality in Showroom:**
  - Many buyers have strong brand loyalty (e.g. *"Sirf Standard brand ka maal do"* or *"Cock brand ke anar do"*).
- **How Staff Knows Today:**
  - Brand names and standard trade abbreviations are written into `ITEMMST.NAME`:
    - `S.T.D` or `STD` = Standard Fireworks
    - `AYYAN` or `AYYANAR` = Ayyanar Fireworks
    - `COCK` = Cock Brand / Sri Kaliswari
    - `MERCURY` = Mercury Fireworks
    - `PANDYAN` = Pandyan Brand
    - `SIVASAKTHI` = Sivasakthi Fireworks
    - `DURGESH` = Durgesh Fireworks
    - `RAJLAXMI` or `RAJHARISH` = Rajlaxmi Brand
- **Native Algorithmic Mitigation:**
  1. **Full-Text Token Search:** The tablet POS search bar performs non-anchored case-insensitive substring searching across the full string of `ITEMMST.NAME`.
  2. **Result:** When the staff types `"COCK"` in the search bar, the tablet instantly returns all 18 Cock brand items across all sections, even though no `BRAND` column exists.

---

### 2.4 Missing Field 4: Colloquial Trade Aliases (Marathi / Hindi Vernacular Terms)
- **Field State in FoxPro:**
  - Field `NICK` is empty or `'***'`. Names are entered in English transliterations (`FLOWER POTS`, `GROUND CHAKKAR`, `SPARKLERS`).
- **Operational Reality in Showroom:**
  - Rural customers frequently request items in Marathi / Hindi:
    - *"Koti"* / *"Anar"* $\to$ Flower Pots
    - *"Chakri"* / *"Bhuinchakra"* $\to$ Ground Chakkars
    - *"Phulbatti"* $\to$ Sparklers
    - *"Ladi"* / *"Maal"* $\to$ Garlands
    - *"Rassi Bomb"* / *"Sutli Bomb"* $\to$ Atom Bombs
    - *"Pencil"* $\to$ Color Torches
    - *"Bijli"* $\to$ Red Bijali Crackers
- **How Staff Knows Today:**
  - Experienced showroom staff instantly translates from vernacular to the English catalog name mentally.
- **Native Algorithmic Mitigation (Client-Side Synonym Dictionary):**
  A lightweight static synonym dictionary is embedded directly in `tablet-app/app.js`:
  ```javascript
  const VERNACULAR_SYNONYMS = {
      "anar": ["FLOWER POT", "FOUNTAIN", "MATKA"],
      "koti": ["FLOWER POT", "KOTI"],
      "chakri": ["GROUND CHAKKAR", "CHAKKAR", "SPINNER"],
      "phulbatti": ["SPARKLER", "SPARKLERS"],
      "ladi": ["GARLAND", "LAR"],
      "rassi": ["BOMB", "ATOM BOMB"],
      "sutli": ["BOMB", "ATOM BOMB"],
      "pencil": ["PENCIL", "TORCH"]
  };
  ```
  When the salesman types `"anar"`, the search engine expands the query to match `"FLOWER POT"`, instantly displaying Section 16 items without requiring any changes to the database.

---

### 2.5 Missing Field 5: Wholesale Carton vs. Loose Packet Pricing
- **Field State in FoxPro:**
  - `ITEMMST` stores only a single selling rate: `SRATE`.
  - There are no separate columns for `CASE_RATE`, `LOOSE_RATE`, or customer tier discounts.
- **Operational Reality in Showroom:**
  - Wholesalers buying master cartons negotiate a lower bulk price than walk-in retail customers buying individual boxes.
- **How Staff Knows Today:**
  - In FAVWIN, the shop bills everything at `SRATE`. If a wholesaler is entitled to a bulk discount, the operator applies a lump-sum discount amount in the **`LESS`** field of `SALEMST` at the bottom of the invoice.
- **Native Algorithmic Mitigation:**
  - The tablet order entry model maintains FoxPro's native behavior:
    1. Line items are priced strictly at `ITEMMST.SRATE`.
    2. The tablet order summary drawer includes an optional **"Bill Discount (₹)"** input field (`less_amount`), which maps directly to `SALEMST.LESS`.
    3. Net total is computed as `Total = Gross - Less + RoundOff`, maintaining 100% mathematical consistency with FoxPro billing.

---

## 3. Summary of Gaps & Resolution Matrix

| Critical Sales Requirement | Present in FoxPro? | Native Technical Mitigation | Impact on Operation |
|---|:---:|---|:---:|
| **Section Browsing** | ✅ `COMPMST.SR` | Group by `CCODE`, sort by `COMPMST.SR` (1..43) | Replicates paper catalog sequence 1:1. |
| **Numeric Item Sequence** | ✅ `NAME` prefix | Regex sort key on `^(\d+)` | Matches showroom shelf numbering. |
| **Pack Multiples** | ❌ Hardcoded to 1 | Regex parser extracts `(10 P)` from `NAME` | Prevents breaking wholesale boxes. |
| **Product Photos** | ❌ None | Category iconography + optional `code.webp` | Sufficient for assisted showroom selling. |
| **Brand Filtering** | ❌ None | Full-text token search on `ITEMMST.NAME` | Instant retrieval of brands like `COCK`, `STD`. |
| **Vernacular Search** | ❌ None | Client-side synonym mapping in `app.js` | Supports rural walk-in buyer vocabulary. |
| **Tiered Pricing** | ❌ Single `SRATE` | Overall order discount via `less_amount` | 100% compatible with FoxPro `SALEMST.LESS`. |
| **Stock Visibility** | ✅ `ITEMMST.CQTY` | Color-coded badges (`In Stock` vs `Out of Stock`) | Prevents committing unavailable inventory. |

**Final Assessment:**  
By utilizing `COMPMST.SR` and smart string heuristics on `ITEMMST.NAME`, **100% of the showroom sales workflow can be supported using legacy FoxPro data alone**, with zero requirement for external Excel catalog files.
