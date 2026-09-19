"""Desktop application launcher supporting GUI and headless operation."""

import argparse
import logging
import multiprocessing
from pathlib import Path
import socket
import sys
from typing import Optional

from app import __version__
from app.desktop.server_runner import ServerRunner
from app.desktop.settings import ControlPanelSettings, load_settings, to_app_config
from app.desktop.ui import TKINTER_AVAILABLE, run_gui
from app.desktop.validator import validate_foxpro_folder

logger = logging.getLogger("PYROJA.Launcher")

INSTANCE_LOCK_PORT = 28080


def acquire_instance_lock(port: int = INSTANCE_LOCK_PORT) -> Optional[socket.socket]:
    """Acquire a local socket lock to guarantee single-instance execution."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        return sock
    except OSError:
        sock.close()
        return None


def run_headless(settings: ControlPanelSettings) -> None:
    """Run server in headless console mode without desktop GUI."""
    print("=" * 65)
    print(f"       PYROJA FoxPro Sync Service v{__version__} (Headless Mode)")
    print("=" * 65)
    print(f"Active FoxPro Data: {settings.foxpro_data_path}")
    print(f"Service Port:       {settings.port}")
    print(f"Bind Host:          {settings.host}")

    val = validate_foxpro_folder(settings.foxpro_data_path)
    if not val.valid:
        print(f"\n[ERROR] FoxPro Folder Validation Failed:\n{val.error_message}")
        sys.exit(1)

    print("\nFoxPro DBF Tables Verified (Strictly Read-Only):")
    for name, info in val.tables.items():
        if info.exists:
            print(f"  • {name}: OK ({info.record_count} records, {info.size_bytes:,} bytes)")
        else:
            print(f"  • {name}: MISSING")

    import uvicorn
    from app.main import create_app

    app_cfg = to_app_config(settings)
    app = create_app(app_cfg)

    print(f"\n[STATUS] Starting Uvicorn server on http://{settings.host}:{settings.port}")
    print("Press CTRL+C to stop.\n")

    try:
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level.lower(),
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by operator.")


def main() -> None:
    """Main application entry point."""
    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser(
        description="PYROJA FoxPro Sync Service & Desktop Control Panel",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless console mode without GUI",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to custom settings JSON file",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Override service port number",
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Override FoxPro live data directory",
    )
    args = parser.parse_args()

    settings_path = Path(args.config) if args.config else None
    settings = load_settings(settings_path)

    if args.port:
        settings.port = args.port
    if args.data_path:
        settings.foxpro_data_path = args.data_path

    if args.headless or not TKINTER_AVAILABLE:
        if not TKINTER_AVAILABLE and not args.headless:
            print("[INFO] Tkinter not available in current environment; starting in headless mode.")
        run_headless(settings)
        return

    # Single-instance check for GUI
    lock_sock = acquire_instance_lock()
    if lock_sock is None:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(
                "PYROJA Already Running",
                "Another instance of the PYROJA Control Panel is already open on this computer.",
            )
            root.destroy()
        except Exception:
            print("Error: Another instance of PYROJA Control Panel is already running.")
        sys.exit(0)

    # Launch GUI
    try:
        run_gui(settings_path=settings_path)
    finally:
        if lock_sock:
            try:
                lock_sock.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
