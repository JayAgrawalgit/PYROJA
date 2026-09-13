"""Configuration loader and schema definition."""

from pathlib import Path
from typing import List, Optional
import os
import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    cors_origins: List[str] = ["*"]


class FoxproConfig(BaseModel):
    data_path: Path = Path("../legacy-software-extracted/FAVWIN/D2627")
    active_fiscal_year: str = "D2627"


class DatabaseConfig(BaseModel):
    path: Path = Path("sync_service.sqlite3")


class CacheConfig(BaseModel):
    ttl_seconds: int = 30
    validate_mtime: bool = True


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    file: Optional[str] = "logs/sync_service.log"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    foxpro: FoxproConfig = Field(default_factory=FoxproConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


import sys
import json

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load configuration from JSON or YAML file and apply environment variable overrides."""
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parent.parent

    if config_path:
        target_file = Path(config_path)
    else:
        env_config = os.getenv("PYROJA_CONFIG_PATH") or os.getenv("SYNC_CONFIG_PATH")
        if env_config:
            target_file = Path(env_config)
        else:
            if (base_dir / "config.json").exists():
                target_file = base_dir / "config.json"
            else:
                target_file = base_dir / "config.yaml"

    config_data = {}
    if target_file.exists():
        with open(target_file, "r", encoding="utf-8") as f:
            if target_file.suffix.lower() == ".json":
                config_data = json.load(f) or {}
            else:
                config_data = yaml.safe_load(f) or {}

    config = AppConfig(**config_data)

    # Environment variable overrides (PYROJA_* primary, SYNC_* backward-compatible fallback)
    server_host = os.getenv("PYROJA_SERVER_HOST") or os.getenv("SYNC_SERVER_HOST")
    if server_host:
        config.server.host = server_host

    server_port = os.getenv("PYROJA_SERVER_PORT") or os.getenv("SYNC_SERVER_PORT")
    if server_port:
        config.server.port = int(server_port)

    foxpro_path = os.getenv("PYROJA_FOXPRO_DATA_PATH") or os.getenv("SYNC_FOXPRO_DATA_PATH")
    if foxpro_path:
        config.foxpro.data_path = Path(foxpro_path)

    fiscal_year = os.getenv("PYROJA_FISCAL_YEAR") or os.getenv("SYNC_FISCAL_YEAR")
    if fiscal_year:
        config.foxpro.active_fiscal_year = fiscal_year

    db_path = os.getenv("PYROJA_DATABASE_PATH") or os.getenv("SYNC_DATABASE_PATH")
    if db_path:
        config.database.path = Path(db_path)

    log_level = os.getenv("PYROJA_LOG_LEVEL") or os.getenv("SYNC_LOG_LEVEL")
    if log_level:
        config.logging.level = log_level

    # Resolve relative paths against base_dir if needed
    if not config.foxpro.data_path.is_absolute():
        config.foxpro.data_path = (base_dir / config.foxpro.data_path).resolve()
    if not config.database.path.is_absolute():
        config.database.path = (base_dir / config.database.path).resolve()

    return config
