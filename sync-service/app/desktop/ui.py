"""Tkinter Desktop Control Panel GUI for PYROJA FoxPro Sync Service."""

import logging
from pathlib import Path
import queue
import threading
import time
from typing import Optional

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    import tkinter.scrolledtext as scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    tk = None  # type: ignore
    ttk = None  # type: ignore
    filedialog = None  # type: ignore
    messagebox = None  # type: ignore
    scrolledtext = None  # type: ignore
    TKINTER_AVAILABLE = False

from app.desktop.server_runner import ServerRunner, ServerState
from app.desktop.settings import (
    ControlPanelSettings,
    load_settings,
    reset_to_defaults,
    save_settings,
)
from app.desktop.validator import (
    get_primary_lan_ip,
    get_tablet_url,
    is_port_available,
    validate_foxpro_folder,
)

logger = logging.getLogger("PYROJA.ControlPanel.UI")


class ControlPanelApp:
    """Main Tkinter desktop application controller."""

    def __init__(self, root: "tk.Tk", settings_path: Optional[Path] = None):
        if not TKINTER_AVAILABLE:
            raise RuntimeError("Tkinter is not available in this Python environment.")

        self.root = root
        self.settings_path = settings_path
        self.settings: ControlPanelSettings = load_settings(self.settings_path)

        self.runner = ServerRunner(on_state_change=self._on_server_state_change)
        self.log_poll_interval_ms = 100

        self._setup_window()
        self._create_widgets()
        self._bind_events()
        self._update_ui_state()

        # Start background queue poller
        self.root.after(self.log_poll_interval_ms, self._poll_log_queue)

        # Initial folder & port validation check in log
        self._initial_diagnostics()

    def _setup_window(self) -> None:
        self.root.title("PYROJA FoxPro Sync Service - Desktop Control Panel")
        self.root.geometry("780x680")
        self.root.minsize(700, 600)

        # Style configuration
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

    def _create_widgets(self) -> None:
        main_frame = ttk.Frame(self.root, padding="12")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ------------------------------------------------------------------
        # Header Frame: Title and Status Badge
        # ------------------------------------------------------------------
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT)

        title_lbl = ttk.Label(
            title_box,
            text="PYROJA FoxPro Sync Service",
            font=("Helvetica", 16, "bold"),
        )
        title_lbl.pack(anchor=tk.W)

        subtitle_lbl = ttk.Label(
            title_box,
            text="Local LAN Gateway between Android POS Tablets and FoxPro FAVWIN",
            font=("Helvetica", 10),
            foreground="#555555",
        )
        subtitle_lbl.pack(anchor=tk.W)

        # Status badge
        self.status_badge_var = tk.StringVar(value="STOPPED")
        self.status_badge = tk.Label(
            header_frame,
            textvariable=self.status_badge_var,
            font=("Helvetica", 11, "bold"),
            bg="#757575",
            fg="white",
            padx=14,
            pady=6,
            relief=tk.FLAT,
        )
        self.status_badge.pack(side=tk.RIGHT, pady=4)

        # ------------------------------------------------------------------
        # Section 1: FoxPro Live Data Settings
        # ------------------------------------------------------------------
        foxpro_frame = ttk.LabelFrame(
            main_frame,
            text=" FoxPro Live Data Directory (Strictly Read-Only) ",
            padding="10",
        )
        foxpro_frame.pack(fill=tk.X, pady=(0, 10))

        path_row = ttk.Frame(foxpro_frame)
        path_row.pack(fill=tk.X, pady=2)

        self.path_var = tk.StringVar(value=self.settings.foxpro_data_path)
        self.path_entry = ttk.Entry(path_row, textvariable=self.path_var, font=("Consolas", 10))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        self.browse_btn = ttk.Button(path_row, text="Browse...", command=self._on_browse_folder)
        self.browse_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.test_folder_btn = ttk.Button(path_row, text="Test Folder", command=self._on_test_folder)
        self.test_folder_btn.pack(side=tk.LEFT)

        self.folder_status_var = tk.StringVar(value="Path set to default live data location.")
        self.folder_status_lbl = ttk.Label(
            foxpro_frame,
            textvariable=self.folder_status_var,
            font=("Helvetica", 9),
            foreground="#2e7d32",
        )
        self.folder_status_lbl.pack(anchor=tk.W, pady=(4, 0))

        # ------------------------------------------------------------------
        # Section 2: Network & Tablet Pairing
        # ------------------------------------------------------------------
        net_frame = ttk.LabelFrame(main_frame, text=" Network & Tablet Pairing ", padding="10")
        net_frame.pack(fill=tk.X, pady=(0, 10))

        # Row 1: Port and Conflict Test
        port_row = ttk.Frame(net_frame)
        port_row.pack(fill=tk.X, pady=2)

        port_lbl = ttk.Label(port_row, text="Service Port:")
        port_lbl.pack(side=tk.LEFT, padx=(0, 6))

        self.port_var = tk.StringVar(value=str(self.settings.port))
        self.port_entry = ttk.Entry(port_row, textvariable=self.port_var, width=8, font=("Consolas", 10))
        self.port_entry.pack(side=tk.LEFT, padx=(0, 8))

        self.check_port_btn = ttk.Button(port_row, text="Check Port", command=self._on_check_port)
        self.check_port_btn.pack(side=tk.LEFT, padx=(0, 16))

        self.lan_var = tk.BooleanVar(value=self.settings.bind_lan)
        self.lan_check = ttk.Checkbutton(
            port_row,
            text="Allow Tablet Wi-Fi Access (0.0.0.0)",
            variable=self.lan_var,
            command=self._on_lan_toggle,
        )
        self.lan_check.pack(side=tk.LEFT)

        # Row 2: Tablet Connection URL display
        url_row = ttk.Frame(net_frame)
        url_row.pack(fill=tk.X, pady=(8, 2))

        url_lbl = ttk.Label(url_row, text="Tablet Connection Address:", font=("Helvetica", 10, "bold"))
        url_lbl.pack(side=tk.LEFT, padx=(0, 6))

        self.url_var = tk.StringVar(value=self._compute_tablet_url())
        self.url_entry = ttk.Entry(
            url_row,
            textvariable=self.url_var,
            font=("Consolas", 10, "bold"),
            state="readonly",
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        self.copy_url_btn = ttk.Button(url_row, text="Copy URL", command=self._on_copy_url)
        self.copy_url_btn.pack(side=tk.LEFT)

        # ------------------------------------------------------------------
        # Section 3: Action Controls
        # ------------------------------------------------------------------
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start Server",
            font=("Helvetica", 11, "bold"),
            bg="#2e7d32",
            fg="white",
            padx=14,
            pady=6,
            relief=tk.RAISED,
            command=self._on_start_server,
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ Stop Server",
            font=("Helvetica", 11, "bold"),
            bg="#c62828",
            fg="white",
            padx=14,
            pady=6,
            relief=tk.RAISED,
            state=tk.DISABLED,
            command=self._on_stop_server,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.health_btn = ttk.Button(btn_frame, text="Check Health", command=self._on_check_health)
        self.health_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.save_btn = ttk.Button(btn_frame, text="Save Settings", command=self._on_save_settings)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.reset_btn = ttk.Button(btn_frame, text="Reset to Defaults", command=self._on_reset_defaults)
        self.reset_btn.pack(side=tk.RIGHT)

        # ------------------------------------------------------------------
        # Section 4: Live Activity & Log Console
        # ------------------------------------------------------------------
        log_frame = ttk.LabelFrame(main_frame, text=" Real-Time Server & Sync Activity ", padding="8")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        log_tools_row = ttk.Frame(log_frame)
        log_tools_row.pack(fill=tk.X, pady=(0, 4))

        log_tip = ttk.Label(
            log_tools_row,
            text="Displays FoxPro table verification, health checks, and tablet API requests.",
            font=("Helvetica", 8),
            foreground="#666666",
        )
        log_tip.pack(side=tk.LEFT)

        clear_log_btn = ttk.Button(log_tools_row, text="Clear Logs", command=self._on_clear_logs)
        clear_log_btn.pack(side=tk.RIGHT)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            height=12,
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # ------------------------------------------------------------------
        # Status Bar
        # ------------------------------------------------------------------
        status_bar_frame = ttk.Frame(main_frame)
        status_bar_frame.pack(fill=tk.X)

        self.status_bar_var = tk.StringVar(value="Ready. Click 'Start Server' to begin.")
        self.status_bar = ttk.Label(
            status_bar_frame,
            textvariable=self.status_bar_var,
            font=("Helvetica", 9),
        )
        self.status_bar.pack(side=tk.LEFT)

        version_lbl = ttk.Label(
            status_bar_frame,
            text="v1.0.0 (Windows Standalone)",
            font=("Helvetica", 9),
            foreground="#888888",
        )
        version_lbl.pack(side=tk.RIGHT)

    def _bind_events(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_closing)
        self.port_var.trace_add("write", lambda *args: self._update_tablet_url_display())

    def _initial_diagnostics(self) -> None:
        """Run initial folder and port checks and print status in log."""
        self._append_log("[INFO] PYROJA Control Panel initialized.")
        self._append_log(f"[INFO] FoxPro data path configured: {self.settings.foxpro_data_path}")
        self._append_log(f"[INFO] API port configured: {self.settings.port}")

        # Non-blocking folder test
        val = validate_foxpro_folder(self.settings.foxpro_data_path)
        if val.valid:
            self._append_log(f"[INFO] FoxPro live tables verified read-only: ITEMMST.DBF, NAMEMST.DBF, SALETRN.DBF found.")
            self.folder_status_var.set("OK: Required FoxPro tables found and verified read-only.")
            self.folder_status_lbl.configure(foreground="#2e7d32")
        else:
            self._append_log(f"[WARNING] FoxPro folder check: {val.error_message}")
            self.folder_status_var.set(f"Note: {val.error_message}")
            self.folder_status_lbl.configure(foreground="#c62828")

    def _compute_tablet_url(self) -> str:
        ip = get_primary_lan_ip() if self.lan_var.get() else "127.0.0.1"
        try:
            port = int(self.port_var.get().strip())
        except (ValueError, TypeError):
            port = self.settings.port
        return get_tablet_url(ip, port)

    def _update_tablet_url_display(self) -> None:
        self.url_var.set(self._compute_tablet_url())

    def _on_lan_toggle(self) -> None:
        self._update_tablet_url_display()

    def _on_copy_url(self) -> None:
        url = self.url_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(url)
        self.status_bar_var.set(f"Copied '{url}' to clipboard.")
        self._append_log(f"[INFO] Copied tablet URL {url} to clipboard.")

    def _on_browse_folder(self) -> None:
        chosen = filedialog.askdirectory(
            initialdir=self.path_var.get() if Path(self.path_var.get()).exists() else "D:\\",
            title="Select FoxPro Data Directory (e.g. D:\\FAVWIN\\D2627)",
        )
        if chosen:
            self.path_var.set(chosen)
            self._on_test_folder()

    def _on_test_folder(self) -> None:
        path = self.path_var.get().strip()
        val = validate_foxpro_folder(path)
        if val.valid:
            details = []
            for name, info in val.tables.items():
                if info.exists:
                    details.append(f"{name}: {info.record_count} records ({info.size_bytes:,} bytes)")
            details_str = "\n".join(f"  • {d}" for d in details)

            self.folder_status_var.set("Folder verified! All required tables are readable.")
            self.folder_status_lbl.configure(foreground="#2e7d32")
            self._append_log(f"[INFO] Folder test PASSED for: {path}\n{details_str}")
            messagebox.showinfo(
                "FoxPro Folder Valid",
                f"Successfully verified FoxPro live data directory (Strictly Read-Only):\n{path}\n\n"
                f"Tables Found:\n{details_str}",
            )
        else:
            self.folder_status_var.set(f"Error: {val.error_message}")
            self.folder_status_lbl.configure(foreground="#c62828")
            self._append_log(f"[ERROR] Folder test FAILED for {path}: {val.error_message}")
            messagebox.showerror(
                "FoxPro Folder Invalid",
                f"Folder validation failed:\n\n{val.error_message}\n\n"
                f"Please ensure the path points to the active financial year directory containing ITEMMST.DBF.",
            )

    def _on_check_port(self) -> None:
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Port", "Port must be a valid integer between 1024 and 65535.")
            return

        host = "0.0.0.0" if self.lan_var.get() else "127.0.0.1"
        available, err = is_port_available(port, host=host)
        if available:
            self._append_log(f"[INFO] Port {port} is available on host {host}.")
            messagebox.showinfo("Port Available", f"Port {port} is available for the Sync Service.")
        else:
            self._append_log(f"[WARNING] Port check failed: {err}")
            messagebox.showwarning("Port In Use", f"Port {port} conflict detected:\n\n{err}")

    def _sync_settings_from_ui(self) -> bool:
        """Read UI inputs into self.settings. Return True if valid, False otherwise."""
        path = self.path_var.get().strip()
        try:
            port = int(self.port_var.get().strip())
            if port < 1024 or port > 65535:
                raise ValueError("Port out of range")
        except ValueError:
            messagebox.showerror("Invalid Port", "Please enter a valid port between 1024 and 65535.")
            return False

        self.settings.foxpro_data_path = path
        self.settings.port = port
        self.settings.bind_lan = self.lan_var.get()
        return True

    def _on_save_settings(self) -> None:
        if not self._sync_settings_from_ui():
            return
        saved_to = save_settings(self.settings, self.settings_path)
        self.status_bar_var.set(f"Settings saved to {saved_to.name}.")
        self._append_log(f"[INFO] Saved configuration to {saved_to}")
        messagebox.showinfo("Settings Saved", f"Settings successfully saved to:\n{saved_to}")

    def _on_reset_defaults(self) -> None:
        if messagebox.askyesno(
            "Reset to Defaults",
            "Reset all settings to default values?\n\n• Data Path: D:\\FAVWIN\\D2627\n• Port: 8080\n• LAN: Enabled",
        ):
            self.settings = reset_to_defaults(self.settings_path)
            self.path_var.set(self.settings.foxpro_data_path)
            self.port_var.set(str(self.settings.port))
            self.lan_var.set(self.settings.bind_lan)
            self._update_tablet_url_display()
            self._append_log("[INFO] Settings reset to default values.")
            self.status_bar_var.set("Settings reset to defaults.")

    def _on_start_server(self) -> None:
        if not self._sync_settings_from_ui():
            return

        # Disable start button immediately to prevent duplicate triggers
        self.start_btn.config(state=tk.DISABLED)
        self.status_bar_var.set("Starting server worker thread...")
        self._append_log(f"[INFO] Starting server on port {self.settings.port} (Host: {self.settings.host})...")

        # Start in background thread so UI does not freeze during startup health polling
        def run_start():
            success, err = self.runner.start(self.settings)
            if not success:
                self.root.after(0, lambda: messagebox.showerror("Startup Error", f"Failed to start server:\n\n{err}"))

        t = threading.Thread(target=run_start, daemon=True)
        t.start()

    def _on_stop_server(self) -> None:
        self.stop_btn.config(state=tk.DISABLED)
        self.status_bar_var.set("Stopping server worker...")

        def run_stop():
            self.runner.stop()

        t = threading.Thread(target=run_stop, daemon=True)
        t.start()

    def _on_check_health(self) -> None:
        if self.runner.state != ServerState.RUNNING:
            messagebox.showinfo(
                "Server Not Running",
                "The server is currently stopped. Start the server first to check live API health.",
            )
            return

        healthy, data = self.runner.check_health()
        if healthy:
            status_text = data.get("status", "OK")
            tables = data.get("tables", {})
            tbl_lines = [f"• {k}: {'OK' if v.get('exists') else 'MISSING'} ({v.get('record_count', 0)} rows)" for k, v in tables.items()]
            msg = f"Status: {status_text}\nService: {data.get('service', 'PYROJA')}\nVersion: {data.get('version', '1.0.0')}\n\nTables:\n" + "\n".join(tbl_lines)
            messagebox.showinfo("Health Status: Healthy", msg)
        else:
            err = data.get("error", "Unknown error")
            messagebox.showwarning("Health Check Warning", f"Health check returned an error:\n\n{err}")

    def _on_server_state_change(self, state: ServerState, error_message: Optional[str]) -> None:
        """Invoked by ServerRunner when server transitions state (thread-safe dispatch)."""
        self.root.after(0, lambda: self._update_ui_for_state(state, error_message))

    def _update_ui_for_state(self, state: ServerState, error_message: Optional[str]) -> None:
        """Update buttons, badges, and status bar based on server state."""
        self.status_badge_var.set(state.value)

        # Update badge styling
        if state == ServerState.RUNNING:
            self.status_badge.config(bg="#2e7d32", fg="white")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.path_entry.config(state="disabled")
            self.browse_btn.config(state="disabled")
            self.port_entry.config(state="disabled")
            self.status_bar_var.set(f"Server is RUNNING on {self.settings.host}:{self.settings.port}. Tablets may connect.")
        elif state == ServerState.STARTING:
            self.status_badge.config(bg="#f57c00", fg="white")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_bar_var.set("Server is starting...")
        elif state == ServerState.STOPPING:
            self.status_badge.config(bg="#f57c00", fg="white")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_bar_var.set("Server is stopping...")
        elif state == ServerState.ERROR:
            self.status_badge.config(bg="#c62828", fg="white")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.path_entry.config(state="normal")
            self.browse_btn.config(state="normal")
            self.port_entry.config(state="normal")
            self.status_bar_var.set(f"Error: {error_message or 'Server failed to start'}")
        else:  # STOPPED
            self.status_badge.config(bg="#757575", fg="white")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.path_entry.config(state="normal")
            self.browse_btn.config(state="normal")
            self.port_entry.config(state="normal")
            self.status_bar_var.set("Server is stopped. Click 'Start Server' to resume.")

    def _update_ui_state(self) -> None:
        self._update_ui_for_state(self.runner.state, self.runner.error_message)

    def _poll_log_queue(self) -> None:
        """Drain background log messages into ScrolledText widget."""
        while True:
            try:
                msg = self.runner.log_queue.get_nowait()
                self._append_log(msg)
            except queue.Empty:
                break

        # Re-schedule poll
        self.root.after(self.log_poll_interval_ms, self._poll_log_queue)

    def _append_log(self, text: str) -> None:
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def _on_clear_logs(self) -> None:
        self.log_text.delete("1.0", tk.END)

    def _on_window_closing(self) -> None:
        """Handle window close event with safety prompt if server is running."""
        if self.runner.state in (ServerState.RUNNING, ServerState.STARTING):
            if messagebox.askyesno(
                "Confirm Exit",
                "The PYROJA Sync Service is currently running.\n\n"
                "Closing this window will stop the server and disconnect Android tablets.\n\n"
                "Do you want to stop the server and exit?",
            ):
                self.status_bar_var.set("Shutting down server before exit...")
                self.runner.stop()
                self.root.destroy()
        else:
            self.root.destroy()


def run_gui(settings_path: Optional[Path] = None) -> None:
    """Launch the Desktop Control Panel GUI."""
    if not TKINTER_AVAILABLE:
        print("Error: Tkinter is not available in this Python installation.")
        print("Please install Python with Tk support or run the server in headless mode (--headless).")
        return

    root = tk.Tk()
    app = ControlPanelApp(root, settings_path=settings_path)
    root.mainloop()
