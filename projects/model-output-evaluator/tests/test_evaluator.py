"""Tests for the core evaluator."""

import pytest

from model_output_evaluator.evaluator import EvalResult, EvalSummary, evaluate


class TestEvalResult:
    def test_creation(self):
        result = EvalResult(predicted="a", expected="b", scores={"exact_match": 0.0})
        assert result.predicted == "a"
        assert result.expected == "b"
        assert result.scores == {"exact_match": 0.0}

    def test_default_scores(self):
        result = EvalResult(predicted="a", expected="b")
        assert result.scores == {}


class TestEvalSummary:
    def test_default_fields(self):
        summary = EvalSummary()
        assert summary.results == []
        assert summary.avg_scores == {}
        assert summary.metric_names == []


class TestEvaluate:
    def test_identical_predictions(self):
        preds = ["hello", "world"]
        refs = ["hello", "world"]
        summary = evaluate(preds, refs)
        assert summary.avg_scores["exact_match"] == 1.0
        assert summary.avg_scores["contains_match"] == 1.0
        assert len(summary.results) == 2

    def test_no_match(self):
        preds = ["foo", "bar"]
        refs = ["baz", "qux"]
        summary = evaluate(preds, refs)
        assert summary.avg_scores["exact_match"] == 0.0

    def test_mixed_results(self):
        preds = ["hello", "foo"]
        refs = ["hello", "bar"]
        summary = evaluate(preds, refs)
        assert summary.avg_scores["exact_match"] == 0.5

    def test_custom_metrics(self):
        preds = ["hello world"]
        refs = ["hello"]
        summary = evaluate(preds, refs, metrics=["contains_match", "exact_match"])
        assert summary.avg_scores["contains_match"] == 1.0
        assert summary.avg_scores["exact_match"] == 0.0
        assert summary.metric_names == ["contains_match", "exact_match"]

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="same length"):
            evaluate(["a", "b"], ["a"])

    def test_unknown_metric_raises(self):
        with pytest.raises(ValueError, match="Unknown metric"):
            evaluate(["a"], ["a"], metrics=["nonexistent_metric"])

    def test_empty_lists(self):
        summary = evaluate([], [])
        assert summary.results == []
        assert all(v == 0.0 for v in summary.avg_scores.values())

    def test_bleu_metric(self):
        preds = ["the cat sat"]
        refs = ["the cat sat"]
        summary = evaluate(preds, refs, metrics=["bleu_score_simple"])
        assert summary.avg_scores["bleu_score_simple"] == 1.0

    def test_per_result_scores(self):
        preds = ["hello"]
        refs = ["hello"]
        summary = evaluate(preds, refs, metrics=["exact_match"])
        assert len(summary.results) == 1
        assert summary.results[0].scores["exact_match"] == 1.0
        assert summary.results[0].predicted == "hello"
        assert summary.results[0].expected == "hello"
