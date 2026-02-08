"""Tests for config_drift_detector.cli."""

from __future__ import annotations

from typer.testing import CliRunner

from config_drift_detector.cli import app

runner = CliRunner()


# -- Helpers ----------------------------------------------------------------


def _write_yaml(tmp_path, name: str, content: str) -> str:
    f = tmp_path / name
    f.write_text(content)
    return str(f)


# -- Version ----------------------------------------------------------------


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


# -- No drift ---------------------------------------------------------------


def test_check_no_drift(tmp_path):
    a = _write_yaml(tmp_path, "a.yaml", "key: value\n")
    b = _write_yaml(tmp_path, "b.yaml", "key: value\n")
    result = runner.invoke(app, ["check", "--a", a, "--b", b])
    assert result.exit_code == 0
    assert "No configuration drift" in result.output


# -- Drift detected ---------------------------------------------------------


def test_check_drift_detected(tmp_path):
    a = _write_yaml(tmp_path, "a.yaml", "key: old\n")
    b = _write_yaml(tmp_path, "b.yaml", "key: new\n")
    result = runner.invoke(app, ["check", "--a", a, "--b", b])
    assert result.exit_code == 1
    assert "key" in result.output


# -- JSON output ------------------------------------------------------------


def test_check_json_output(tmp_path):
    a = _write_yaml(tmp_path, "a.yaml", "x: 1\n")
    b = _write_yaml(tmp_path, "b.yaml", "x: 2\n")
    result = runner.invoke(app, ["check", "--a", a, "--b", b, "--json"])
    assert result.exit_code == 1
    assert '"path": "x"' in result.output
    assert '"type": "changed"' in result.output


def test_check_json_no_drift(tmp_path):
    a = _write_yaml(tmp_path, "a.yaml", "x: 1\n")
    b = _write_yaml(tmp_path, "b.yaml", "x: 1\n")
    result = runner.invoke(app, ["check", "--a", a, "--b", b, "--json"])
    assert result.exit_code == 0
    assert "[]" in result.output


# -- Tag filtering ----------------------------------------------------------


def test_check_with_tags(tmp_path):
    content_a = "db:\n  host: localhost\ncache:\n  ttl: 60\n"
    content_b = "db:\n  host: remotehost\ncache:\n  ttl: 120\n"
    a = _write_yaml(tmp_path, "a.yaml", content_a)
    b = _write_yaml(tmp_path, "b.yaml", content_b)
    result = runner.invoke(app, ["check", "--a", a, "--b", b, "--tags", "db", "--json"])
    assert result.exit_code == 1
    assert "db.host" in result.output
    assert "cache.ttl" not in result.output


# -- Error handling ---------------------------------------------------------


def test_check_file_not_found(tmp_path):
    a = _write_yaml(tmp_path, "a.yaml", "key: value\n")
    result = runner.invoke(app, ["check", "--a", a, "--b", "/nonexistent.yaml"])
    assert result.exit_code == 2
    assert "Error" in result.output
