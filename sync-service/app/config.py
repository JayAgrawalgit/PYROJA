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
    format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    file: Optional[str] = "sync_service.log"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    foxpro: FoxproConfig = Field(default_factory=FoxproConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load configuration from YAML file and apply environment variable overrides."""
    base_dir = Path(__file__).resolve().parent.parent
    if config_path:
        target_file = Path(config_path)
    else:
        env_config = os.getenv("SYNC_CONFIG_PATH")
        if env_config:
            target_file = Path(env_config)
        else:
            target_file = base_dir / "config.yaml"

    config_data = {}
    if target_file.exists():
        with open(target_file, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

    config = AppConfig(**config_data)

    # Environment variable overrides
    if os.getenv("SYNC_SERVER_HOST"):
        config.server.host = os.environ["SYNC_SERVER_HOST"]
    if os.getenv("SYNC_SERVER_PORT"):
        config.server.port = int(os.environ["SYNC_SERVER_PORT"])
    if os.getenv("SYNC_FOXPRO_DATA_PATH"):
        config.foxpro.data_path = Path(os.environ["SYNC_FOXPRO_DATA_PATH"])
    if os.getenv("SYNC_FISCAL_YEAR"):
        config.foxpro.active_fiscal_year = os.environ["SYNC_FISCAL_YEAR"]
    if os.getenv("SYNC_DATABASE_PATH"):
        config.database.path = Path(os.environ["SYNC_DATABASE_PATH"])
    if os.getenv("SYNC_LOG_LEVEL"):
        config.logging.level = os.environ["SYNC_LOG_LEVEL"]

    # Resolve relative paths against base_dir if needed
    if not config.foxpro.data_path.is_absolute():
        config.foxpro.data_path = (base_dir / config.foxpro.data_path).resolve()
    if not config.database.path.is_absolute():
        config.database.path = (base_dir / config.database.path).resolve()

    return config
