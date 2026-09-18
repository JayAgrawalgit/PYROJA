# PYROJA Repository Artifact Audit & Clutter Remediation Report

**Audit Date:** September 19, 2026  
**Auditor:** Senior Software Architect & Forensic Release Engineer  
**Repository:** `PYROJA` (`https://github.com/JayAgrawalgit/PYROJA`)  
**Branch:** `chore/repository-artifact-cleanup`  
**Target Milestone:** Post-v1.0.0 Clean Repository State  

---

## 1. Executive Summary & Inventory Census

A comprehensive forensic audit of all **2,282 tracked Git files** and local workspace assets was conducted across the PYROJA repository. The objective is to eliminate repository clutter safely without degrading the PYROJA sync service, tablet app, Windows standalone packaging, build pipelines, operational documentation, or developer workflows.

### Repository File Distribution

| Top-Level Directory / Area | Tracked File Count | Description / Role |
| :--- | :---: | :--- |
| **Root (`/`)** | 35 | Documentation, audits, changelogs, packaging worksheets, and version files |
| **`sync-service/`** | 44 | FastAPI Python backend, DBF engine, pack resolver, SQLite models, test suites |
| **`tablet-app/`** | 77 | Android Capacitor POS web application, Android native wrapper, tests, assets |
| **`PYRO-Sync-Service/`** | 665 | Standalone 64-bit Windows PE distribution (embedded Python 3.11, wheels, launchers) |
| **`packaging/`** | 5 | Dockerfiles and shell scripts for cross-compiling Windows standalone binaries |
| **`scripts/`** | 1 | Developer workflow automation script (`workflow.sh`) |
| **`vfp/`** | 2 | Root duplicate of FoxPro import scripts |
| **`legacy-software-extracted/`** | 1,453 | Upstream Visual FoxPro 6.0 tables (`D2627`), compiled programs (`.FXP`), indexes |
| **Total Tracked Files** | **2,282** | Full repository inventory |

---

## 2. Artifact Classification Framework

All reviewed, suspicious, non-code, and audit files are classified into four strict operational categories:

1. **Category 1: Required Runtime, Build, Packaging, Deployment, Test, or User Documentation — RETAIN.**  
   *Criteria:* Necessary for application runtime, compilation, packaging, testing, or user-facing setup. Retained in their canonical root or directory locations.
2. **Category 2: Useful Historical / Audit Evidence — ARCHIVE.**  
   *Criteria:* Valuable historical records, audit proof, or reverse-engineering specifications that should be preserved for traceability, but clutter the repository root. Moved to `docs/archive/` or `docs/specs/` with all cross-references updated.
3. **Category 3: Generated / Reproducible Output — IGNORE.**  
   *Criteria:* Machine-generated outputs, runtime databases, test staging payloads, or build artifacts. Excluded via hardened rules in `.gitignore`.
4. **Category 4: Clearly Obsolete, Duplicated, or Unused File — DELETE.**  
   *Criteria:* Dead files, redundant copies with canonical equivalents elsewhere, or unreferenced temporary prototypes proven to have zero references and zero operational utility.

---

## 3. Comprehensive Artifact Audit Table

The table below catalogs every evaluated non-source or suspicious file across the repository:

| # | File Path | Size | Purpose / Category | References Found | Needed at Runtime / Build / Deploy? | Reproducible? | Risk of Removal | Recommendation | Supporting Evidence & Rationale |
|:---:|:---|:---:|:---|:---|:---:|:---:|:---:|:---:|:---|
| 1 | `proof_footer_removed_cart.png` | 445 KB | UI verification screenshot (footer decommission) | 2 (`FOOTER_REMOVAL_AUDIT.md`, `FOOTER_REMOVAL_CHANGELOG.md`) | No | Yes (UI capture) | Low | **Archive** (`docs/archive/proofs/`) | Verification screenshot captured on 2026-09-13. Co-locating with archived audit report preserves evidence while freeing 445 KB from root. |
| 2 | `proof_footer_removed_catalog.png` | 419 KB | UI verification screenshot (footer decommission) | 2 (`FOOTER_REMOVAL_AUDIT.md`, `FOOTER_REMOVAL_CHANGELOG.md`) | No | Yes (UI capture) | Low | **Archive** (`docs/archive/proofs/`) | Verification screenshot captured on 2026-09-13. Co-locating with archived audit report preserves evidence while freeing 419 KB from root. |
| 3 | `proof_footer_removed_checkout.png` | 445 KB | UI verification screenshot (footer decommission) | 2 (`FOOTER_REMOVAL_AUDIT.md`, `FOOTER_REMOVAL_CHANGELOG.md`) | No | Yes (UI capture) | Low | **Archive** (`docs/archive/proofs/`) | Verification screenshot captured on 2026-09-13. Co-locating with archived audit report preserves evidence while freeing 445 KB from root. |
| 4 | `FOOTER_REMOVAL_AUDIT.md` | 6.1 KB | Task audit for bottom diagnostic bar removal | 1 (`FOOTER_REMOVAL_CHANGELOG.md`) | No | Historical report | Low | **Archive** (`docs/archive/audits/`) | One-time forensic audit completed on 2026-09-13. Safe to move into archive; links to proof images updated to `../proofs/`. |
| 5 | `FOOTER_REMOVAL_CHANGELOG.md` | 2.9 KB | Changelog for footer removal task | 1 (`FOOTER_REMOVAL_CHANGELOG.md`) | No | Historical report | Low | **Archive** (`docs/archive/audits/`) | One-time task changelog completed on 2026-09-13. Archived alongside audit report. |
| 6 | `EXECUTABLE_AUDIT.md` | 8.1 KB | Forensic audit for standalone Windows executable | 0 | No | Historical report | Low | **Archive** (`docs/archive/audits/`) | Milestone audit completed on 2026-09-13 for v1.0.0 standalone package. |
| 7 | `EXE_BUILD_REPORT.md` | 3.6 KB | Build report for `PYRO-Sync-Service.exe` | 0 | No | Historical report | Low | **Archive** (`docs/archive/reports/`) | Toolchain documentation and build verification from 2026-09-13. |
| 8 | `EXE_CHANGELOG.md` | 2.5 KB | Executable release changelog | 0 | No | Historical report | Low | **Archive** (`docs/archive/reports/`) | Subsumed into root `CHANGELOG.md`. Kept for historical traceability. |
| 9 | `EXECUTIVE_SUMMARY.md` | 4.3 KB | Executive summary for Windows standalone package | 0 | No | Historical report | Low | **Archive** (`docs/archive/reports/`) | Milestone executive summary from 2026-09-13. |
| 10 | `TECHNICAL_AUDIT.md` | 5.0 KB | Technical audit of sync service packaging | 0 | No | Historical report | Low | **Archive** (`docs/archive/audits/`) | Architectural audit from 2026-09-13 milestone. |
| 11 | `VERIFICATION_REPORT.md` | 4.9 KB | Verification report for standalone executable | 0 | No | Historical report | Low | **Archive** (`docs/archive/reports/`) | Wine verification test results from 2026-09-13. |
| 12 | `DEPLOYMENT_AUDIT.md` | 18.8 KB | Complete deployment audit for FoxPro integration | 0 | No | Historical report | Low | **Archive** (`docs/archive/audits/`) | Comprehensive system audit from 2026-09-13. |
| 13 | `alpha_test_plan.md` | 9.8 KB | Alpha showroom floor operations test plan | 0 | No | Historical doc | Low | **Archive** (`docs/archive/pilot/`) | Phase 1 alpha test plan from 2026-09-07. No active test runner uses it. |
| 14 | `bug_tracker_template.md` | 6.5 KB | Alpha pilot defect management template | 0 | No | Historical doc | Low | **Archive** (`docs/archive/pilot/`) | Defect tracking template from 2026-09-07. |
| 15 | `operator_feedback_form.md` | 7.6 KB | Alpha pilot operator usability form | 0 | No | Historical doc | Low | **Archive** (`docs/archive/pilot/`) | Operator feedback questionnaire from 2026-09-07. |
| 16 | `catalog_mapping_report.md` | 14.3 KB | Initial catalog mapping feasibility study (Sep 7) | 0 | No | Historical report | Low | **Archive** (`docs/archive/reports/`) | Superseded on 2026-09-12 by `CATEGORY_MAPPING_REPORT.md` which confirmed binary `COMPMST` link. |
| 17 | `CATEGORY_MAPPING_REPORT.md` | 16.6 KB | Reverse-engineered category mapping report (Sep 12) | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Authoritative reverse-engineering specification proving `COMPMST` and `ITEMMST.CCODE` relationship. |
| 18 | `import_workflow_and_test_plan.md` | 13.2 KB | FoxPro native import workflow & test plan (Phase 3B) | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Documents Gate 1-4 duplicate protection, `import_staging.json` payload, and headless FoxPro `IMPORT.PRG`. |
| 19 | `invoice_creation_analysis.md` | 18.3 KB | FoxPro invoice import feasibility analysis (Phase 3A) | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Architectural analysis comparing direct DBF writes vs headless FoxPro script. |
| 20 | `legacy_catalog_strategy.md` | 8.0 KB | Legacy FoxPro catalog strategy & pipeline (Phase 2.6) | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Data pipeline architecture for FoxPro catalog ingestion. |
| 21 | `missing_data_report.md` | 9.9 KB | Missing sales data analysis & legacy mitigation | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Statistical analysis of missing or unpopulated fields in `SALEMST` and `ITEMMST`. |
| 22 | `required_fields.md` | 12.5 KB | FoxPro billing required fields & data dictionary | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Field-by-field data dictionary for `SALEMST`, `SALEITEM`, `BILLBOOK`, and `NAMEMST`. |
| 23 | `showroom_navigation.md` | 14.2 KB | Legacy showroom navigation architecture (Phase 2.6) | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Physical showroom layout and product section mapping document. |
| 24 | `table_relationships.md` | 12.9 KB | FoxPro billing table relationships & propagation | 0 | No | Architecture spec | Low | **Move** (`docs/specs/`) | Definitive reference for FoxPro `.CDX` compound index tags, primary keys, and data propagation. |
| 25 | `CATALOG_PACKAGING_REPORT.md` | 176 KB | Hardened catalog packaging rules report (Sep 19) | 0 | No | Business report | Low | **Move** (`docs/packaging/`) | Generated during recent packaging resolver development. Co-locating in `docs/packaging/` keeps root clean. |
| 26 | `PACKAGING_BUSINESS_REVIEW_WORKSHEET.md` | 151 KB | Product packaging rules business review worksheet | 1 (`PACKAGING_HISTORY_EVIDENCE_REPORT.md`) | No | Business review | Low | **Move** (`docs/packaging/`) | Active business review document for showroom owner sign-off. |
| 27 | `PACKAGING_HISTORY_EVIDENCE_REPORT.md` | 108 KB | Packaging rules historical sales evidence report | 0 | No | Business evidence | Low | **Move** (`docs/packaging/`) | Documents historical sales analysis for 439 candidate products. |
| 28 | `PACKAGING_RULE_DECISIONS.csv` | 100 KB | Packaging rule decision matrix (439 rows) | 1 (`PACKAGING_HISTORY_EVIDENCE_REPORT.md`) | No | Data export | Low | **Move** (`docs/packaging/`) | Complete export of empirical packaging decisions and GCD analysis. |
| 29 | `ACTIVE_RULE_RISK_REGISTER.md` | 11.4 KB | Active packaging rules risk register & pilot safety audit (Sep 19) | 0 | No | Risk register | Low | **Move** (`docs/packaging/`) | Safety audit of 32 approved overlay rules; co-located with packaging reports in `docs/packaging/`. |
| 30 | `tablet-app/screen.png` | 1.1 MB | Prototype screenshot (Sep 6) | 0 | No | Ad-hoc image | Zero | **Delete** | Untracked/unreferenced prototype screenshot taking 1.1 MB in git. Not referenced in web app or Android build. |
| 30 | `tablet-app/screenshot1.png` | 188 KB | Prototype screenshot (Sep 7) | 0 | No | Ad-hoc image | Zero | **Delete** | Unreferenced prototype image taking 188 KB in git. |
| 31 | `tablet-app/screenshot2_catalog.png` | 338 KB | Prototype screenshot (Sep 7) | 0 | No | Ad-hoc image | Zero | **Delete** | Unreferenced prototype image taking 338 KB in git. |
| 32 | `tablet-app/screenshot3_cart.png` | 358 KB | Prototype screenshot (Sep 7) | 0 | No | Ad-hoc image | Zero | **Delete** | Unreferenced prototype image taking 358 KB in git. |
| 33 | `tablet-app/screenshot4_offline_restart.png` | 324 KB | Prototype screenshot (Sep 7) | 0 | No | Ad-hoc image | Zero | **Delete** | Unreferenced prototype image taking 324 KB in git. |
| 34 | `vfp/CONFIG.FPW` & `vfp/IMPORT.PRG` | 23 KB | FoxPro headless import scripts at root | 0 | Redundant copy | Duplicate | Zero | **Delete** (Root copy) | Exactly identical (100% byte-for-byte match) to `sync-service/vfp/CONFIG.FPW` and `sync-service/vfp/IMPORT.PRG`. Canonical location is `sync-service/vfp/`. |
| 35 | `README.md` | 8.1 KB | Core project documentation & overview | Multiple | Yes (user doc) | Authoritative | High | **Retain** (Root) | Primary project readme; contains architectural ASCII diagram and deployment instructions. |
| 36 | `CHANGELOG.md` | 4.0 KB | Master project changelog | 1 (`FOOTER_REMOVAL_CHANGELOG.md`) | Yes (project doc) | Authoritative | High | **Retain** (Root) | Tracks all released versions (v0.1.0 to v1.0.0). |
| 37 | `VERSION` | 6 B | Semantic version single source of truth (`1.0.0`) | 11 | Yes (versioning) | Authoritative | High | **Retain** (Root) | Consumed by `tablet-app/scripts/sync-version.js` and `sync-service/app/__init__.py`. |
| 38 | `DEVELOPMENT_WORKFLOW.md` | 9.1 KB | Contribution & developer workflow guide | Referenced in README/scripts | Yes (dev doc) | Authoritative | High | **Retain** (Root) | Enforces zero-broken-build rules, conventional commit standards, and workflow scripts. |
| 39 | `WINDOWS_DEPLOYMENT_GUIDE.md` | 4.3 KB | Store administrator deployment guide | Referenced in README | Yes (operator doc) | Authoritative | High | **Retain** (Root) | Step-by-step production setup guide for store staff. |
| 40 | `config.sample.json` | 511 B | Root sample configuration template | 2 | Yes (sample config) | Template | High | **Retain** (Root) | Root-level template for rapid server configuration without exploring subdirectories. |
| 41 | `.gitignore` | 1.7 KB | Git file exclusion rules | 0 | Yes (git workflow) | Configuration | High | **Retain & Harden** | Standardizes file exclusions for macOS, Python, Node, Android, and temporary FoxPro files. |
| 42 | `scripts/workflow.sh` | 4.3 KB | Developer workflow automation script | Referenced in DEV_WORKFLOW | Yes (tooling) | Tooling | High | **Retain** | Automates test execution, syntax validation, commit validation, and git push. |
| 43 | `sync-service/` | ~300 KB | FastAPI backend, DBF engine, pack resolver, tests | Multiple | Yes (backend runtime) | Source code | High | **Retain** | Core Python sync service. |
| 44 | `tablet-app/` (clean) | ~3 MB | Android Capacitor POS application | Multiple | Yes (frontend runtime) | Source code | High | **Retain** | Core POS tablet client. |
| 45 | `PYRO-Sync-Service/` | 16 MB | Standalone 64-bit Windows deployment package | Referenced in deployment guide | Yes (deployment package) | Pre-built bundle | High | **Retain** | Bundled turnkey Windows executable package ready for store distribution. |
| 46 | `packaging/` | 16 KB | Windows cross-compilation toolchain & Dockerfiles | Packaging pipeline | Yes (build tooling) | Build scripts | High | **Retain** | Contains `build_windows_dist.sh` and verification scripts. |
| 47 | `legacy-software-extracted/` | 82 MB | Upstream Visual FoxPro database replica | Data source | Yes (data layer) | Production tables | High | **Retain** | Master inventory tables (`D2627/ITEMMST.DBF`, etc.) required for sync and testing. |

---

## 4. Remediation Plan & Link Preservation

### A. Archival Directory Structure
To organize archived files logically without cluttering root, the following directory hierarchy is established under `docs/`:

```text
docs/
├── archive/
│   ├── audits/
│   │   ├── DEPLOYMENT_AUDIT.md
│   │   ├── EXECUTABLE_AUDIT.md
│   │   ├── FOOTER_REMOVAL_AUDIT.md
│   │   ├── FOOTER_REMOVAL_CHANGELOG.md
│   │   └── TECHNICAL_AUDIT.md
│   ├── reports/
│   │   ├── EXE_BUILD_REPORT.md
│   │   ├── EXE_CHANGELOG.md
│   │   ├── EXECUTIVE_SUMMARY.md
│   │   ├── VERIFICATION_REPORT.md
│   │   └── catalog_mapping_report.md
│   ├── pilot/
│   │   ├── alpha_test_plan.md
│   │   ├── bug_tracker_template.md
│   │   └── operator_feedback_form.md
│   └── proofs/
│       ├── proof_footer_removed_cart.png
│       ├── proof_footer_removed_catalog.png
│       └── proof_footer_removed_checkout.png
├── specs/
│   ├── CATEGORY_MAPPING_REPORT.md
│   ├── import_workflow_and_test_plan.md
│   ├── invoice_creation_analysis.md
│   ├── legacy_catalog_strategy.md
│   ├── missing_data_report.md
│   ├── required_fields.md
│   ├── showroom_navigation.md
│   └── table_relationships.md
└── packaging/
    ├── ACTIVE_RULE_RISK_REGISTER.md
    ├── CATALOG_PACKAGING_REPORT.md
    ├── PACKAGING_BUSINESS_REVIEW_WORKSHEET.md
    ├── PACKAGING_HISTORY_EVIDENCE_REPORT.md
    └── PACKAGING_RULE_DECISIONS.csv
```

### B. Link Updates
1. **`docs/archive/audits/FOOTER_REMOVAL_AUDIT.md`**:  
   Update screenshot image references from root links to relative links targeting `../proofs/`:
   - `proof_footer_removed_catalog.png` $\to$ `../proofs/proof_footer_removed_catalog.png`
   - `proof_footer_removed_cart.png` $\to$ `../proofs/proof_footer_removed_cart.png`
   - `proof_footer_removed_checkout.png` $\to$ `../proofs/proof_footer_removed_checkout.png`
2. **`docs/packaging/PACKAGING_HISTORY_EVIDENCE_REPORT.md`**:  
   Verify that relative links to `PACKAGING_RULE_DECISIONS.csv` and `PACKAGING_BUSINESS_REVIEW_WORKSHEET.md` remain intact within `./`.

### C. Gitignore Hardening & Scoping
Runtime execution of `export_orders.py` and FoxPro `IMPORT.PRG` produces transient staging JSON payloads. To prevent polluting the repository tree while strictly protecting static test fixtures and JSON schemas, `.gitignore` is scoped narrowly:

```gitignore
# ==========================================
# Runtime Order Staging & Import Outputs
# ==========================================
# Ephemeral order staging and import execution outputs
/import_staging.json
/import_result.json
sync-service/import_staging.json
sync-service/import_result.json
PYRO-Sync-Service/import_staging.json
PYRO-Sync-Service/import_result.json

# Explicitly ensure test sample fixtures and schemas are never ignored
!sync-service/samples/import_staging.json
!sync-service/schemas/staging_schema.json

# ==========================================
# Test Coverage & Cache Outputs
# ==========================================
.coverage
htmlcov/
```

- **Runtime vs Fixture Audit:** Verified that `sync-service/samples/import_staging.json` and `sync-service/schemas/staging_schema.json` are required test contract files (tested by `test_exporter.py`). The negation rules (`!sync-service/samples/...`) ensure they remain tracked and visible.
- **Verification Command:** `git check-ignore -v ./import_staging.json sync-service/import_staging.json sync-service/samples/import_staging.json`
  - Output confirms `./import_staging.json` and `sync-service/import_staging.json` are ignored.
  - Output confirms `sync-service/samples/import_staging.json` is **not** ignored.

---

## 5. Cryptographic Verification: Duplicate Root `vfp/` Deletion

Before removing `vfp/CONFIG.FPW` and `vfp/IMPORT.PRG` from the repository root, cryptographic SHA-256 checksums were calculated and compared against their canonical counterparts in `sync-service/vfp/`:

| Artifact | Canonical Path | Deleted Root Path | SHA-256 Checksum | Match Status |
| :--- | :--- | :--- | :--- | :---: |
| **FoxPro Config** | `sync-service/vfp/CONFIG.FPW` | `vfp/CONFIG.FPW` | `9b1d40dca761ac62bb17d61e0f8da6341149435329e2e4acf5f0ef2a7307c4d2` | **IDENTICAL (100%)** |
| **FoxPro Import Script** | `sync-service/vfp/IMPORT.PRG` | `vfp/IMPORT.PRG` | `7a1dab16f0630af2fa130a75a6594b8827d6f20e1203b0cb95ba8e897fa2b7cc` | **IDENTICAL (100%)** |

**Conclusion:** The root files were bit-for-bit redundant duplicates committed during repository initialization (`b19609f`). Deleting the root copies leaves the canonical scripts in `sync-service/vfp/` completely intact with zero risk of data or code loss.

---

## 6. Comprehensive Reference Search & Dependency Audit

Every moved, archived, and deleted file was audited across all tracked repository text, configuration, script, and manifest files (including Python, JavaScript, shell scripts, batch files, Gradle configs, Dockerfiles, and JSON/YAML):

| Target File | Original Location | New Destination / Action | References Found | Disposition & Resolution Status |
| :--- | :--- | :--- | :---: | :--- |
| `DEPLOYMENT_AUDIT.md` | `/` | `docs/archive/audits/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `EXECUTABLE_AUDIT.md` | `/` | `docs/archive/audits/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `FOOTER_REMOVAL_AUDIT.md` | `/` | `docs/archive/audits/` | 7 | Updated internal proof links to `../proofs/`; listed in `FOOTER_REMOVAL_CHANGELOG.md` text. |
| `FOOTER_REMOVAL_CHANGELOG.md` | `/` | `docs/archive/audits/` | 7 | Listed in `ARTIFACT_AUDIT.md` and historical changelog text. |
| `TECHNICAL_AUDIT.md` | `/` | `docs/archive/audits/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `alpha_test_plan.md` | `/` | `docs/archive/pilot/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `bug_tracker_template.md` | `/` | `docs/archive/pilot/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `operator_feedback_form.md` | `/` | `docs/archive/pilot/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `proof_footer_removed_cart.png` | `/` | `docs/archive/proofs/` | 5 | Updated links in `FOOTER_REMOVAL_AUDIT.md` to `../proofs/proof_footer_removed_cart.png`. |
| `proof_footer_removed_catalog.png` | `/` | `docs/archive/proofs/` | 5 | Updated links in `FOOTER_REMOVAL_AUDIT.md` to `../proofs/proof_footer_removed_catalog.png`. |
| `proof_footer_removed_checkout.png` | `/` | `docs/archive/proofs/` | 5 | Updated links in `FOOTER_REMOVAL_AUDIT.md` to `../proofs/proof_footer_removed_checkout.png`. |
| `EXECUTIVE_SUMMARY.md` | `/` | `docs/archive/reports/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `EXE_BUILD_REPORT.md` | `/` | `docs/archive/reports/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `EXE_CHANGELOG.md` | `/` | `docs/archive/reports/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `VERIFICATION_REPORT.md` | `/` | `docs/archive/reports/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Zero operational code references. |
| `catalog_mapping_report.md` | `/` | `docs/archive/reports/` | 2 | `ARTIFACT_AUDIT.md` (audit table & tree). Superseded by `CATEGORY_MAPPING_REPORT.md`. |
| `CATEGORY_MAPPING_REPORT.md` | `/` | `docs/specs/` | 3 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `import_workflow_and_test_plan.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `invoice_creation_analysis.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `legacy_catalog_strategy.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `missing_data_report.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `required_fields.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `showroom_navigation.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `table_relationships.md` | `/` | `docs/specs/` | 2 | `ARTIFACT_AUDIT.md`. Specification document. Zero operational code references. |
| `CATALOG_PACKAGING_REPORT.md` | `/` | `docs/packaging/` | 2 | `ARTIFACT_AUDIT.md`. Business report. Zero operational code references. |
| `PACKAGING_BUSINESS_REVIEW_WORKSHEET.md` | `/` | `docs/packaging/` | 4 | Co-located relative links preserved (`./PACKAGING_BUSINESS_REVIEW_WORKSHEET.md`). |
| `PACKAGING_HISTORY_EVIDENCE_REPORT.md` | `/` | `docs/packaging/` | 5 | Co-located relative links preserved in `docs/packaging/`. |
| `PACKAGING_RULE_DECISIONS.csv` | `/` | `docs/packaging/` | 4 | Co-located relative link preserved in `PACKAGING_HISTORY_EVIDENCE_REPORT.md`. |
| `ACTIVE_RULE_RISK_REGISTER.md` | `/` | `docs/packaging/` | 5 | Co-located relative link preserved in `PACKAGING_BUSINESS_REVIEW_WORKSHEET.md`. |
| `screen.png` | `tablet-app/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Zero code or build references. |
| `screenshot1.png` | `tablet-app/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Zero code or build references. |
| `screenshot2_catalog.png` | `tablet-app/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Zero code or build references. |
| `screenshot3_cart.png` | `tablet-app/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Zero code or build references. |
| `screenshot4_offline_restart.png` | `tablet-app/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Zero code or build references. |
| `vfp/CONFIG.FPW` | `vfp/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Canonical version in `sync-service/vfp/CONFIG.FPW`. |
| `vfp/IMPORT.PRG` | `vfp/` | **DELETED** | 1 | `ARTIFACT_AUDIT.md`. Canonical version in `sync-service/vfp/IMPORT.PRG`. |

**Markdown Link Validation:** An automated link scanner verified **54 links across 62 markdown files**. **100% of relative links resolve to valid, existing files.**

---

## 7. Tablet Application Validation & Blocker Report

Validation commands and checks executed for the Android Tablet POS application:

| Check | Execution Command | Result | Blocker / Dependency Constraint |
| :--- | :--- | :---: | :--- |
| **Android Unit Tests** | `cd tablet-app/android && JAVA_HOME="/opt/homebrew/opt/openjdk@21" ./gradlew testDebugUnitTest` | **PASSED** | 53 actionable tasks executed, 0 failures. Ran `ExampleUnitTest`. |
| **Android Debug APK Compilation** | `cd tablet-app/android && JAVA_HOME="/opt/homebrew/opt/openjdk@21" ./gradlew assembleDebug` | **PASSED** | 93 actionable tasks executed, 0 failures. Output: `tablet-app/android/app/build/outputs/apk/debug/app-debug.apk`. |
| **Node.js Web Lint / Type Check** | `npm test` / `npm run build` | **BLOCKED** | `node`, `npm`, and `npx` are not installed on this host (`command not found: node`). Lockfiles were left unmodified. |
| **JavaScript Syntax Check** | `node -c tablet-app/app.js` | **BLOCKED** | Node runtime unavailable on local machine. Code verified by inspection against recent commits. |
| **Android Instrumentation Tests** | `./gradlew connectedDebugAndroidTest` | **BLOCKED** | Requires an attached physical tablet or running Android emulator (`adb devices` is empty). |

---

## 8. Windows Packaging Validation & Rebuild Qualification

Validation commands and dependency analysis for Windows packaging:

| Check | Target / Command | Result | Technical Qualification |
| :--- | :--- | :---: | :--- |
| **Packaging Inputs Inspection** | `packaging/build_windows_dist.sh` | **VERIFIED** | Source audit confirms packaging inputs depend exclusively on `sync-service/app/`. There are zero dependencies on `vfp/`, `docs/`, or root report files. |
| **Deployment Scripts Inspection** | `PYRO-Sync-Service/start_pyroja.bat`, `start_sync_service.bat` | **VERIFIED** | Scripts reference local `PYROJA.exe` and `PYRO-Sync-Service.exe` within the same folder. Untouched and functional. |
| **Full Windows Executable Rebuild** | Docker cross-compilation (`packaging/Dockerfile.dist_builder`) | **NOT RUN** | **Explicit Qualification:** A full Windows binary recompile was NOT performed. The Docker daemon is inactive (`unix:///Users/jayagrawal/.orbstack/run/docker.sock` unavailable) and `wine` is not installed on macOS. |
| **Wine Runtime Verification** | `packaging/verify_windows_deployment.sh` | **NOT RUN** | Requires Wine environment, unavailable on this host. |

---

## 9. Residual Risks, Deployment Impact & Rollback Procedure

- **Deployment Impact:**  
  *Qualified Low.* No runtime code or backend logic was altered. The standalone Windows deployment folder `PYRO-Sync-Service/` remains as committed in v1.0.0. All packaging scripts remain intact with unchanged inputs. Android Gradle debug build compiles cleanly.
- **Residual Risks:**  
  1. *Host Tooling Gap:* Node.js is not installed on this developer workstation, meaning `tablet-app/package.json` scripts (`npm run build`, `npm run sync`) require execution on a machine with Node 18+ installed.
  2. *Windows Rebuild Cadence:* When new Python features are deployed to production, `packaging/build_windows_dist.sh` must be executed within Docker to refresh `PYRO-Sync-Service/`.
- **Rollback Procedure:**  
  If any archived document or removed file is required in its previous location:
  ```bash
  # Option 1: Complete branch discard
  git checkout main
  git branch -D chore/repository-artifact-cleanup

  # Option 2: Selective commit revert
  git revert <commit-hash>
  ```

