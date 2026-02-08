"""Tests for the categorizer module."""

from __future__ import annotations

from error_log_summarizer.categorizer import categorize_errors, summarize
from error_log_summarizer.parser import LogEntry


def _entry(level: str = "ERROR", message: str = "something failed") -> LogEntry:
    return LogEntry(timestamp="2024-01-15 10:30:00", level=level, message=message)


class TestCategorizeErrors:
    def test_connection_error(self):
        entries = [_entry(message="Connection refused to host db.local")]
        cats = categorize_errors(entries)
        assert "ConnectionError" in cats
        assert len(cats["ConnectionError"]) == 1

    def test_timeout_error(self):
        entries = [_entry(message="Request timed out after 30s")]
        cats = categorize_errors(entries)
        assert "TimeoutError" in cats

    def test_file_not_found(self):
        entries = [_entry(message="File not found: /etc/config.yml")]
        cats = categorize_errors(entries)
        assert "FileNotFound" in cats

    def test_permission_error(self):
        entries = [_entry(message="Permission denied for /var/log/secure")]
        cats = categorize_errors(entries)
        assert "PermissionError" in cats

    def test_memory_error(self):
        entries = [_entry(message="Out of memory: killed process 1234")]
        cats = categorize_errors(entries)
        assert "MemoryError" in cats

    def test_syntax_error(self):
        entries = [_entry(message="Syntax error in config at line 42")]
        cats = categorize_errors(entries)
        assert "SyntaxError" in cats

    def test_generic_fallback(self):
        entries = [_entry(message="Unknown failure occurred")]
        cats = categorize_errors(entries)
        assert "Generic" in cats

    def test_only_errors_categorized(self):
        entries = [
            _entry(level="INFO", message="Connection established"),
            _entry(level="WARNING", message="Connection slow"),
            _entry(level="ERROR", message="Connection refused"),
        ]
        cats = categorize_errors(entries)
        total = sum(len(v) for v in cats.values())
        assert total == 1

    def test_empty_input(self):
        cats = categorize_errors([])
        assert cats == {}

    def test_multiple_categories(self):
        entries = [
            _entry(message="Connection refused"),
            _entry(message="File not found: foo.txt"),
            _entry(message="Permission denied"),
        ]
        cats = categorize_errors(entries)
        assert len(cats) == 3


class TestSummarize:
    def test_counts(self):
        entries = [
            _entry(level="ERROR", message="err1"),
            _entry(level="ERROR", message="err2"),
            _entry(level="WARNING", message="warn1"),
            _entry(level="INFO", message="info1"),
            _entry(level="INFO", message="info2"),
            _entry(level="INFO", message="info3"),
        ]
        s = summarize(entries)
        assert s.total_entries == 6
        assert s.error_count == 2
        assert s.warning_count == 1
        assert s.info_count == 3

    def test_top_errors(self):
        entries = [
            _entry(message="Connection refused"),
            _entry(message="Connection refused"),
            _entry(message="Connection refused"),
            _entry(message="File not found: foo"),
        ]
        s = summarize(entries, top=2)
        assert len(s.top_errors) == 2
        assert s.top_errors[0][1] == 3  # most frequent

    def test_top_errors_normalized(self):
        entries = [
            _entry(message="Timeout after 30s on host 10.0.0.1"),
            _entry(message="Timeout after 60s on host 10.0.0.2"),
        ]
        s = summarize(entries, top=5)
        # Both should normalize to the same pattern
        assert len(s.top_errors) == 1
        assert s.top_errors[0][1] == 2

    def test_empty_input(self):
        s = summarize([])
        assert s.total_entries == 0
        assert s.error_count == 0
        assert s.categories == {}
        assert s.top_errors == []

    def test_categories_populated(self):
        entries = [
            _entry(message="Connection refused"),
            _entry(message="Permission denied"),
        ]
        s = summarize(entries)
        assert "ConnectionError" in s.categories
        assert "PermissionError" in s.categories
