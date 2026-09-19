"""Configuration and persistent settings management for the PYROJA Desktop Control Panel."""

from dataclasses import asdict, dataclass, field
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict, Optional

from app.config import AppConfig, DatabaseConfig, FoxproConfig, LoggingConfig, ServerConfig

logger = logging.getLogger("PYROJA.ControlPanel")

DEFAULT_FOXPRO_PATH = r"D:\FAVWIN\D2627"
DEFAULT_PORT = 8080
DEFAULT_FISCAL_YEAR = "D2627"
DEFAULT_BIND_LAN = True
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_SQLITE_PATH = "sync_service.sqlite3"


@dataclass
class ControlPanelSettings:
    """Settings structure for PYROJA Desktop Control Panel."""
    foxpro_data_path: str = DEFAULT_FOXPRO_PATH
    port: int = DEFAULT_PORT
    bind_lan: bool = DEFAULT_BIND_LAN
    fiscal_year: str = DEFAULT_FISCAL_YEAR
    log_level: str = DEFAULT_LOG_LEVEL
    sqlite_db_path: str = DEFAULT_SQLITE_PATH
    auto_start: bool = False

    @property
    def host(self) -> str:
        """Returns the bind host IP address based on LAN toggle."""
        return "0.0.0.0" if self.bind_lan else "127.0.0.1"

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ControlPanelSettings":
        """Create settings instance from dictionary with validation and safe fallbacks."""
        if not isinstance(data, dict):
            return cls()

        foxpro_path = str(data.get("foxpro_data_path") or DEFAULT_FOXPRO_PATH)
        try:
            port = int(data.get("port", DEFAULT_PORT))
            if port < 1024 or port > 65535:
                port = DEFAULT_PORT
        except (ValueError, TypeError):
            port = DEFAULT_PORT

        bind_lan = bool(data.get("bind_lan", DEFAULT_BIND_LAN))
        fiscal_year = str(data.get("fiscal_year") or DEFAULT_FISCAL_YEAR)
        log_level = str(data.get("log_level") or DEFAULT_LOG_LEVEL).upper()
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            log_level = DEFAULT_LOG_LEVEL

        sqlite_path = str(data.get("sqlite_db_path") or DEFAULT_SQLITE_PATH)
        auto_start = bool(data.get("auto_start", False))

        return cls(
            foxpro_data_path=foxpro_path,
            port=port,
            bind_lan=bind_lan,
            fiscal_year=fiscal_year,
            log_level=log_level,
            sqlite_db_path=sqlite_path,
            auto_start=auto_start,
        )


def get_default_settings_path() -> Path:
    """Resolve the per-user configuration file path.

    On Windows: %APPDATA%/PYROJA/settings.json
    On non-Windows: ~/.pyroja/settings.json
    """
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "PYROJA" / "settings.json"

    # Portable mode check: if running frozen or next to script, check for portable_settings.json
    if getattr(sys, "frozen", False):
        portable_file = Path(sys.executable).resolve().parent / "portable_settings.json"
        if portable_file.exists():
            return portable_file

    home = Path.home()
    return home / ".pyroja" / "settings.json"


def load_settings(settings_path: Optional[Path] = None) -> ControlPanelSettings:
    """Load settings from JSON file.

    If file does not exist, returns default settings without writing to disk.
    If file contains malformed JSON, returns default settings and logs warning.
    """
    target = settings_path or get_default_settings_path()
    if not target.exists():
        logger.debug(f"Settings file not found at {target}; using default settings.")
        return ControlPanelSettings()

    try:
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ControlPanelSettings.from_dict(data)
    except Exception as exc:
        logger.warning(f"Failed to read settings from {target} ({exc}); falling back to defaults.")
        return ControlPanelSettings()


def save_settings(settings: ControlPanelSettings, settings_path: Optional[Path] = None) -> Path:
    """Save settings to JSON file in per-user or specified directory."""
    target = settings_path or get_default_settings_path()
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w", encoding="utf-8") as f:
        json.dump(settings.to_dict(), f, indent=2)

    logger.info(f"Saved control panel settings to {target}")
    return target


def reset_to_defaults(settings_path: Optional[Path] = None) -> ControlPanelSettings:
    """Reset configuration to default settings and persist to disk."""
    default_settings = ControlPanelSettings()
    save_settings(default_settings, settings_path=settings_path)
    return default_settings


def to_app_config(
    settings: ControlPanelSettings,
    base_dir: Optional[Path] = None,
) -> AppConfig:
    """Convert desktop ControlPanelSettings into FastAPI AppConfig."""
    server_cfg = ServerConfig(
        host=settings.host,
        port=settings.port,
        cors_origins=["*"],
    )

    foxpro_p = Path(settings.foxpro_data_path)
    if not foxpro_p.is_absolute() and base_dir:
        foxpro_p = (base_dir / foxpro_p).resolve()

    foxpro_cfg = FoxproConfig(
        data_path=foxpro_p,
        active_fiscal_year=settings.fiscal_year,
    )

    db_p = Path(settings.sqlite_db_path)
    if not db_p.is_absolute() and base_dir:
        db_p = (base_dir / db_p).resolve()

    database_cfg = DatabaseConfig(path=db_p)

    logging_cfg = LoggingConfig(
        level=settings.log_level,
        file="logs/sync_service.log",
    )

    return AppConfig(
        server=server_cfg,
        foxpro=foxpro_cfg,
        database=database_cfg,
        logging=logging_cfg,
    )
