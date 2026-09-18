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

### C. Gitignore Hardening
Add explicit exclusion rules in `.gitignore` to prevent runtime generation of order staging files and test coverage from polluting Git status:
```gitignore
# Runtime staging and FoxPro result files
import_staging.json
import_result.json

# Test coverage outputs
.coverage
htmlcov/
```

---

## 5. Risk Assessment & Verification Directives

- **Sync Service Impact:** Zero. All Python code and tests in `sync-service/` remain 100% intact. Tests continue targeting `sync-service/app/`.
- **Tablet POS Impact:** Zero. Obsolete screenshots in `tablet-app/` were unreferenced; all web assets (`index.html`, `app.js`, `fonts/`, `tailwind.cdn.js`) and Capacitor configurations are untouched.
- **Windows Packaging Impact:** Zero. `PYRO-Sync-Service/` and `packaging/` remain fully functional.
- **Verification Gates:**
  1. Full execution of backend test suite (`pytest sync-service/tests/ -v`).
  2. Verification of JavaScript syntax (`node -c tablet-app/app.js`).
  3. Verification that no broken relative links exist in documentation.
  4. Git tree verification to ensure clean status with zero untracked clutter.
