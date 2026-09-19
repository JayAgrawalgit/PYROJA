"""Server lifecycle manager for running PYROJA FastAPI / Uvicorn service in a managed background thread."""

import asyncio
from enum import Enum
import json
import logging
import queue
import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple
import urllib.error
import urllib.request

import uvicorn

from app.desktop.settings import ControlPanelSettings, to_app_config
from app.desktop.validator import is_port_available, validate_foxpro_folder
from app.main import create_app

logger = logging.getLogger("PYROJA.ServerRunner")


class ServerState(str, Enum):
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    ERROR = "ERROR"


class QueueLogHandler(logging.Handler):
    """Logging handler that routes records into a thread-safe Queue for UI consumption."""

    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.log_queue.put(msg)
        except Exception:
            self.handleError(record)


class ServerRunner:
    """Manages the FastAPI / Uvicorn server lifecycle with state tracking and log forwarding."""

    def __init__(
        self,
        on_state_change: Optional[Callable[[ServerState, Optional[str]], None]] = None,
    ):
        self.state: ServerState = ServerState.STOPPED
        self.error_message: Optional[str] = None
        self.on_state_change = on_state_change

        self.log_queue: queue.Queue = queue.Queue()
        self._log_handler = QueueLogHandler(self.log_queue)

        self._server: Optional[uvicorn.Server] = None
        self._app: Optional[Any] = None
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._lock = threading.Lock()
        self._active_port: int = 8080
        self._active_host: str = "0.0.0.0"

        self._setup_logging_interception()

    def _setup_logging_interception(self) -> None:
        """Attach queue log handler to root and project loggers."""
        for name in ("PYROJA", "uvicorn", "uvicorn.error", "uvicorn.access", "app"):
            l = logging.getLogger(name)
            if self._log_handler not in l.handlers:
                l.addHandler(self._log_handler)

    def _set_state(self, state: ServerState, error_message: Optional[str] = None) -> None:
        """Update internal state and notify callback."""
        self.state = state
        self.error_message = error_message
        if error_message:
            self.log_queue.put(f"[ERROR] {error_message}")
        if self.on_state_change:
            try:
                self.on_state_change(state, error_message)
            except Exception as exc:
                logger.error(f"Error in on_state_change callback: {exc}")

    def start(self, settings: ControlPanelSettings, timeout: float = 6.0) -> Tuple[bool, Optional[str]]:
        """Start the server in a background thread.

        Validates folder and port before starting.
        Prevents duplicate start calls.
        """
        with self._lock:
            if self.state in (ServerState.STARTING, ServerState.RUNNING):
                return False, "Server is already running or starting."

            # 1. Validate FoxPro folder strictly read-only
            folder_val = validate_foxpro_folder(settings.foxpro_data_path)
            if not folder_val.valid:
                err = folder_val.error_message or "FoxPro folder validation failed."
                self._set_state(ServerState.ERROR, err)
                return False, err

            # 2. Validate port availability
            port_avail, port_err = is_port_available(settings.port, host=settings.host)
            if not port_avail:
                err = port_err or f"Port {settings.port} is not available."
                self._set_state(ServerState.ERROR, err)
                return False, err

            self._set_state(ServerState.STARTING)
            self._active_port = settings.port
            self._active_host = settings.host

            try:
                # Prepare configuration and FastAPI app
                app_config = to_app_config(settings)
                self._app = create_app(app_config)

                uvicorn_config = uvicorn.Config(
                    app=self._app,
                    host=settings.host,
                    port=settings.port,
                    log_level=settings.log_level.lower(),
                    loop="asyncio",
                )
                self._server = uvicorn.Server(uvicorn_config)

                # Launch in daemon thread
                self._thread = threading.Thread(
                    target=self._run_server_thread,
                    name="PYROJA-Server-Worker",
                    daemon=True,
                )
                self._thread.start()
            except Exception as exc:
                err = f"Failed to initialize server: {exc}"
                self._set_state(ServerState.ERROR, err)
                return False, err

        # 3. Poll for readiness outside lock
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self._thread or not self._thread.is_alive():
                err = "Server worker thread terminated unexpectedly during startup."
                self._set_state(ServerState.ERROR, err)
                return False, err

            if self._server and getattr(self._server, "started", False):
                self._set_state(ServerState.RUNNING)
                self.log_queue.put(f"[INFO] Server successfully started on {settings.host}:{settings.port}")
                return True, None

            time.sleep(0.05)

        # Timeout reached
        if self._thread and self._thread.is_alive():
            self._set_state(ServerState.RUNNING)
            self.log_queue.put(f"[INFO] Server started on {settings.host}:{settings.port}")
            return True, None
        else:
            err = f"Server failed to become healthy within {timeout}s."
            self._set_state(ServerState.ERROR, err)
            return False, err

    def _run_server_thread(self) -> None:
        """Worker thread entrypoint."""
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            if self._server:
                self._loop.run_until_complete(self._server.serve())
        except Exception as exc:
            logger.error(f"Unhandled exception in server worker thread: {exc}", exc_info=True)
            self._set_state(ServerState.ERROR, str(exc))
        finally:
            if self._loop and self._loop.is_running():
                self._loop.close()
            with self._lock:
                if self.state != ServerState.ERROR:
                    self._set_state(ServerState.STOPPED)

    def stop(self, timeout: float = 5.0) -> bool:
        """Stop the running server cleanly and wait for worker thread to exit."""
        with self._lock:
            if self.state in (ServerState.STOPPED, ServerState.ERROR):
                return True

            self._set_state(ServerState.STOPPING)
            self.log_queue.put("[INFO] Stopping server gracefully...")

            if self._server:
                self._server.should_exit = True

        # Wait for thread termination outside the lock
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)

        with self._lock:
            self._set_state(ServerState.STOPPED)
            self.log_queue.put("[INFO] Server stopped.")
            self._server = None
            self._thread = None
            return True

    def check_health(self, timeout: float = 3.0) -> Tuple[bool, Dict[str, Any]]:
        """Query health status of the active FastAPI service."""
        if self.state != ServerState.RUNNING:
            return False, {"error": "Server is not running"}

        # First query active master_service in-memory if available
        if self._app and hasattr(self._app.state, "master_service") and self._app.state.master_service:
            try:
                h = self._app.state.master_service.check_health()
                data = h.model_dump() if hasattr(h, "model_dump") else h.dict()
                data["service"] = "PYROJA"
                is_healthy = data.get("status") in ("HEALTHY", "WARNING", "DEGRADED")
                return is_healthy, data
            except Exception as exc:
                logger.debug(f"Direct master_service check failed: {exc}")

        # Fallback to HTTP query
        poll_host = "127.0.0.1" if self._active_host in ("0.0.0.0", "127.0.0.1") else self._active_host
        url = f"http://{poll_host}:{self._active_port}/api/health"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PYROJA-ControlPanel"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return resp.status == 200, data
        except urllib.error.HTTPError as he:
            try:
                data = json.loads(he.read().decode("utf-8"))
                return False, data
            except Exception:
                return False, {"error": f"HTTP {he.code}: {he.reason}"}
        except Exception as exc:
            return False, {"error": str(exc)}
