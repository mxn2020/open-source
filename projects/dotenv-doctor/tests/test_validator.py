"""Tests for dotenv_doctor.validator."""

from dotenv_doctor.parser import EnvEntry
from dotenv_doctor.validator import Severity, validate_env


def _entry(key: str, value: str = "val", line: int = 1) -> EnvEntry:
    return EnvEntry(key=key, value=value, line_number=line, raw_line=f"{key}={value}")


class TestDuplicateKeys:
    def test_no_duplicates(self):
        entries = [_entry("A", line=1), _entry("B", line=2)]
        issues = validate_env(entries)
        dupes = [i for i in issues if "Duplicate" in i.message]
        assert dupes == []

    def test_duplicate_detected(self):
        entries = [_entry("A", line=1), _entry("A", line=3)]
        issues = validate_env(entries)
        dupes = [i for i in issues if "Duplicate" in i.message]
        assert len(dupes) == 1
        assert dupes[0].severity == Severity.WARNING
        assert dupes[0].line_number == 3


class TestEmptyValues:
    def test_no_empty(self):
        entries = [_entry("A", value="hello")]
        issues = validate_env(entries)
        empty = [i for i in issues if "Empty" in i.message]
        assert empty == []

    def test_empty_detected(self):
        entries = [_entry("A", value="")]
        issues = validate_env(entries)
        empty = [i for i in issues if "Empty" in i.message]
        assert len(empty) == 1
        assert empty[0].severity == Severity.WARNING


class TestInvalidKeyNames:
    def test_valid_key(self):
        entries = [_entry("DATABASE_URL")]
        issues = validate_env(entries)
        bad = [i for i in issues if "pattern" in i.message]
        assert bad == []

    def test_lowercase_key(self):
        entries = [_entry("my_key")]
        issues = validate_env(entries)
        bad = [i for i in issues if "pattern" in i.message]
        assert len(bad) == 1
        assert bad[0].severity == Severity.WARNING

    def test_starts_with_number(self):
        entries = [_entry("3PO")]
        issues = validate_env(entries)
        bad = [i for i in issues if "pattern" in i.message]
        assert len(bad) == 1

    def test_key_with_hyphen(self):
        entries = [_entry("MY-KEY")]
        issues = validate_env(entries)
        bad = [i for i in issues if "pattern" in i.message]
        assert len(bad) == 1


class TestTemplateComparison:
    def test_missing_key_from_template(self):
        entries = [_entry("A")]
        template = [_entry("A"), _entry("B")]
        issues = validate_env(entries, template)
        missing = [i for i in issues if "missing" in i.message]
        assert len(missing) == 1
        assert missing[0].severity == Severity.ERROR
        assert missing[0].key == "B"

    def test_extra_key_not_in_template(self):
        entries = [_entry("A"), _entry("EXTRA")]
        template = [_entry("A")]
        issues = validate_env(entries, template)
        extra = [i for i in issues if "not defined in the template" in i.message]
        assert len(extra) == 1
        assert extra[0].severity == Severity.INFO
        assert extra[0].key == "EXTRA"

    def test_no_template(self):
        entries = [_entry("A"), _entry("B")]
        issues = validate_env(entries)
        template_issues = [i for i in issues if "template" in i.message or "missing" in i.message]
        assert template_issues == []

    def test_perfect_match(self):
        entries = [_entry("A"), _entry("B")]
        template = [_entry("A"), _entry("B")]
        issues = validate_env(entries, template)
        template_issues = [i for i in issues if "template" in i.message or "missing" in i.message]
        assert template_issues == []
