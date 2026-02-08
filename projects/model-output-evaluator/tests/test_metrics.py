"""Tests for evaluation metrics."""

from model_output_evaluator.metrics import (
    bleu_score_simple,
    contains_match,
    exact_match,
    jaccard_similarity,
    levenshtein_similarity,
)


class TestExactMatch:
    def test_identical_strings(self):
        assert exact_match("hello", "hello") == 1.0

    def test_different_strings(self):
        assert exact_match("hello", "world") == 0.0

    def test_empty_strings(self):
        assert exact_match("", "") == 1.0

    def test_case_sensitive(self):
        assert exact_match("Hello", "hello") == 0.0

    def test_whitespace_matters(self):
        assert exact_match("hello ", "hello") == 0.0


class TestContainsMatch:
    def test_exact_match(self):
        assert contains_match("hello", "hello") == 1.0

    def test_substring(self):
        assert contains_match("hello world", "hello") == 1.0

    def test_not_contained(self):
        assert contains_match("hello", "world") == 0.0

    def test_empty_expected(self):
        assert contains_match("hello", "") == 1.0

    def test_empty_predicted(self):
        assert contains_match("", "hello") == 0.0

    def test_both_empty(self):
        assert contains_match("", "") == 1.0


class TestLevenshteinSimilarity:
    def test_identical(self):
        assert levenshtein_similarity("hello", "hello") == 1.0

    def test_completely_different(self):
        assert levenshtein_similarity("abc", "xyz") == 0.0

    def test_one_edit(self):
        result = levenshtein_similarity("cat", "bat")
        assert abs(result - (1 - 1 / 3)) < 1e-9

    def test_empty_strings(self):
        assert levenshtein_similarity("", "") == 1.0

    def test_one_empty(self):
        assert levenshtein_similarity("hello", "") == 0.0

    def test_other_empty(self):
        assert levenshtein_similarity("", "hello") == 0.0

    def test_partial_similarity(self):
        result = levenshtein_similarity("kitten", "sitting")
        assert 0.0 < result < 1.0


class TestJaccardSimilarity:
    def test_identical(self):
        assert jaccard_similarity("the cat sat", "the cat sat") == 1.0

    def test_no_overlap(self):
        assert jaccard_similarity("hello world", "foo bar") == 0.0

    def test_partial_overlap(self):
        result = jaccard_similarity("the cat", "the dog")
        assert abs(result - 1 / 3) < 1e-9

    def test_empty_strings(self):
        assert jaccard_similarity("", "") == 1.0

    def test_one_empty(self):
        assert jaccard_similarity("hello", "") == 0.0

    def test_duplicate_tokens(self):
        result = jaccard_similarity("the the the", "the")
        assert result == 1.0


class TestBleuScoreSimple:
    def test_identical(self):
        assert bleu_score_simple("the cat sat", "the cat sat") == 1.0

    def test_no_overlap(self):
        assert bleu_score_simple("hello world", "foo bar") == 0.0

    def test_partial_overlap(self):
        result = bleu_score_simple("the cat sat", "the dog sat")
        assert abs(result - 2 / 3) < 1e-9

    def test_empty_strings(self):
        assert bleu_score_simple("", "") == 1.0

    def test_empty_predicted(self):
        assert bleu_score_simple("", "hello") == 0.0

    def test_all_predicted_in_expected(self):
        assert bleu_score_simple("cat", "the cat sat on the mat") == 1.0
