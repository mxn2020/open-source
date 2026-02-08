"""Tests for the CLI interface."""

import json

from typer.testing import CliRunner

from model_output_evaluator.cli import app

runner = CliRunner()


def _write_json(path, data):
    path.write_text(json.dumps(data))


class TestEvaluateCommand:
    def test_basic_evaluate(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        _write_json(preds_file, ["hello", "world"])
        _write_json(refs_file, ["hello", "world"])

        result = runner.invoke(
            app, ["evaluate-cmd", "--predictions", str(preds_file), "--references", str(refs_file)]
        )
        assert result.exit_code == 0

    def test_json_output(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        _write_json(preds_file, ["hello"])
        _write_json(refs_file, ["hello"])

        result = runner.invoke(
            app,
            [
                "evaluate-cmd",
                "--predictions",
                str(preds_file),
                "--references",
                str(refs_file),
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "results" in data
        assert "avg_scores" in data
        assert data["avg_scores"]["exact_match"] == 1.0

    def test_custom_metrics(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        _write_json(preds_file, ["hello world"])
        _write_json(refs_file, ["hello"])

        result = runner.invoke(
            app,
            [
                "evaluate-cmd",
                "--predictions",
                str(preds_file),
                "--references",
                str(refs_file),
                "--metrics",
                "exact_match,contains_match",
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["avg_scores"]["contains_match"] == 1.0
        assert data["avg_scores"]["exact_match"] == 0.0

    def test_length_mismatch(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        _write_json(preds_file, ["hello", "world"])
        _write_json(refs_file, ["hello"])

        result = runner.invoke(
            app, ["evaluate-cmd", "--predictions", str(preds_file), "--references", str(refs_file)]
        )
        assert result.exit_code == 2

    def test_invalid_json(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        preds_file.write_text("not json")
        _write_json(refs_file, ["hello"])

        result = runner.invoke(
            app, ["evaluate-cmd", "--predictions", str(preds_file), "--references", str(refs_file)]
        )
        assert result.exit_code == 2

    def test_non_string_array(self, tmp_path):
        preds_file = tmp_path / "preds.json"
        refs_file = tmp_path / "refs.json"
        _write_json(preds_file, [1, 2, 3])
        _write_json(refs_file, ["a", "b", "c"])

        result = runner.invoke(
            app, ["evaluate-cmd", "--predictions", str(preds_file), "--references", str(refs_file)]
        )
        assert result.exit_code == 2


class TestCompareCommand:
    def test_basic_compare(self, tmp_path):
        a_file = tmp_path / "a.json"
        b_file = tmp_path / "b.json"
        refs_file = tmp_path / "refs.json"
        _write_json(a_file, ["hello", "world"])
        _write_json(b_file, ["hi", "world"])
        _write_json(refs_file, ["hello", "world"])

        result = runner.invoke(
            app,
            ["compare", "--a", str(a_file), "--b", str(b_file), "--references", str(refs_file)],
        )
        assert result.exit_code == 0

    def test_compare_json(self, tmp_path):
        a_file = tmp_path / "a.json"
        b_file = tmp_path / "b.json"
        refs_file = tmp_path / "refs.json"
        _write_json(a_file, ["hello"])
        _write_json(b_file, ["world"])
        _write_json(refs_file, ["hello"])

        result = runner.invoke(
            app,
            [
                "compare",
                "--a",
                str(a_file),
                "--b",
                str(b_file),
                "--references",
                str(refs_file),
                "--json",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "model_a" in data
        assert "model_b" in data
        assert data["model_a"]["avg_scores"]["exact_match"] == 1.0
        assert data["model_b"]["avg_scores"]["exact_match"] == 0.0
