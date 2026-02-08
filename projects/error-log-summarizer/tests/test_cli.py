"""Tests for the CLI interface."""

from __future__ import annotations

import json
import textwrap

from typer.testing import CliRunner

from error_log_summarizer.cli import app

runner = CliRunner()

SAMPLE_LOG = textwrap.dedent("""\
    2024-01-15 10:30:00 ERROR Connection refused to database
    2024-01-15 10:30:01 WARNING Disk usage at 85%
    2024-01-15 10:30:02 INFO Health check passed
    2024-01-15 10:30:03 ERROR File not found: /etc/app/config.yml
    2024-01-15 10:30:04 ERROR Connection refused to database
""")

CLEAN_LOG = textwrap.dedent("""\
    2024-01-15 10:30:00 INFO Server started
    2024-01-15 10:30:01 INFO Request handled
""")


class TestSummarizeCommand:
    def test_basic(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(SAMPLE_LOG)
        result = runner.invoke(app, ["summarize", str(log)])
        assert result.exit_code == 1  # errors found
        assert "Total entries" in result.output or "total_entries" in result.output

    def test_json_output(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(SAMPLE_LOG)
        result = runner.invoke(app, ["summarize", str(log), "--json"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert data["total_entries"] == 5
        assert data["error_count"] == 3

    def test_top_flag(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(SAMPLE_LOG)
        result = runner.invoke(app, ["summarize", str(log), "--json", "--top", "1"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert len(data["top_errors"]) == 1

    def test_clean_log_exit_zero(self, tmp_path):
        log = tmp_path / "clean.log"
        log.write_text(CLEAN_LOG)
        result = runner.invoke(app, ["summarize", str(log)])
        assert result.exit_code == 0

    def test_file_not_found(self):
        result = runner.invoke(app, ["summarize", "/nonexistent/file.log"])
        assert result.exit_code == 2
        assert "not found" in result.output.lower()

    def test_empty_file(self, tmp_path):
        log = tmp_path / "empty.log"
        log.write_text("")
        result = runner.invoke(app, ["summarize", str(log)])
        assert result.exit_code == 0


class TestCategorizeCommand:
    def test_basic(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(SAMPLE_LOG)
        result = runner.invoke(app, ["categorize", str(log)])
        assert result.exit_code == 1  # errors found

    def test_json_output(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(SAMPLE_LOG)
        result = runner.invoke(app, ["categorize", str(log), "--json"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert "ConnectionError" in data
        assert "FileNotFound" in data

    def test_clean_log(self, tmp_path):
        log = tmp_path / "clean.log"
        log.write_text(CLEAN_LOG)
        result = runner.invoke(app, ["categorize", str(log)])
        assert result.exit_code == 0

    def test_file_not_found(self):
        result = runner.invoke(app, ["categorize", "/nonexistent/file.log"])
        assert result.exit_code == 2
