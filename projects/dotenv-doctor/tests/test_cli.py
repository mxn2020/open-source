"""Tests for dotenv_doctor.cli."""

import json
import textwrap
from pathlib import Path

from typer.testing import CliRunner

from dotenv_doctor.cli import app

runner = CliRunner()


class TestCheckCommand:
    def test_check_valid_file(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("DATABASE_URL=postgres://localhost/db\nSECRET=hunter2\n")
        result = runner.invoke(app, ["check", str(env_file)])
        assert result.exit_code == 0

    def test_check_file_not_found(self, tmp_path: Path):
        result = runner.invoke(app, ["check", str(tmp_path / "missing.env")])
        assert result.exit_code == 2

    def test_check_with_issues(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=\nKEY=duplicate\n")
        result = runner.invoke(app, ["check", str(env_file)])
        assert result.exit_code == 0
        assert "Duplicate" in result.output or "Empty" in result.output

    def test_check_with_template_missing_key(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("A=1\n")
        template = tmp_path / ".env.example"
        template.write_text("A=\nB=\n")
        result = runner.invoke(app, ["check", str(env_file), "--template", str(template)])
        assert result.exit_code == 1

    def test_check_json_output(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=\n")
        result = runner.invoke(app, ["check", str(env_file), "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_check_template_not_found(self, tmp_path: Path):
        env_file = tmp_path / ".env"
        env_file.write_text("A=1\n")
        result = runner.invoke(
            app, ["check", str(env_file), "--template", str(tmp_path / "nope")]
        )
        assert result.exit_code == 2


class TestCompareCommand:
    def test_compare_identical(self, tmp_path: Path):
        f1 = tmp_path / "a.env"
        f2 = tmp_path / "b.env"
        f1.write_text("KEY=value\n")
        f2.write_text("KEY=value\n")
        result = runner.invoke(app, ["compare", str(f1), str(f2)])
        assert result.exit_code == 0
        assert "identical" in result.output.lower()

    def test_compare_different(self, tmp_path: Path):
        f1 = tmp_path / "a.env"
        f2 = tmp_path / "b.env"
        f1.write_text("KEY=value1\nONLY_IN_1=x\n")
        f2.write_text("KEY=value2\nONLY_IN_2=y\n")
        result = runner.invoke(app, ["compare", str(f1), str(f2)])
        assert result.exit_code == 1

    def test_compare_json_output(self, tmp_path: Path):
        f1 = tmp_path / "a.env"
        f2 = tmp_path / "b.env"
        f1.write_text("A=1\n")
        f2.write_text("B=2\n")
        result = runner.invoke(app, ["compare", str(f1), str(f2), "--json"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert isinstance(data, list)

    def test_compare_file_not_found(self, tmp_path: Path):
        f1 = tmp_path / "a.env"
        f1.write_text("A=1\n")
        result = runner.invoke(app, ["compare", str(f1), str(tmp_path / "nope.env")])
        assert result.exit_code == 2
