# Alpha Pilot: Operator Usability & Feedback Form
**System:** RAM FATAKA CENTER Billing & POS Integration  
**Evaluation Scope:** Legacy-Only Showroom Tablet POS & FoxPro Sync  
**Instructions:** To be completed by Operator 1 (Salesman) and Operator 2 (Billing Clerk) at the end of Day 1 and Day 2 pilot sessions.

---

## 1. General Information

| Field | Operator Response |
|---|---|
| **Operator Name:** | _____________________________________________ |
| **Role:** | [ ] Showroom Floor Salesman &nbsp;&nbsp;&nbsp;&nbsp; [ ] Billing Counter Clerk |
| **Device Model / Tablet ID:** | [ ] Tablet 1 (TAB-01) &nbsp;&nbsp; [ ] Tablet 2 (TAB-02) &nbsp;&nbsp; [ ] Billing PC |
| **Date & Shift:** | Date: _____ / _____ / 2026 &nbsp;&nbsp;&nbsp;&nbsp; Shift: [ ] Morning &nbsp; [ ] Evening |
| **Approx. Orders Handled:** | [ ] 1 – 5 &nbsp;&nbsp;&nbsp;&nbsp; [ ] 6 – 15 &nbsp;&nbsp;&nbsp;&nbsp; [ ] 16 – 30 &nbsp;&nbsp;&nbsp;&nbsp; [ ] 30+ |

---

## 2. Quantitative Evaluation (Scale 1 to 5)

*Rating Scale: **1 = Very Poor / Frustrating** &nbsp;|&nbsp; **2 = Below Average** &nbsp;|&nbsp; **3 = Acceptable** &nbsp;|&nbsp; **4 = Good / Fast** &nbsp;|&nbsp; **5 = Excellent / Seamless***

### A. Tablet Usability & Physical Handling (Showroom Salesman)
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **A1** | **Screen Readability:** Product names, prices, and stock numbers are easy to read while standing in showroom lighting. | `[   ]` | |
| **A2** | **Touch Target Size:** Buttons (`+1`, `+5`, `+10`, sections) are large enough to tap accurately without mis-clicks. | `[   ]` | |
| **A3** | **One-Hand / Standing Use:** The tablet interface is comfortable to operate while walking with a customer. | `[   ]` | |
| **A4** | **Battery Endurance:** Tablet battery lasted through the session without emergency recharging. | `[   ]` | |

---

### B. Showroom Section Navigation (`COMPMST.SR` 1 to 43)
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **B1** | **Section Order:** Showroom section sequence (`Caps -> Sparklers -> Pots -> Chakkars -> Bombs -> Multishots`) matches physical showroom aisles. | `[   ]` | |
| **B2** | **Section Switching Speed:** Tapping a section on the left sidebar opens products immediately with zero lag. | `[   ]` | |
| **B3** | **"Skip Section" Efficiency:** Skipping unwanted categories (e.g. customer doesn't want Rockets) is fast and intuitive. | `[   ]` | |
| **B4** | **Shelf Item Alignment:** Items appear in the expected catalog number sequence (`111-`, `178-`, `443-`, `588-`). | `[   ]` | |

---

### C. Item Selection, Steppers & Pack Quantity
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **C1** | **Quick Steppers:** The `+1`, `+5`, `+10` quick buttons make adding wholesale quantities faster than typing on a keypad. | `[   ]` | |
| **C2** | **Direct Quantity Keypad:** Entering large specific quantities (e.g. `120` or `250`) is quick and simple. | `[   ]` | |
| **C3** | **Pack Size Clarity:** Pack size descriptions inside item names (e.g. `(10 P)`, `(100X1)`) are clear enough to prevent selling loose pieces. | `[   ]` | |
| **C4** | **Out-of-Stock Visibility:** Amber/Red badges on zero-stock items (`CQTY <= 0`) clearly prevented committing unavailable items. | `[   ]` | |

---

### D. Search & Item Discovery
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **D1** | **Item Number Search:** Typing item number prefix (e.g. `"443"` or `"735"`) instantly brings up the exact cracker. | `[   ]` | |
| **D2** | **Brand Search:** Typing brand name (e.g. `"COCK"`, `"STD"`, `"AYYAN"`) successfully filters brand items. | `[   ]` | |
| **D3** | **Vernacular Search:** Typing colloquial terms (e.g. `"anar"`, `"chakri"`, `"ladi"`) displays relevant items correctly. | `[   ]` | |

---

### E. Order Review, Totals & Sync (Salesman)
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **E1** | **Cart Drawer Visibility:** Running items count and subtotal on the right side kept customer informed of their budget. | `[   ]` | |
| **E2** | **Discount Entry:** Entering negotiated bill discount (`less_amount`) was straightforward. | `[   ]` | |
| **E3** | **Order Submission Speed:** Tapping "Submit Order" uploaded the draft instantly without hanging. | `[   ]` | |
| **E4** | **Offline Resilience:** If WiFi disconnected in back storage, orders saved to outbox without crashing or losing items. | `[   ]` | |

---

### F. Counter Review & FoxPro Ingestion (Billing Clerk / Operator 2)
| # | Evaluation Statement | Rating (1 - 5) | Specific Remarks |
|:---:|---|:---:|---|
| **F1** | **Queue Visibility:** New tablet drafts appeared on the Sync Service screen immediately upon submission. | `[   ]` | |
| **F2** | **Draft Accuracy:** Draft customer name, items, rates, and totals matched customer intent 100%. | `[   ]` | |
| **F3** | **Import Execution:** Running the import script into FoxPro (`IMPORT.PRG`) was smooth and completed in under 1 second. | `[   ]` | |
| **F4** | **Ledger & Stock Accuracy:** Verified that `SALEMST`, `SALETRN`, `LEDGER`, and `ITEMMST` updated accurately without manual corrections. | `[   ]` | |
| **F5** | **Traceability:** Found `"DRAFT:TAB01-XXXX"` in `SALEMST.NOTE` matching the tablet draft ID. | `[   ]` | |

---

## 3. Qualitative Feedback & Open Observations

### 3.1 What was the BEST feature of the tablet POS during selling?
> *Example: "Not having to write items on carbon paper; jumping straight to flower pots."*
>  
> _________________________________________________________________________________________
> _________________________________________________________________________________________

### 3.2 What was the BIGGEST bottleneck or slowest action?
> *Example: "Searching for items with weird spelling; accidental double-tapping on +10."*
>  
> _________________________________________________________________________________________
> _________________________________________________________________________________________

### 3.3 How did customers react when ordering on the tablet?
> *Example: "Impressed by live bill total; asked if prices had GST included; preferred seeing screen."*
>  
> _________________________________________________________________________________________
> _________________________________________________________________________________________

### 3.4 Were any products difficult to find using only FoxPro categories (`COMPMST`)?
> *List specific item names or numbers that felt in the wrong section:*
>  
> 1. Item: ___________________________________ Felt it belonged in: _______________________
> 2. Item: ___________________________________ Felt it belonged in: _______________________

### 3.5 Any accidental errors or missing features?
> _________________________________________________________________________________________
> _________________________________________________________________________________________

---

## 4. Operator Recommendation & Sign-Off

*Would you prefer using this tablet system over paper order pads for the upcoming Diwali rush?*
- [ ] **YES, Definitely** — Much faster and avoids manual re-billing.
- [ ] **YES, with minor fixes** — Need small tweaks listed above before full rollout.
- [ ] **NO, Prefer Paper** — Explanatory reason: _________________________________________

**Operator Signature:** ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp; **Date:** _____ / _____ / 2026
