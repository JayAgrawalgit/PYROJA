"""Packaging script for PYROJA Desktop Control Panel.

Usage:
  python packaging/build_windows_control_panel.py [--clean]

On Windows:
  Compiles a standalone, zero-dependency Windows executable (PYROJA-Control-Panel.exe)
  using PyInstaller and outputs to dist/PYROJA-Control-Panel/.

On macOS / Linux:
  Performs pre-flight checks, verifies all spec files and dependencies,
  and outputs detailed instructions for Windows compilation.
"""

import argparse
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Build PYROJA Desktop Control Panel for Windows")
    parser.add_argument("--clean", action="store_true", help="Clean build directories before packaging")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    sync_service_dir = repo_root / "sync-service"
    spec_file = sync_service_dir / "pyroja_control_panel.spec"

    print("=" * 70)
    print("        PYROJA Standalone Windows Packaging Builder")
    print("=" * 70)
    print(f"Repository Root:    {repo_root}")
    print(f"Sync Service Path:  {sync_service_dir}")
    print(f"PyInstaller Spec:   {spec_file}")
    print(f"Host Platform:      {platform.system()} ({platform.machine()})")
    print(f"Python Version:     {platform.python_version()}")

    if not spec_file.exists():
        print(f"[ERROR] PyInstaller spec file not found: {spec_file}")
        sys.exit(1)

    # Verify critical application data
    rules_json = sync_service_dir / "app" / "data" / "catalog_pack_rules.json"
    if not rules_json.exists():
        print(f"[ERROR] Required catalog packaging rules missing: {rules_json}")
        sys.exit(1)
    else:
        print(f"[OK] Found catalog rules: {rules_json}")

    # Check for PyInstaller
    try:
        import PyInstaller
        has_pyinstaller = True
        print(f"[OK] PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        has_pyinstaller = False
        print("[WARNING] PyInstaller is not installed in the active environment.")

    is_windows = platform.system().lower() == "windows"

    if is_windows:
        print("\n--- Running Windows Native PyInstaller Build ---")
        if not has_pyinstaller:
            print("[INFO] Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

        dist_dir = sync_service_dir / "dist"
        build_dir = sync_service_dir / "build"

        if args.clean:
            print("[INFO] Cleaning existing build and dist folders...")
            shutil.rmtree(dist_dir, ignore_errors=True)
            shutil.rmtree(build_dir, ignore_errors=True)

        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            str(spec_file),
        ]
        print(f"Executing: {' '.join(cmd)}")
        subprocess.check_call(cmd, cwd=str(sync_service_dir))

        output_exe = dist_dir / "PYROJA-Control-Panel.exe"
        if output_exe.exists():
            print(f"\n[SUCCESS] Standalone Windows executable built successfully:")
            print(f"  -> {output_exe} ({output_exe.stat().st_size:,} bytes)")
        else:
            print(f"\n[INFO] Build completed. Output files located in: {dist_dir}")
    else:
        print("\n" + "-" * 70)
        print("Note: PyInstaller builds standalone binaries for the host OS platform.")
        print(f"To compile the native Windows .exe on the Windows 10 target machine:")
        print("-" * 70)
        print("1. Open PowerShell or Command Prompt on the Windows 10 PC.")
        print("2. Navigate to the repository directory:")
        print("   cd C:\\path\\to\\PYROJA\\sync-service")
        print("3. Install PyInstaller in your Python environment:")
        print("   pip install pyinstaller")
        print("4. Execute the build command:")
        print("   pyinstaller --clean pyroja_control_panel.spec")
        print("\nOutput binary will be generated at:")
        print("   sync-service\\dist\\PYROJA-Control-Panel.exe")
        print("=" * 70)


if __name__ == "__main__":
    main()
