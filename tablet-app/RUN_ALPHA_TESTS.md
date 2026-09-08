# PyroWholesale POS — Alpha Test Execution Guide

This guide provides step-by-step instructions for running the automated Espresso test suite, executing manual verification checklists, and diagnosing runtime behavior using Android Studio and ADB.

---

## 1. Prerequisites & Environment Setup

| Component | Minimum Version | Recommended Path / Setting |
|---|---|---|
| **Operating System** | macOS 14+ / Windows 10+ / Linux | macOS Apple Silicon / Intel |
| **Java Development Kit** | OpenJDK 21 LTS | `/opt/homebrew/opt/openjdk@21` |
| **Android SDK** | API 34+ (Build-Tools 34.0.0+) | `$HOME/Library/Android/sdk` |
| **Gradle** | 8.14.3 (bundled via `gradlew`) | `./gradlew` |
| **Target Device / AVD** | Android 9.0+ (API 28+) | Pixel Tablet (10.1" Landscape, API 35) |

---

## 2. Running Automated Tests via Android Studio

1. **Open the Project:**
   - Launch **Android Studio**.
   - Select **File** $\to$ **Open...**
   - Navigate to and select the directory:
     ```text
     /Users/jayagrawal/Documents/My Orders/tablet-app/android
     ```
   - Wait for the initial Gradle sync to complete (`BUILD SUCCESSFUL`).

2. **Configure JDK 21 in Android Studio:**
   - Open **Settings / Preferences** $\to$ **Build, Execution, Deployment** $\to$ **Build Tools** $\to$ **Gradle**.
   - Under **Gradle JDK**, ensure **JDK 21** is selected (e.g. `/opt/homebrew/opt/openjdk@21`).

3. **Launch the Target Emulator:**
   - Open **Device Manager** in Android Studio.
   - Start an emulator profile (recommended: **Pixel Tablet**, 2560x1600 Landscape).

4. **Execute Instrumentation Test Suite:**
   - In the **Project** explorer window, navigate to:
     ```text
     app -> src -> androidTest -> java -> com.pyrowholesale.pos -> PyroPosInstrumentationTest
     ```
   - Right-click `PyroPosInstrumentationTest` and select **Run 'PyroPosInstrumentationTest'**.
   - Android Studio will build the test APK, install it onto the emulator, and execute all 5 tests:
     - `test01_appLaunch`
     - `test02_indexedDbInitialization`
     - `test03_offlineModeStartup`
     - `test04_syncServiceUrlConfiguration`
     - `test05_productLoading`
   - Results will display in the **Run / Test Results** panel with green checkmarks.

---

## 3. Running Automated Tests via Command Line (CLI)

Run the full automated test suite directly from your terminal:

```bash
cd "tablet-app/android"

# Set JDK and Android SDK paths
export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$ANDROID_HOME/platform-tools:$PATH"

# Execute all connected Android instrumentation tests
./gradlew :app:connectedDebugAndroidTest --no-daemon
```

### Viewing Test Results
After execution, Gradle generates an interactive HTML report at:
```text
tablet-app/android/app/build/reports/androidTests/connected/debug/index.html
```
Open this file in your browser to inspect test durations, assertions, and device metadata.

---

## 4. Emulator Validation Checklist

Perform the following operational tests in the Android Emulator:

| # | Test Scenario | Steps to Execute | Expected Result | Pass/Fail |
|---|---|---|---|:---:|
| **1** | **Fresh Installation** | `adb install dist/pyrowholesale-pos-debug.apk` | App installs cleanly without package signature or manifest errors. | Pass |
| **2** | **App Upgrade Install** | Reinstall with `-r` flag: `adb install -r dist/pyrowholesale-pos-debug.apk` | Existing SQLite/IndexedDB data preserved; app updates with `Success`. | Pass |
| **3** | **Offline Startup** | Enable Airplane mode (`cmd connectivity airplane-mode enable`), kill process, and launch app. | App launches immediately (< 250ms), loads cached DBF records, displays `#99999 CASH A/C`, and marks status `OFFLINE`. | Pass |
| **4** | **Online Startup** | Start Windows Sync Service, disable Airplane mode, click `PULL DBF MASTERS`. | App contacts `http://10.0.2.2:8080`, downloads 3,019 products and 883 customers, and turns pill green (`ONLINE`). | Pass |
| **5** | **Device Rotation** | Rotate emulator from Landscape to Portrait and back (`user_rotation 0` $\to$ `1`). | WebView reflows smoothly without reload or cart state loss. | Pass |
| **6** | **Background / Resume** | Press HOME key (`input keyevent KEYCODE_HOME`), wait 5s, relaunch app. | App resumes instantly in foreground with existing draft ID, cart items, and search query intact. | Pass |

---

## 5. ADB Commands Reference Guide

### 5.1 Installation & Launch
```bash
# Install fresh APK
adb install dist/pyrowholesale-pos-debug.apk

# Reinstall / Upgrade preserving user data
adb install -r dist/pyrowholesale-pos-debug.apk

# Launch the POS application
adb shell am start -n com.pyrowholesale.pos/.MainActivity

# Force stop the application
adb shell am force-stop com.pyrowholesale.pos

# Clear all local app data (resets IndexedDB & cache)
adb shell pm clear com.pyrowholesale.pos

# Uninstall the application
adb uninstall com.pyrowholesale.pos
```

### 5.2 Real-time Log Collection & Filtering
```bash
# Clear log buffer
adb logcat -c

# Stream only Capacitor & WebView JavaScript console logs
adb logcat -v time "Capacitor:D" "Capacitor/Console:V" "chromium:V" "*:S"

# Stream all POS-related messages
adb logcat -v time | grep -i -E "(PyroWholesale|Capacitor|chromium|IndexedDB)"

# Export recent 5000 lines of logcat to file
adb logcat -d -t 5000 > alpha_logcat.txt
```

### 5.3 Crash Diagnosis & System Health
```bash
# View fatal crash stack traces
adb logcat -b crash -d

# Check system dropbox for ANRs or native crashes
adb shell dumpsys dropbox --print | grep -i -E "(crash|anr|com.pyrowholesale.pos)"

# Inspect active memory usage
adb shell dumpsys meminfo com.pyrowholesale.pos

# Check CPU consumption
adb shell top -n 1 | grep com.pyrowholesale.pos
```

### 5.4 Live Chrome DevTools Protocol (CDP) Remote Debugging
Because `webContentsDebuggingEnabled: true` is enabled in `capacitor.config.json`, you can inspect the running tablet app from your desktop:

1. Connect tablet or emulator via ADB.
2. Open Google Chrome on your computer.
3. Navigate to:
   ```text
   chrome://inspect/#devices
   ```
4. Click **Inspect** under `PYROWHOLESALE - Tablet POS Workstation` to open Chrome DevTools:
   - **Console:** Test JavaScript commands live (`window.pos.products.length`).
   - **Application $\to$ IndexedDB:** Inspect raw SQLite-backed tables (`products`, `customers`, `drafts`, `sync_queue`).
   - **Network:** View API latency and payload schemas.
