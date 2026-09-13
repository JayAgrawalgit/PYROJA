# Changelog: Product Display Purity & Cache Invalidation

All notable changes to the PYROJA application stack are documented herein.

---

## [0.1.1-alpha] - 2026-09-13

### 1. What Was Investigated
- Persistent display of secondary metadata (`Pack`, `Inner units`, `GST`) inside product description areas.
- Discrepancy between APK rebuilds and runtime behavior on Android devices.
- Inactive placeholder records ("ghost products") causing blank catalog entries and skewed category counts.

### 2. Root Cause
- **Secondary Display Injection:** Catalog table renderer and modal headers contained string interpolation logic appending metadata attributes directly underneath product titles.
- **Chromium Disk Cache Retention:** Android WebView maintained cached copies of `index.html` in `/data/data/com.pyrowholesale.pos/app_webview/Default/Cache`, ignoring newly packaged assets.
- **Unfiltered FoxPro Ingestion:** Inactive DBF records lacking names, stock, and rates were imported as active catalog items.

### 3. What Was Changed

#### Sync Service (`sync-service/`)
- **`app/services/master_service.py`**:
  - Implemented ghost-product filter in `get_products_sync()`: Omits records where trimmed name is empty, stock is `<= 0`, and selling rate is `<= 0`.
  - Implemented matching filter in `get_categories_sync()` to guarantee category counter accuracy.
- **`tests/test_api.py` & `tests/test_tablet_integration.py`**:
  - Updated mock product sets and count assertions to validate ghost product exclusion.

#### Tablet POS Application (`tablet-app/`)
- **`index.html`**:
  - Simplified product description cell in `renderCatalog()` to render strictly `${p.name}`.
  - Removed `#modal-product-code`, `#modal-product-rate`, and `#modal-product-stock` subtitle elements from `#qty-modal`.
  - Removed obsolete variable references from `openQuantityDialog()`.
  - Added HTTP `<meta>` headers for cache suppression (`no-cache, no-store, must-revalidate`).
- **`app.js`**:
  - Implemented client-side defensive filter against ghost items during IndexedDB hydration.
- **`tests/beta_blockers_test.js`**:
  - Added Test 6 verifying ghost-product filtering behavior.
- **`package.json`**:
  - Updated `build:apk` script to invoke `./gradlew assembleRelease`.
- **Repository Cleanup**:
  - Deleted redundant legacy file `tablet-app/code.html`.
  - Removed duplicate debug APK binaries `tablet-app/dist/pyroja-pos-debug.apk` and `tablet-app/dist/pyrowholesale-pos-debug.apk`.

#### Android Native Wrapper (`tablet-app/android/`)
- **`app/src/main/java/com/pyrowholesale/pos/MainActivity.java`**:
  - Added `bridge.getWebView().clearCache(true)`.
  - Configured `WebSettings.LOAD_NO_CACHE` to prevent disk caching of local web assets.
- **`app/build.gradle`**:
  - Added `signingConfigs.getByName("debug")` to release build configuration for automated testing.

### 4. Files Modified
- `sync-service/app/services/master_service.py`
- `sync-service/tests/test_api.py`
- `sync-service/tests/test_tablet_integration.py`
- `tablet-app/index.html`
- `tablet-app/app.js`
- `tablet-app/package.json`
- `tablet-app/package-lock.json`
- `tablet-app/tests/beta_blockers_test.js`
- `tablet-app/android/app/build.gradle`
- `tablet-app/android/app/src/main/java/com/pyrowholesale/pos/MainActivity.java`
- `DEPLOYMENT_AUDIT.md` (Created)
- `tablet-app/code.html` (Deleted)
- `tablet-app/dist/pyroja-pos-debug.apk` (Deleted)
- `tablet-app/dist/pyrowholesale-pos-debug.apk` (Deleted)

### 5. Risks
- Newly added FoxPro items missing names will not appear until a name, stock, or rate is entered.
- Legacy installations require either APK upgrade or app data purge to reset cached WebView assets.

### 6. Validation Performed
- Backend unit and integration tests: 28/28 passed (`pytest`).
- Frontend automated tests: 6/6 passed (`node tests/beta_blockers_test.js`).
- DevTools DOM audit: 100 rows examined; 0 non-name elements found in description cells.
- Device testing: Verified order dispatch `ORD-20260913-9E6226` and visual rendering across 5 core views on Android emulator.

### 7. Failed Verifications
- None.

### 8. Final Outcome
- Pure product name presentation achieved across all UI views.
- WebView disk cache invalidation verified.
- Ghost items eliminated from product and category counts.
- Single clean release APK produced.
