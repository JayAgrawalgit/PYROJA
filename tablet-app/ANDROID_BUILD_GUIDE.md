# Android Build & Compilation Guide (macOS)
**Application:** PYROJA Tablet POS  
**Package Name:** `com.pyrowholesale.pos`  
**Framework:** Capacitor 8.5 on Android Native Wrapper  
**Target Platform:** Android 7.0+ (API 24 to API 36)

---

## 1. Project Stack & Architecture

- **Web Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript (`app.js`, `index.html`)
- **Native Container:** `@capacitor/core` + `@capacitor/android` v8.5.1
- **Local Storage:** IndexedDB with SQLite backing inside Android WebView (offline-first)
- **Networking:** Local WiFi cleartext HTTP REST client to Windows Sync Service (`:8080`)
- **Native Project Directory:** `tablet-app/android/`

---

## 2. Generated Artifacts

| Artifact | File Location | Size | Description |
|---|---|:---:|---|
| **Debug APK (Top-Level)** | [**`tablet-app/dist/pyroja-pos-debug.apk`**](file:///Users/jayagrawal/Documents/PYROJA/tablet-app/dist/pyroja-pos-debug.apk) | 8.7 MB | Ready to install on Android tablets. |
| **Gradle Output APK** | [**`tablet-app/android/app/build/outputs/apk/debug/app-debug.apk`**](file:///Users/jayagrawal/Documents/My%20Orders/tablet-app/android/app/build/outputs/apk/debug/app-debug.apk) | 3.9 MB | Direct build output from Gradle. |
| **Android Manifest** | [**`tablet-app/android/app/src/main/AndroidManifest.xml`**](file:///Users/jayagrawal/Documents/My%20Orders/tablet-app/android/app/src/main/AndroidManifest.xml) | — | Configured with `usesCleartextTraffic="true"` and network permissions. |
| **Capacitor Config** | [**`tablet-app/capacitor.config.json`**](file:///Users/jayagrawal/Documents/My%20Orders/tablet-app/capacitor.config.json) | — | Native cleartext, server scheme, and WebView debugging config. |
| **Package Manifest** | [**`tablet-app/package.json`**](file:///Users/jayagrawal/Documents/My%20Orders/tablet-app/package.json) | — | Build and sync automation scripts. |

---

## 3. Prerequisites for Building on macOS

1. **Node.js:** v18+ (tested with v26.8.1)
2. **Java Development Kit:** OpenJDK 21 LTS (located at `/opt/homebrew/opt/openjdk@21`)
3. **Android SDK:** Command-line tools / platform-tools (located at `~/Library/Android/sdk`)

---

## 4. Build & Compilation Commands

### One-Command Quick Build (from `tablet-app/`):
```bash
cd "tablet-app"

# 1. Set environment variables
export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$PATH"

# 2. Sync web assets and build debug APK
npm run build:apk
```

### Manual Step-by-Step Build:
```bash
cd "tablet-app"

# Step 1: Copy HTML/JS to web assets directory
npm run build

# Step 2: Sync Capacitor web assets into Android project
npx cap sync android

# Step 3: Compile APK using Gradle wrapper
cd android
export JAVA_HOME="/opt/homebrew/opt/openjdk@21"
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$PATH"

./gradlew assembleDebug
```

---

## 5. Installing the APK on Connected Android Tablets

Connect the tablet via USB with "USB Debugging" enabled:

```bash
# Verify device is connected
adb devices

# Install APK directly
adb install -r tablet-app/dist/pyroja-pos-debug.apk

# Launch App on Tablet
adb shell am start -n com.pyrowholesale.pos/com.pyrowholesale.pos.MainActivity
```

---

## 6. Configuring Local WiFi Sync on the Tablet

When the app opens on the Android tablet:
1. Tap the **"CONNECTING..."** or **"ONLINE"** status badge in the top navigation bar.
2. In the prompt, enter the Windows Sync Service IP and port on your shop WiFi:
   ```
   http://192.168.1.100:8080
   ```
3. The app saves this URL to local persistent storage (`localStorage` & SQLite metadata).
4. Tap **"PULL DBF MASTERS"** to download the 1,091 active products and customer accounts.
5. All subsequent orders are saved locally in SQLite and auto-synced over WiFi to the shop PC.
