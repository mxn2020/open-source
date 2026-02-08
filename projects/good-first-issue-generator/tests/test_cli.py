"""Tests for the CLI module."""

import os

from typer.testing import CliRunner

from good_first_issue_generator.cli import app

runner = CliRunner()


def _write_file(directory: str, name: str, content: str) -> str:
    """Helper to write a file in the given directory."""
    path = os.path.join(directory, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return path


class TestScanCommand:
    """Tests for the scan CLI command."""

    def test_scan_finds_issues(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.py", "# TODO: fix this\ndef broken():\n    pass\n")
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 0

    def test_scan_empty_directory(self, tmp_path: str) -> None:
        result = runner.invoke(app, ["scan", str(tmp_path)])
        assert result.exit_code == 1

    def test_scan_invalid_directory(self) -> None:
        result = runner.invoke(app, ["scan", "/nonexistent/path/abc123"])
        assert result.exit_code == 2

    def test_scan_json_output(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.py", "# TODO: fix this\n")
        result = runner.invoke(app, ["scan", str(tmp_path), "--json"])
        assert result.exit_code == 0
        assert '"title"' in result.output

    def test_scan_markdown_output(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.py", "# TODO: fix this\n")
        result = runner.invoke(app, ["scan", str(tmp_path), "--markdown"])
        assert result.exit_code == 0
        assert "# Good First Issues" in result.output

    def test_scan_max_issues(self, tmp_path: str) -> None:
        content = "\n".join(f"# TODO: item {i}" for i in range(20))
        _write_file(str(tmp_path), "app.py", content + "\n")
        result = runner.invoke(app, ["scan", str(tmp_path), "--max", "3", "--json"])
        assert result.exit_code == 0
        import json

        data = json.loads(result.output)
        assert len(data) <= 3

    def test_scan_custom_extensions(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.ts", "// TODO: implement\n")
        result = runner.invoke(app, ["scan", str(tmp_path), "--extensions", ".ts"])
        assert result.exit_code == 0


class TestStatsCommand:
    """Tests for the stats CLI command."""

    def test_stats_shows_counts(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.py", "# TODO: fix\ndef broken():\n    pass\n")
        result = runner.invoke(app, ["stats", str(tmp_path)])
        assert result.exit_code == 0
        assert "Total opportunities" in result.output

    def test_stats_empty_directory(self, tmp_path: str) -> None:
        result = runner.invoke(app, ["stats", str(tmp_path)])
        assert result.exit_code == 0

    def test_stats_invalid_directory(self) -> None:
        result = runner.invoke(app, ["stats", "/nonexistent/path/abc123"])
        assert result.exit_code == 2


class TestVersionFlag:
    """Tests for the --version flag."""

    def test_version_output(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
