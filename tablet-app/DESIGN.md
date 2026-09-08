---
name: Industrial Pyrotechnic Wholesale POS
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#e2bfb2'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#a98a7e'
  outline-variant: '#5a4138'
  surface-tint: '#ffb599'
  primary: '#ffb599'
  on-primary: '#5a1c00'
  primary-container: '#f66018'
  on-primary-container: '#4f1700'
  inverse-primary: '#a73a00'
  secondary: '#ffb77d'
  on-secondary: '#4d2600'
  secondary-container: '#d97707'
  on-secondary-container: '#432100'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbce'
  primary-fixed-dim: '#ffb599'
  on-primary-fixed: '#370e00'
  on-primary-fixed-variant: '#7f2b00'
  secondary-fixed: '#ffdcc3'
  secondary-fixed-dim: '#ffb77d'
  on-secondary-fixed: '#2f1500'
  on-secondary-fixed-variant: '#6e3900'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  headline-lg:
    fontFamily: Chivo
    fontSize: 28px
    fontWeight: '800'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Chivo
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 26px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Chivo
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 22px
  body-lg:
    fontFamily: Chivo
    fontSize: 15px
    fontWeight: '500'
    lineHeight: 20px
  body-md:
    fontFamily: Chivo
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Chivo
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  label-numeric-lg:
    fontFamily: JetBrains Mono
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 26px
    letterSpacing: -0.02em
  label-numeric-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
  label-numeric-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.08em
spacing:
  touch-min: 48px
  touch-compact: 40px
  pad-xs: 4px
  pad-sm: 8px
  pad-md: 12px
  pad-lg: 16px
  pad-xl: 24px
  col-gap: 8px
  row-gap: 4px
---

## Brand & Style

This design system serves high-velocity B2B wholesale order capture in rugged commercial fireworks showrooms, trade-show floors, and dimly lit warehouse staging hubs. The aesthetic is purely utilitarian, uncompromising, and industrial—combining high-density tabular precision with immediate physical clarity. 

Key pillars:
- **Zero Fluff & High Density:** Prioritizes tabular data throughput, minimizing decorative chrome and whitespace to maximize visible lines per screen without sacrificing touch precision.
- **Harsh Environment Legibility:** Optimized for Android tablets (10–11" landscape) under varied lighting—from harsh halogen fixtures to dark shipping containers—using crisp contrasting borders, deep slate surfaces, and safety-grade visual signals.
- **Tactile Touch Performance:** Immediate feedback loops, rapid mechanical-feel tap targets, and visible validation states designed for glove-friendly or rapid thumb-and-stylus interactions.

## Colors

The palette is engineered around high functional contrast and strict semantic meaning:

- **Surface & Backgrounds:**
  - Base canvas: `#0F172A` (Slate 900)
  - Surface elevations / cards / panels: `#1E293B` (Slate 800)
  - Cell hover & pressed highlights: `#334155` (Slate 700)
  - Dividers & structural grids: `#475569` (Slate 600)
- **Primary Safety Accents:**
  - Primary Action / Stepper Active: `#EA580C` (Safety Orange)
  - Focus Ring / Warning / Secondary Accent: `#D97706` (Hazard Amber)
- **Financial & Sync Signals:**
  - Positive Live Totals / In-Stock / Cloud Synced: `#10B981` (Emerald Green)
  - Offline Alert / Backorder / Error: `#EF4444` (Crimson Red)
- **Text & Numeric Hierarchy:**
  - High-emphasis values and metrics: `#F8FAFC` (Slate 50)
  - Medium-emphasis labels & metadata: `#94A3B8` (Slate 400)
  - Disabled states: `#64748B` (Slate 500)

## Typography

Typography balances rapid scanning with exact numeric precision:
- **Headings & Product Nomenclature:** Set in `Chivo` for bold, legible letterforms with industrial authority.
- **Data Tables & Monetary Calculations:** Set in `JetBrains Mono` with tabular lining numbers (`font-variant-numeric: tabular-nums`) to ensure zero horizontal shift when quantities, case counts, or line totals increment dynamically.
- **Case Sensitivity:** Structural table headers, packing unit tiers (e.g., `CS`, `PK`, `UN`), and hazard classes (e.g., `1.4G`, `1.3G`) enforce uppercase formatting via `label-caps` for instant identification.

## Layout & Spacing

Designed specifically for 10–11" tablets (typically 1920×1200 or 2560×1600 landscape at 1.5x–2.0x DPI scaling, yielding 1280×800 to 1366×768 effective viewport):

- **Two-Pane Structural Split:**
  - **Left / Center Catalog & Order Grid:** 65% width fixed split. Accommodates search filters, product barcode scanner inputs, and the dense order lines grid.
  - **Right Execution Drawer & Keypad:** 35% fixed width (minimum 360px). Houses live running totals, tier volume discounts, batch notes, and an integrated rapid numeric keypad for direct active-row entry.
- **Density Principles:**
  - Vertical data row height is standardized to 48px to satisfy tablet accessibility touch criteria while packing 10–12 visible order lines above the fold.
  - Cell padding is locked to `pad-sm` (8px) horizontally and `pad-xs` (4px) vertically.

## Elevation & Depth

No soft ambient blurs or skeuomorphic drops. Elevation is communicated through **structural high-contrast borders and solid tonal layer stepping**:

- **Layer 0 (Canvas):** Solid `#0F172A`.
- **Layer 1 (Panels & Grids):** `#1E293B` bounded by a 1px solid border of `#334155`.
- **Layer 2 (Active/Selected Row or Card):** `#334155` background with an inset 2px border in `#EA580C` (Safety Orange).
- **Layer 3 (Modals & Numeric Keypad Overlays):** `#1E293B` framed by 2px solid `#64748B`, using a sharp 4px hard shadow (`4px 4px 0px #000000`) for unambiguous tactical separation.

## Shapes

A strict `0` (Sharp) corner profile is applied across all components. 

Buttons, table rows, badges, tabs, and keypad elements employ 0px border-radii. This maximizes functional pixel space, reinforces the physical industrial instrumentation vibe, and eliminates visual anti-aliasing fuzziness along table borders.

## Components

### 1. Stepper Controls ([+] / [-])
- **Dimensions:** Square 44×44px hit-box.
- **Styling:** Inset `#0F172A` background, 1px `#475569` border. Large, centered monospace symbol (`+` or `−`) in `#F8FAFC`.
- **States:** Active/Pressed shifts instantly to `#EA580C` background with `#0F172A` icon. No animations or transitions to avoid lag during fast double-tapping.

### 2. Tabular Data Grid
- **Header:** Sticky, `#0F172A` background, 32px height, 1px bottom border `#475569`, text styled with `label-caps` in `#94A3B8`.
- **Columns:** Code (80px), Description (Flex), Hazard (60px), Pack/Case (80px), Price/Unit (90px), Qty Stepper (140px), Ext Total (110px).
- **Numbers:** All monetary and count columns right-aligned with `JetBrains Mono`.
- **Status Indicators:** 6px left border accent indicating line status (Emerald = in-stock confirmed, Amber = partial stock / allocation required, Red = line error).

### 3. Integrated Numeric Keypad
- **Layout:** 4×3 keypad grid with dedicated `CLEAR`, `ENTER`, and common fireworks bulk case increments (`+5`, `+10`, `+25`).
- **Keys:** Minimum 64px height, high-contrast `#1E293B` face, 1px `#475569` outline, 22px bold monospace text.

### 4. Live Order Summary Banner
- **Location:** Anchored bottom-right.
- **Styling:** Highlighted container in `#0F172A` with a 2px `#10B981` border.
- **Data:** Displays Gross Weight, Total Cube (cu ft), Explosive Content (NEC/NEW), and Final Payable Total rendered in `label-numeric-lg` (`#10B981`).

### 5. Input Fields & Barcode Handlers
- **Height:** 44px consistent height.
- **Styling:** `#0F172A` background, 1px `#64748B` border, `#F8FAFC` font.
- **Focus State:** 2px high-intensity `#D97706` outline for scanner confirmation.