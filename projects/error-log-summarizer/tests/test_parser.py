"""Tests for the log parser module."""

from __future__ import annotations

import json
import textwrap

from error_log_summarizer.parser import parse_log_file, _parse_line


class TestGenericFormat:
    def test_parse_error(self):
        entry = _parse_line("2024-01-15 10:30:00 ERROR Something failed")
        assert entry is not None
        assert entry.timestamp == "2024-01-15 10:30:00"
        assert entry.level == "ERROR"
        assert entry.message == "Something failed"

    def test_parse_warning(self):
        entry = _parse_line("2024-01-15 10:30:00 WARNING Disk space low")
        assert entry is not None
        assert entry.level == "WARNING"

    def test_parse_info(self):
        entry = _parse_line("2024-01-15 10:30:00 INFO Server started")
        assert entry is not None
        assert entry.level == "INFO"
        assert entry.message == "Server started"

    def test_parse_critical(self):
        entry = _parse_line("2024-01-15 10:30:00 CRITICAL Database down")
        assert entry is not None
        assert entry.level == "CRITICAL"

    def test_case_insensitive_level(self):
        entry = _parse_line("2024-01-15 10:30:00 error lowercase error")
        assert entry is not None
        assert entry.level == "ERROR"

    def test_iso_timestamp_with_t(self):
        entry = _parse_line("2024-01-15T10:30:00 ERROR Something failed")
        assert entry is not None
        assert entry.timestamp == "2024-01-15T10:30:00"


class TestApacheFormat:
    def test_parse_error(self):
        entry = _parse_line("[Wed Jan 15 10:30:00 2024] [error] client denied by server")
        assert entry is not None
        assert entry.timestamp == "Wed Jan 15 10:30:00 2024"
        assert entry.level == "ERROR"
        assert entry.message == "client denied by server"

    def test_parse_warning(self):
        entry = _parse_line("[Wed Jan 15 10:30:00 2024] [warn] module already loaded")
        assert entry is not None
        assert entry.level == "WARNING"

    def test_parse_notice(self):
        entry = _parse_line("[Wed Jan 15 10:30:00 2024] [notice] server started")
        assert entry is not None
        assert entry.level == "INFO"


class TestSyslogFormat:
    def test_parse_basic(self):
        entry = _parse_line("Jan 15 10:30:00 myhost sshd[1234]: Connection refused from 1.2.3.4")
        assert entry is not None
        assert entry.timestamp == "Jan 15 10:30:00"
        assert entry.source == "sshd"
        assert entry.level == "ERROR"
        assert "Connection refused" in entry.message

    def test_info_message(self):
        entry = _parse_line("Jan 15 10:30:00 myhost cron[500]: job started successfully")
        assert entry is not None
        assert entry.level == "INFO"

    def test_warning_message(self):
        entry = _parse_line("Jan 15 10:30:00 myhost app[99]: request timeout reached")
        assert entry is not None
        assert entry.level == "WARNING"


class TestJsonFormat:
    def test_parse_basic(self):
        line = json.dumps(
            {"timestamp": "2024-01-15T10:30:00", "level": "error", "message": "db down"}
        )
        entry = _parse_line(line)
        assert entry is not None
        assert entry.level == "ERROR"
        assert entry.message == "db down"

    def test_parse_with_source(self):
        line = json.dumps(
            {"timestamp": "2024-01-15", "level": "WARNING", "message": "slow", "source": "api"}
        )
        entry = _parse_line(line)
        assert entry is not None
        assert entry.source == "api"

    def test_invalid_json_skipped(self):
        entry = _parse_line("{not valid json")
        assert entry is None

    def test_json_missing_fields_skipped(self):
        entry = _parse_line(json.dumps({"foo": "bar"}))
        assert entry is None


class TestEdgeCases:
    def test_empty_line(self):
        assert _parse_line("") is None
        assert _parse_line("   ") is None

    def test_unparseable_line(self):
        assert _parse_line("just some random text without structure") is None


class TestParseLogFile:
    def test_generic_file(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text(textwrap.dedent("""\
            2024-01-15 10:30:00 ERROR Something failed
            2024-01-15 10:30:01 INFO Server running
            2024-01-15 10:30:02 WARNING Disk space low
        """))
        entries = parse_log_file(str(log))
        assert len(entries) == 3
        assert entries[0].level == "ERROR"
        assert entries[1].level == "INFO"
        assert entries[2].level == "WARNING"

    def test_mixed_formats(self, tmp_path):
        log = tmp_path / "mixed.log"
        log.write_text(textwrap.dedent("""\
            2024-01-15 10:30:00 ERROR generic error
            [Wed Jan 15 10:30:00 2024] [error] apache error
        """))
        entries = parse_log_file(str(log))
        assert len(entries) == 2

    def test_file_not_found(self):
        import pytest

        with pytest.raises(FileNotFoundError):
            parse_log_file("/nonexistent/path/to/file.log")

    def test_empty_file(self, tmp_path):
        log = tmp_path / "empty.log"
        log.write_text("")
        entries = parse_log_file(str(log))
        assert entries == []

    def test_skips_unparseable_lines(self, tmp_path):
        log = tmp_path / "messy.log"
        log.write_text(textwrap.dedent("""\
            random noise
            2024-01-15 10:30:00 ERROR real error
            more noise
        """))
        entries = parse_log_file(str(log))
        assert len(entries) == 1
        assert entries[0].level == "ERROR"
