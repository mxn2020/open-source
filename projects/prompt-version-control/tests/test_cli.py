"""Tests for the CLI interface."""

import json

import pytest
from typer.testing import CliRunner

from prompt_version_control.cli import app
from prompt_version_control.store import PromptStore

runner = CliRunner()


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    """Use a temporary database for all CLI tests."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr(
        "prompt_version_control.cli._get_store",
        lambda: PromptStore(db_path=db_path),
    )


class TestSaveCommand:
    def test_save_with_content(self):
        result = runner.invoke(app, ["save", "greeting", "--content", "Hello!"])
        assert result.exit_code == 0
        assert "Saved" in result.output
        assert "1.0" in result.output

    def test_save_with_file(self, tmp_path):
        f = tmp_path / "prompt.txt"
        f.write_text("Hello from file!")
        result = runner.invoke(app, ["save", "greeting", "--file", str(f)])
        assert result.exit_code == 0
        assert "Saved" in result.output

    def test_save_no_content_or_file(self):
        result = runner.invoke(app, ["save", "greeting"])
        assert result.exit_code == 2

    def test_save_both_content_and_file(self, tmp_path):
        f = tmp_path / "prompt.txt"
        f.write_text("file content")
        result = runner.invoke(app, ["save", "greeting", "--content", "text", "--file", str(f)])
        assert result.exit_code == 2

    def test_save_with_metadata(self):
        result = runner.invoke(
            app, ["save", "greeting", "--content", "Hello!", "--meta", "model=gpt-4"]
        )
        assert result.exit_code == 0

    def test_save_json_output(self):
        result = runner.invoke(app, ["save", "greeting", "--content", "Hello!", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["version"] == "1.0"
        assert data["name"] == "greeting"

    def test_save_file_not_found(self):
        result = runner.invoke(app, ["save", "greeting", "--file", "/nonexistent/file.txt"])
        assert result.exit_code == 2

    def test_save_invalid_metadata(self):
        result = runner.invoke(app, ["save", "greeting", "--content", "Hi", "--meta", "badformat"])
        assert result.exit_code == 2


class TestGetCommand:
    def test_get_latest(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello v1"])
        runner.invoke(app, ["save", "greeting", "--content", "Hello v2"])
        result = runner.invoke(app, ["get", "greeting"])
        assert result.exit_code == 0
        assert "Hello v2" in result.output

    def test_get_specific_version(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello v1"])
        runner.invoke(app, ["save", "greeting", "--content", "Hello v2"])
        result = runner.invoke(app, ["get", "greeting", "--version", "1.0"])
        assert result.exit_code == 0
        assert "Hello v1" in result.output

    def test_get_by_tag(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello v1"])
        runner.invoke(app, ["tag", "greeting", "1.0", "stable"])
        result = runner.invoke(app, ["get", "greeting", "--tag", "stable"])
        assert result.exit_code == 0
        assert "Hello v1" in result.output

    def test_get_not_found(self):
        result = runner.invoke(app, ["get", "nonexistent"])
        assert result.exit_code == 1

    def test_get_json_output(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello!"])
        result = runner.invoke(app, ["get", "greeting", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["content"] == "Hello!"


class TestListCommand:
    def test_list_prompts(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        runner.invoke(app, ["save", "summarize", "--content", "Summarize"])
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "greeting" in result.output
        assert "summarize" in result.output

    def test_list_versions(self):
        runner.invoke(app, ["save", "greeting", "--content", "v1"])
        runner.invoke(app, ["save", "greeting", "--content", "v2"])
        result = runner.invoke(app, ["list", "--name", "greeting"])
        assert result.exit_code == 0
        assert "1.0" in result.output
        assert "2.0" in result.output

    def test_list_empty(self):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 1

    def test_list_json_output(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["list", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "greeting" in data


class TestTagCommand:
    def test_tag_version(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["tag", "greeting", "1.0", "stable"])
        assert result.exit_code == 0
        assert "Tagged" in result.output

    def test_tag_not_found(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["tag", "greeting", "99.0", "bad"])
        assert result.exit_code == 1

    def test_tag_json_output(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["tag", "greeting", "1.0", "prod", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["tag"] == "prod"


class TestDiffCommand:
    def test_diff(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello v1"])
        runner.invoke(app, ["save", "greeting", "--content", "Hello v2"])
        result = runner.invoke(app, ["diff", "greeting", "1.0", "2.0"])
        assert result.exit_code == 0
        assert "Hello v1" in result.output or "Hello v2" in result.output

    def test_diff_no_changes(self):
        runner.invoke(app, ["save", "greeting", "--content", "Same"])
        runner.invoke(app, ["save", "greeting", "--content", "Same"])
        result = runner.invoke(app, ["diff", "greeting", "1.0", "2.0"])
        assert result.exit_code == 0
        assert "No differences" in result.output

    def test_diff_not_found(self):
        result = runner.invoke(app, ["diff", "greeting", "1.0", "2.0"])
        assert result.exit_code == 1


class TestDeleteCommand:
    def test_delete(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["delete", "greeting"])
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_delete_not_found(self):
        result = runner.invoke(app, ["delete", "nonexistent"])
        assert result.exit_code == 1

    def test_delete_json_output(self):
        runner.invoke(app, ["save", "greeting", "--content", "Hello"])
        result = runner.invoke(app, ["delete", "greeting", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["deleted"] == "greeting"
