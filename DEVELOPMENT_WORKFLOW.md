# PYROJA Developer Workflow & Contribution Guidelines

This document defines the engineering standards, automated validation pipelines, and git contribution workflow for **PYROJA** (Android Tablet POS & Windows Sync Service for RAM FATAKA CENTER).

---

## 1. Core Principles

1. **Zero-Broken-Build Policy:** Never commit or push code that fails automated test suites, introduces syntax errors, or breaks Android APK compilation.
2. **Atomic Conventional Commits:** Every code change must be accompanied by a validated git commit following the [Conventional Commits](https://www.conventionalcommits.org/) standard.
3. **Architectural Invariants:**
   - Android Package ID must remain **`com.pyrowholesale.pos`** to ensure seamless in-place APK updates (`adb install -r`) without clearing operator data.
   - IndexedDB database name is standardized as **`PYROJA`** (backed by automated non-destructive migration from legacy databases).
   - FoxPro `.DBF` table operations must remain strictly zero-locking during read operations.
   - All tablet orders must target the Estimate billbook series (**`BILLBOOK.CODE == 'E '`**).

---

## 2. Automated Developer Workflow Script

PYROJA includes a workflow script located at [`scripts/workflow.sh`](scripts/workflow.sh) that automates the entire validation, staging, committing, and remote pushing cycle.

### Usage

```bash
# Standard workflow after modifying code
./scripts/workflow.sh "<type>(<scope>): <subject>"

# Workflow including Android APK build & packaging
./scripts/workflow.sh "<type>(<scope>): <subject>" --build-apk
```

### Examples

```bash
# Adding a feature to the wholesale stepper
./scripts/workflow.sh "feat(stepper): add 10x pack multiplier button"

# Fixing a cart calculation issue
./scripts/workflow.sh "fix(cart): correct round-off calculation on GST exempt fireworks"

# Updating documentation
./scripts/workflow.sh "docs(readme): add Windows firewall troubleshooting guide"

# Compiling a new production APK release
./scripts/workflow.sh "build(android): compile release candidate APK" --build-apk
```

---

## 3. Workflow Pipeline Steps

When `./scripts/workflow.sh` executes, it performs four sequential gates:

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ Gate 1: Pre-Commit Validation                               │
 │ • sync-service pytest suite (all 26 test suites)            │
 │ • tablet-app JavaScript syntax check (node -c)              │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Passes
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Gate 2: Native Android Verification (if --build-apk)        │
 │ • npm run sync (sync web assets to Android platform)        │
 │ • ./gradlew assembleDebug --no-daemon                       │
 │ • Copy APK to tablet-app/dist/pyroja-pos-debug.apk          │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Passes
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Gate 3: Git Staging & Conventional Commit                   │
 │ • Validate commit message regex against Conventional Spec   │
 │ • git add -A                                                │
 │ • git commit -m "<message>"                                 │
 │ • Output commit hash (HEAD) and branch                      │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Passes
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Gate 4: Remote Push Protocol                                │
 │ • Check git remote:                                         │
 │   - If remote exists: push HEAD to origin branch            │
 │   - If remote does not exist: report push was skipped       │
 └─────────────────────────────────────────────────────────────┘
```

If any gate fails, the script halts execution immediately (`set -euo pipefail`), preventing broken code from being committed or pushed.

---

## 4. Conventional Commit Standards

All commits must conform to the following pattern:

```text
<type>(<scope>): <subject>
```

### Allowed Types

| Type | Description | Example Scope |
| :--- | :--- | :--- |
| **`feat`** | Introduces a new feature or capability | `feat(cart):`, `feat(stepper):`, `feat(sync):` |
| **`fix`** | Patches a bug or resolves an issue | `fix(auth):`, `fix(dbf):`, `fix(tabs):` |
| **`docs`** | Documentation-only changes | `docs(readme):`, `docs(api):` |
| **`refactor`** | Code reorganization with no behavior change | `refactor(header):`, `refactor(models):` |
| **`build`** | Build system, Gradle, dependencies, or APK output | `build(android):`, `build(deps):` |
| **`test`** | Adding or correcting test cases | `test(orders):`, `test(api):` |
| **`perf`** | Performance improvement | `perf(dbf):`, `perf(indexeddb):` |
| **`chore`** | Maintenance, formatting, or project housekeeping | `chore(git):`, `chore(clean):` |

---

## 5. Manual Step-by-Step Validation (Reference)

If executing steps individually without the automated script:

### A. Python Backend Sync Service
```bash
cd sync-service

# Activate virtual environment
source .venv/bin/activate  # macOS / Linux
# or .venv\Scripts\activate.bat on Windows

# Run tests
pytest tests/ -v
```

### B. Tablet POS Web & JavaScript
```bash
cd tablet-app

# Syntax check
node -c app.js

# Build web distribution
npm run build
```

### C. Android Native Container & APK Build
```bash
cd tablet-app

# Sync Capacitor assets
npm run sync

# Build debug APK with Gradle
cd android
export ANDROID_HOME="$HOME/Library/Android/sdk"
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
./gradlew assembleDebug --no-daemon

# Copy binary to distribution directory
cp app/build/outputs/apk/debug/app-debug.apk ../dist/pyroja-pos-debug.apk
```

---

## 6. Remote Push Protocol

- **When a Remote Exists:**  
  The workflow script pushes to the tracked remote branch (`origin <current-branch>`). If authentication or network issues occur, the script alerts the developer while ensuring the local commit remains safe.
- **When No Remote Exists (Offline Local Dev):**  
  The script displays:
  ```text
  Notice: No git remote configured. Push skipped.
  ```
  This allows seamless local offline development on showroom tablets or standalone laptops without throwing errors.

---

## 7. Semantic Versioning & Release Lifecycle

PYROJA enforces strict Semantic Versioning (`MAJOR.MINOR.PATCH[-PRERELEASE]`):

### Single Source of Truth (`VERSION`)
The version is governed by the root [`VERSION`](VERSION) file (e.g. `0.1.0-alpha`).

### Version Synchronization Pipeline
1. `tablet-app/scripts/sync-version.js` generates `tablet-app/version.js` and `tablet-app/version.json`.
2. `tablet-app/index.html` renders the dynamic badge:
   ```html
   <span id="app-version-badge">v0.1.0-alpha</span>
   ```
3. `sync-service/app/__init__.py` exposes `__version__` across FastAPI endpoints (`GET /` and `GET /api/health`).

### Release Procedure
To cut a new release (e.g. `0.2.0-beta`):
```bash
# 1. Update VERSION file
echo "0.2.0-beta" > VERSION

# 2. Execute automated workflow with APK compilation
./scripts/workflow.sh "chore(release): bump version to 0.2.0-beta" --build-apk

# 3. Create git tag
git tag -a "v0.2.0-beta" -m "Release v0.2.0-beta"
git push origin "v0.2.0-beta"
```

---

## 8. Protected Files & Directories

To prevent accidental data loss or breaking field deployments, the following files should **never** be manually overwritten or modified without explicit team approval:

1. `legacy-software-extracted/FAVWIN/D2627/*.DBF` — Master FoxPro production tables.
2. `tablet-app/android/app/src/main/res/values/strings.xml` — `package_name` must stay `com.pyrowholesale.pos` (until post-Alpha).
3. `tablet-app/app.js` — IndexedDB database name `PYROJA`.
