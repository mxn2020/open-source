"""Tests for config_drift_detector.parsers."""

from __future__ import annotations

import pytest

from config_drift_detector.parsers import parse_file

# -- YAML ------------------------------------------------------------------


def test_parse_yaml(tmp_path):
    f = tmp_path / "config.yaml"
    f.write_text("database:\n  host: localhost\n  port: 5432\n")
    result = parse_file(str(f))
    assert result == {"database": {"host": "localhost", "port": 5432}}


def test_parse_yml_extension(tmp_path):
    f = tmp_path / "config.yml"
    f.write_text("key: value\n")
    result = parse_file(str(f))
    assert result == {"key": "value"}


# -- JSON ------------------------------------------------------------------


def test_parse_json(tmp_path):
    f = tmp_path / "config.json"
    f.write_text('{"database": {"host": "localhost", "port": 5432}}')
    result = parse_file(str(f))
    assert result == {"database": {"host": "localhost", "port": 5432}}


# -- TOML ------------------------------------------------------------------


def test_parse_toml(tmp_path):
    f = tmp_path / "config.toml"
    f.write_text('[database]\nhost = "localhost"\nport = 5432\n')
    result = parse_file(str(f))
    assert result == {"database": {"host": "localhost", "port": 5432}}


# -- Edge cases -------------------------------------------------------------


def test_parse_empty_yaml(tmp_path):
    f = tmp_path / "empty.yaml"
    f.write_text("")
    result = parse_file(str(f))
    assert result == {}


def test_parse_file_not_found():
    with pytest.raises(FileNotFoundError, match="not found"):
        parse_file("/nonexistent/path.yaml")


def test_parse_unsupported_extension(tmp_path):
    f = tmp_path / "config.ini"
    f.write_text("[section]\nkey=value\n")
    with pytest.raises(ValueError, match="Unsupported file format"):
        parse_file(str(f))
