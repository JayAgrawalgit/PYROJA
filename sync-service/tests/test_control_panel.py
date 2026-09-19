"""Unit tests for PYROJA Desktop Control Panel components:
Settings, Read-Only Validation, Port Detection, and Server Runner Lifecycle.
"""

import json
from pathlib import Path
import socket
import time
import pytest

from app.desktop.launcher import acquire_instance_lock
from app.desktop.server_runner import ServerRunner, ServerState
from app.desktop.settings import (
    DEFAULT_FOXPRO_PATH,
    DEFAULT_PORT,
    ControlPanelSettings,
    load_settings,
    reset_to_defaults,
    save_settings,
    to_app_config,
)
from app.desktop.validator import (
    get_all_lan_ips,
    get_primary_lan_ip,
    get_tablet_url,
    inspect_dbf_header_readonly,
    is_port_available,
    validate_foxpro_folder,
)
from tests.conftest import create_synthetic_dbf


# ==============================================================================
# Settings Tests
# ==============================================================================

def test_default_settings():
    """Verify standard default configuration values."""
    settings = ControlPanelSettings()
    assert settings.foxpro_data_path == DEFAULT_FOXPRO_PATH
    assert settings.port == DEFAULT_PORT
    assert settings.bind_lan is True
    assert settings.host == "0.0.0.0"
    assert settings.fiscal_year == "D2627"
    assert settings.log_level == "INFO"


def test_settings_save_and_load(tmp_path):
    """Verify settings save to disk and reload accurately."""
    custom_path = tmp_path / "custom_settings.json"
    settings = ControlPanelSettings(
        foxpro_data_path=r"C:\FAVWIN\D2627",
        port=8090,
        bind_lan=False,
        fiscal_year="D2526",
        log_level="DEBUG",
    )
    saved_file = save_settings(settings, settings_path=custom_path)
    assert saved_file == custom_path
    assert custom_path.exists()

    loaded = load_settings(settings_path=custom_path)
    assert loaded.foxpro_data_path == r"C:\FAVWIN\D2627"
    assert loaded.port == 8090
    assert loaded.bind_lan is False
    assert loaded.host == "127.0.0.1"
    assert loaded.fiscal_year == "D2526"
    assert loaded.log_level == "DEBUG"


def test_settings_corrupt_fallback(tmp_path):
    """Verify graceful fallback to defaults when settings file is corrupt JSON."""
    corrupt_file = tmp_path / "corrupt_settings.json"
    corrupt_file.write_text("{invalid json structure: true,", encoding="utf-8")

    loaded = load_settings(settings_path=corrupt_file)
    assert loaded.foxpro_data_path == DEFAULT_FOXPRO_PATH
    assert loaded.port == DEFAULT_PORT
    assert loaded.bind_lan is True


def test_settings_reset_to_defaults(tmp_path):
    """Verify reset_to_defaults reverts and persists default configuration."""
    target_file = tmp_path / "settings_to_reset.json"
    custom_settings = ControlPanelSettings(port=9999, bind_lan=False)
    save_settings(custom_settings, settings_path=target_file)

    reverted = reset_to_defaults(settings_path=target_file)
    assert reverted.port == DEFAULT_PORT
    assert reverted.bind_lan is True

    # Check persisted file
    reloaded = load_settings(settings_path=target_file)
    assert reloaded.port == DEFAULT_PORT


def test_settings_to_app_config(tmp_path):
    """Verify conversion of ControlPanelSettings to FastAPI AppConfig."""
    settings = ControlPanelSettings(
        foxpro_data_path=str(tmp_path / "favwin"),
        port=8085,
        bind_lan=True,
    )
    app_cfg = to_app_config(settings, base_dir=tmp_path)
    assert app_cfg.server.port == 8085
    assert app_cfg.server.host == "0.0.0.0"
    assert str(app_cfg.foxpro.data_path) == str(tmp_path / "favwin")

    # When bind_lan is False, host should be 127.0.0.1
    settings.bind_lan = False
    app_cfg2 = to_app_config(settings, base_dir=tmp_path)
    assert app_cfg2.server.host == "127.0.0.1"


# ==============================================================================
# Folder & DBF Read-Only Validation Tests
# ==============================================================================

def test_folder_validation_empty_and_nonexistent():
    """Verify empty or non-existent folder paths fail with clear error."""
    res_empty = validate_foxpro_folder("")
    assert not res_empty.valid
    assert "empty" in res_empty.error_message.lower()

    res_missing = validate_foxpro_folder("/non/existent/path/for/pyroja_test_12345")
    assert not res_missing.valid
    assert "does not exist" in res_missing.error_message.lower()


def test_folder_validation_missing_required_dbfs(temp_dbf_dir):
    """Verify folder validation reports missing required DBFs."""
    # Create only ITEMMST.DBF
    create_synthetic_dbf(
        temp_dbf_dir / "ITEMMST.DBF",
        fields=[("CODE", "C", 5, 0), ("NAME", "C", 20, 0)],
        records=[{"CODE": "00001", "NAME": "SPARKLER"}],
    )

    res = validate_foxpro_folder(str(temp_dbf_dir))
    assert not res.valid
    assert "NAMEMST.DBF" in res.missing_required
    assert "SALETRN.DBF" in res.missing_required
    assert res.tables["ITEMMST.DBF"].exists is True


def test_folder_validation_success_synthetic_dbfs(temp_dbf_dir):
    """Verify folder validation succeeds when all required DBFs exist."""
    # Create required DBFs
    for table_name in ["ITEMMST.DBF", "NAMEMST.DBF", "SALETRN.DBF"]:
        create_synthetic_dbf(
            temp_dbf_dir / table_name,
            fields=[("CODE", "C", 5, 0), ("NAME", "C", 20, 0)],
            records=[{"CODE": "00001", "NAME": "TEST"}],
        )

    res = validate_foxpro_folder(str(temp_dbf_dir))
    assert res.valid
    assert len(res.missing_required) == 0
    assert res.tables["ITEMMST.DBF"].record_count == 1
    assert res.tables["NAMEMST.DBF"].record_count == 1
    assert res.tables["SALETRN.DBF"].record_count == 1


def test_folder_validation_strictly_read_only(temp_dbf_dir):
    """Verify that validating a folder makes ZERO modifications or disk writes."""
    test_file = temp_dbf_dir / "ITEMMST.DBF"
    create_synthetic_dbf(
        test_file,
        fields=[("CODE", "C", 5, 0)],
        records=[{"CODE": "00001"}],
    )
    initial_mtime = test_file.stat().st_mtime_ns
    initial_files = set(temp_dbf_dir.iterdir())

    # Run validation multiple times
    _ = validate_foxpro_folder(str(temp_dbf_dir))
    _ = inspect_dbf_header_readonly(test_file)

    post_mtime = test_file.stat().st_mtime_ns
    post_files = set(temp_dbf_dir.iterdir())

    assert initial_mtime == post_mtime, "Validation modified DBF file timestamp!"
    assert initial_files == post_files, "Validation created or removed files in target directory!"


def test_folder_validation_case_insensitivity(temp_dbf_dir):
    """Verify case-insensitive matching for lowercase filenames on non-Windows/shares."""
    for table_name in ["itemmst.dbf", "namemst.dbf", "saletrn.dbf"]:
        create_synthetic_dbf(
            temp_dbf_dir / table_name,
            fields=[("CODE", "C", 5, 0)],
            records=[{"CODE": "00001"}],
        )

    res = validate_foxpro_folder(str(temp_dbf_dir))
    assert res.valid
    assert len(res.missing_required) == 0


def test_folder_validation_real_extracted_data():
    """Verify folder validation on the committed legacy FoxPro extracted data."""
    base_dir = Path(__file__).resolve().parent.parent
    real_path = (base_dir / "../legacy-software-extracted/FAVWIN/D2627").resolve()
    if real_path.exists():
        res = validate_foxpro_folder(str(real_path))
        assert res.valid
        assert res.tables["ITEMMST.DBF"].record_count > 1000
        assert res.tables["NAMEMST.DBF"].record_count > 500
        assert res.tables["SALETRN.DBF"].record_count > 1000


# ==============================================================================
# Port & Network Tests
# ==============================================================================

def find_free_port() -> int:
    """Helper to find an unused dynamic port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def test_port_availability_and_conflict():
    """Verify free port detection and occupied port conflict reporting."""
    free_port = find_free_port()
    avail, err = is_port_available(free_port)
    assert avail is True
    assert err is None

    # Bind socket to simulate port conflict
    occupied_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    occupied_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    occupied_sock.bind(("", free_port))
    occupied_sock.listen(1)

    try:
        in_use_avail, in_use_err = is_port_available(free_port)
        assert in_use_avail is False
        assert f"Port {free_port} is already in use" in in_use_err
    finally:
        occupied_sock.close()

    # Once closed, port should be available again
    re_avail, re_err = is_port_available(free_port)
    assert re_avail is True


def test_lan_ip_and_tablet_url():
    """Verify LAN IP discovery and tablet connection URL formatting."""
    primary_ip = get_primary_lan_ip()
    assert isinstance(primary_ip, str)
    assert len(primary_ip.split(".")) == 4

    all_ips = get_all_lan_ips()
    assert isinstance(all_ips, list)
    assert len(all_ips) >= 1

    tablet_url = get_tablet_url("192.168.1.100", 8080)
    assert tablet_url == "http://192.168.1.100:8080"


# ==============================================================================
# Server Runner Lifecycle Tests
# ==============================================================================

def test_server_runner_invalid_config_state_transition():
    """Verify server runner transitions to ERROR state if directory does not exist."""
    state_history = []

    def on_state(state, err):
        state_history.append((state, err))

    runner = ServerRunner(on_state_change=on_state)
    assert runner.state == ServerState.STOPPED

    invalid_settings = ControlPanelSettings(
        foxpro_data_path="/nonexistent/directory/test_12345",
        port=find_free_port(),
    )

    success, err = runner.start(invalid_settings)
    assert success is False
    assert runner.state == ServerState.ERROR
    assert "does not exist" in (err or "").lower()


def test_server_runner_duplicate_start_prevention(temp_dbf_dir, tmp_path):
    """Verify that calling start() while starting or running is rejected."""
    for table_name in ["ITEMMST.DBF", "NAMEMST.DBF", "SALETRN.DBF"]:
        create_synthetic_dbf(
            temp_dbf_dir / table_name,
            fields=[("CODE", "C", 5, 0)],
            records=[{"CODE": "00001"}],
        )

    free_port = find_free_port()
    settings = ControlPanelSettings(
        foxpro_data_path=str(temp_dbf_dir),
        port=free_port,
        bind_lan=False,
        sqlite_db_path=str(tmp_path / "state.sqlite3"),
    )

    runner = ServerRunner()
    success, _ = runner.start(settings, timeout=6.0)
    assert success is True
    assert runner.state == ServerState.RUNNING

    try:
        # Duplicate start attempt
        dup_success, dup_err = runner.start(settings)
        assert dup_success is False
        assert "already running" in (dup_err or "").lower()
    finally:
        runner.stop()
        assert runner.state == ServerState.STOPPED


def test_server_runner_full_lifecycle(temp_dbf_dir, tmp_path):
    """Verify full start -> health check -> graceful stop lifecycle."""
    for table_name in ["ITEMMST.DBF", "NAMEMST.DBF", "SALETRN.DBF"]:
        create_synthetic_dbf(
            temp_dbf_dir / table_name,
            fields=[("CODE", "C", 5, 0)],
            records=[{"CODE": "00001"}],
        )

    free_port = find_free_port()
    settings = ControlPanelSettings(
        foxpro_data_path=str(temp_dbf_dir),
        port=free_port,
        bind_lan=False,
        sqlite_db_path=str(tmp_path / "lifecycle_state.sqlite3"),
    )

    runner = ServerRunner()
    started, err = runner.start(settings, timeout=6.0)
    assert started is True, f"Failed to start server: {err}"
    assert runner.state == ServerState.RUNNING

    try:
        # Health check
        healthy, health_data = runner.check_health(timeout=3.0)
        assert healthy is True
        assert health_data.get("service") == "PYROJA"
        assert health_data.get("status") in ("HEALTHY", "WARNING", "DEGRADED")
    finally:
        stopped = runner.stop(timeout=5.0)
        assert stopped is True
        assert runner.state == ServerState.STOPPED


def test_instance_lock():
    """Verify single instance lock mechanism prevents multiple instances."""
    lock_port = find_free_port()
    sock1 = acquire_instance_lock(port=lock_port)
    assert sock1 is not None

    # Second acquisition on same port should fail
    sock2 = acquire_instance_lock(port=lock_port)
    assert sock2 is None

    # Once released, acquisition should succeed again
    sock1.close()
    sock3 = acquire_instance_lock(port=lock_port)
    assert sock3 is not None
    sock3.close()
