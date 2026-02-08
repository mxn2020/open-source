"""Tests for the CLI module."""

import json
from pathlib import Path

from typer.testing import CliRunner

from pr_reviewer_bot.cli import app

runner = CliRunner()

SAMPLE_DIFF = """\
diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,3 +1,5 @@
 import os
+# TODO: remove this
+print("debug")
 
 def main():
"""

CLEAN_DIFF = """\
diff --git a/clean.py b/clean.py
--- a/clean.py
+++ b/clean.py
@@ -1,2 +1,3 @@
 import os
+import sys
 
"""

SECRET_DIFF = """\
diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -1,2 +1,3 @@
 import os
+API_KEY = "sk-abc123secretkey99"
 
"""


class TestCLIWithFile:
    def test_review_file_with_issues(self, tmp_path: Path):
        diff_path = tmp_path / "test.diff"
        diff_path.write_text(SAMPLE_DIFF)
        result = runner.invoke(app, [str(diff_path)])
        assert result.exit_code == 1
        assert "TODO" in result.output or "debug" in result.output.lower()

    def test_review_clean_file(self, tmp_path: Path):
        diff_path = tmp_path / "clean.diff"
        diff_path.write_text(CLEAN_DIFF)
        result = runner.invoke(app, [str(diff_path)])
        assert result.exit_code == 0
        assert "No issues" in result.output

    def test_review_file_not_found(self):
        result = runner.invoke(app, ["/nonexistent/path.diff"])
        assert result.exit_code == 2


class TestCLIStdin:
    def test_review_from_stdin_dash(self):
        result = runner.invoke(app, ["-"], input=SAMPLE_DIFF)
        assert result.exit_code == 1

    def test_review_from_stdin_no_arg(self):
        result = runner.invoke(app, [], input=SAMPLE_DIFF)
        assert result.exit_code == 1


class TestCLIJsonOutput:
    def test_json_output_valid(self, tmp_path: Path):
        diff_path = tmp_path / "test.diff"
        diff_path.write_text(SAMPLE_DIFF)
        result = runner.invoke(app, [str(diff_path), "--json"])
        data = json.loads(result.output)
        assert "comments" in data
        assert "summary" in data
        assert data["summary"]["total"] > 0

    def test_json_clean_file(self, tmp_path: Path):
        diff_path = tmp_path / "clean.diff"
        diff_path.write_text(CLEAN_DIFF)
        result = runner.invoke(app, [str(diff_path), "--json"])
        data = json.loads(result.output)
        assert data["summary"]["total"] == 0


class TestCLISeverityFilter:
    def test_filter_warning(self, tmp_path: Path):
        diff_path = tmp_path / "test.diff"
        diff_path.write_text(SAMPLE_DIFF)
        result = runner.invoke(app, [str(diff_path), "--json", "--severity", "warning"])
        data = json.loads(result.output)
        for comment in data["comments"]:
            assert comment["severity"] in ("warning", "error")

    def test_filter_error(self, tmp_path: Path):
        diff_path = tmp_path / "secret.diff"
        diff_path.write_text(SECRET_DIFF)
        result = runner.invoke(app, [str(diff_path), "--json", "--severity", "error"])
        data = json.loads(result.output)
        for comment in data["comments"]:
            assert comment["severity"] == "error"

    def test_invalid_severity(self, tmp_path: Path):
        diff_path = tmp_path / "test.diff"
        diff_path.write_text(SAMPLE_DIFF)
        result = runner.invoke(app, [str(diff_path), "--severity", "critical"])
        assert result.exit_code == 2


class TestCLIExitCodes:
    def test_exit_0_no_issues(self, tmp_path: Path):
        diff_path = tmp_path / "clean.diff"
        diff_path.write_text(CLEAN_DIFF)
        result = runner.invoke(app, [str(diff_path)])
        assert result.exit_code == 0

    def test_exit_1_issues_found(self, tmp_path: Path):
        diff_path = tmp_path / "test.diff"
        diff_path.write_text(SAMPLE_DIFF)
        result = runner.invoke(app, [str(diff_path)])
        assert result.exit_code == 1

    def test_exit_2_error(self):
        result = runner.invoke(app, ["/nonexistent/file.diff"])
        assert result.exit_code == 2
