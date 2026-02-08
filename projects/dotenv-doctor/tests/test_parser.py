"""Tests for dotenv_doctor.parser."""

import textwrap
from pathlib import Path

from dotenv_doctor.parser import EnvEntry, parse_file, parse_line


class TestParseLine:
    def test_simple_assignment(self):
        entry = parse_line("DATABASE_URL=postgres://localhost/db", 1)
        assert entry == EnvEntry(
            key="DATABASE_URL",
            value="postgres://localhost/db",
            line_number=1,
            raw_line="DATABASE_URL=postgres://localhost/db",
        )

    def test_empty_line(self):
        assert parse_line("", 1) is None

    def test_whitespace_only(self):
        assert parse_line("   ", 1) is None

    def test_comment(self):
        assert parse_line("# this is a comment", 1) is None

    def test_inline_comment(self):
        entry = parse_line("KEY=value # this is a comment", 1)
        assert entry is not None
        assert entry.value == "value"

    def test_double_quoted_value(self):
        entry = parse_line('KEY="hello world"', 1)
        assert entry is not None
        assert entry.value == "hello world"

    def test_single_quoted_value(self):
        entry = parse_line("KEY='hello world'", 1)
        assert entry is not None
        assert entry.value == "hello world"

    def test_quoted_value_with_inline_comment(self):
        entry = parse_line('KEY="hello world" # comment', 1)
        assert entry is not None
        assert entry.value == "hello world"

    def test_export_prefix(self):
        entry = parse_line("export MY_VAR=123", 1)
        assert entry is not None
        assert entry.key == "MY_VAR"
        assert entry.value == "123"

    def test_empty_value(self):
        entry = parse_line("KEY=", 1)
        assert entry is not None
        assert entry.key == "KEY"
        assert entry.value == ""

    def test_spaces_around_equals(self):
        entry = parse_line("KEY = value", 1)
        assert entry is not None
        assert entry.key == "KEY"
        assert entry.value == "value"

    def test_no_equals_sign(self):
        assert parse_line("JUST_A_KEY", 1) is None

    def test_value_with_equals_sign(self):
        entry = parse_line("KEY=a=b=c", 1)
        assert entry is not None
        assert entry.value == "a=b=c"


class TestParseFile:
    def test_parse_valid_file(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text(textwrap.dedent("""\
                # Database config
                DATABASE_URL=postgres://localhost/db
                SECRET_KEY="my-secret"

                # Feature flags
                export ENABLE_FEATURE=true
                EMPTY_KEY=
            """))

        entries = parse_file(env_file)
        assert len(entries) == 4
        assert entries[0].key == "DATABASE_URL"
        assert entries[1].key == "SECRET_KEY"
        assert entries[1].value == "my-secret"
        assert entries[2].key == "ENABLE_FEATURE"
        assert entries[3].key == "EMPTY_KEY"
        assert entries[3].value == ""

    def test_parse_empty_file(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("")
        assert parse_file(env_file) == []

    def test_parse_comments_only(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("# comment 1\n# comment 2\n")
        assert parse_file(env_file) == []
