"""Unit tests for the DBFReader class."""

from pathlib import Path
import pytest

from app.dbf.reader import DBFReader, DBFFileNotFoundError, DBFCorruptedError
from tests.conftest import create_synthetic_dbf


def test_dbf_file_not_found():
    reader = DBFReader("/nonexistent/path/table.dbf")
    assert not reader.exists()
    with pytest.raises(DBFFileNotFoundError):
        _ = reader.header
    with pytest.raises(DBFFileNotFoundError):
        reader.compute_checksum()
    with pytest.raises(DBFFileNotFoundError):
        reader.get_mtime()


def test_dbf_corrupted_short_header(temp_dbf_dir):
    short_file = temp_dbf_dir / "short.dbf"
    short_file.write_bytes(b"\x30\x01\x02")  # Less than 32 bytes
    reader = DBFReader(short_file)
    with pytest.raises(DBFCorruptedError):
        _ = reader.header


def test_synthetic_dbf_reading(temp_dbf_dir):
    table_file = temp_dbf_dir / "TEST.DBF"
    fields = [
        ("CODE", "C", 5, 0),
        ("NAME", "C", 20, 0),
        ("QTY", "N", 6, 0),
        ("RATE", "N", 8, 2),
    ]
    records = [
        {"CODE": "00001", "NAME": "SPARKLER GOLD", "QTY": 50, "RATE": 35.50},
        {"CODE": "00002", "NAME": "ROCKET BOOM", "QTY": 100, "RATE": 120.00},
        {"CODE": "00003", "NAME": "DELETED ITEM", "QTY": 0, "RATE": 0.00},
    ]
    # Mark record 2 (index 2) as deleted
    create_synthetic_dbf(table_file, fields, records, deleted_indices=[2])

    reader = DBFReader(table_file)
    assert reader.exists()
    header = reader.header
    assert header.num_records == 3
    assert len(header.fields) == 4
    assert [f.name for f in header.fields] == ["CODE", "NAME", "QTY", "RATE"]

    active_records = reader.read_all_records()
    # Deleted record should be filtered out
    assert len(active_records) == 2
    assert active_records[0]["CODE"] == "00001"
    assert active_records[0]["NAME"] == "SPARKLER GOLD"
    assert active_records[0]["QTY"] == 50
    assert active_records[0]["RATE"] == 35.50

    assert active_records[1]["CODE"] == "00002"
    assert active_records[1]["RATE"] == 120.00

    checksum = reader.compute_checksum()
    assert len(checksum) == 64  # Valid SHA-256


def test_real_dbf_tables_parsing(real_data_config):
    data_dir = real_data_config.foxpro.data_path
    item_table = data_dir / "ITEMMST.DBF"
    if not item_table.exists():
        pytest.skip(f"Real data directory {data_dir} not available")

    reader = DBFReader(item_table)
    header = reader.header
    assert header.version == 0x30
    assert header.num_records > 3000
    assert any(f.name == "CODE" for f in header.fields)
    assert any(f.name == "NAME" for f in header.fields)
    assert any(f.name == "SRATE" for f in header.fields)

    # Read first 10 items using generator
    recs = []
    for r in reader.iter_records():
        recs.append(r)
        if len(recs) >= 10:
            break

    assert len(recs) == 10
    assert recs[0]["CODE"] == "00013"
    assert "ROLL CAPS" in recs[0]["NAME"]
    assert recs[0]["SRATE"] == 48.0
