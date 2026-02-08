# Design Document

## Overview

Model Output Evaluator is a command-line tool for evaluating and scoring model outputs
against expected reference results. It provides a set of text comparison metrics and
produces formatted reports in both human-readable and machine-readable formats.

## Architecture

The project is organized into four core modules:

### metrics.py

Contains all evaluation metric functions. Each metric takes two strings (`predicted`
and `expected`) and returns a float between 0.0 (no match) and 1.0 (perfect match).

Available metrics:

- **exact_match**: Binary comparison — 1.0 if strings are identical, 0.0 otherwise.
- **contains_match**: 1.0 if the expected string is a substring of the predicted string.
- **levenshtein_similarity**: Based on the Levenshtein edit distance, computed as
  `1 - (edit_distance / max_len)`. Uses a standard dynamic programming implementation.
- **jaccard_similarity**: Token-level Jaccard index — the size of the intersection of
  word sets divided by the size of their union.
- **bleu_score_simple**: A simplified unigram BLEU-like precision score. Computes the
  proportion of predicted words that appear in the expected text. This is intentionally
  simplified and does not include brevity penalty or higher-order n-grams.

A `METRICS_REGISTRY` dictionary maps metric names to their functions, making it easy
to look up metrics by name and to extend the system with new metrics.

### evaluator.py

Contains the core evaluation logic:

- **EvalResult**: A dataclass holding a single prediction-reference pair and its scores.
- **EvalSummary**: A dataclass holding all results, averaged scores, and metric names.
- **evaluate()**: The main function that takes lists of predictions and references,
  computes per-pair scores using the selected metrics, and returns an `EvalSummary`.

### reporter.py

Provides two output formatters:

- **report_text()**: Generates a Rich-formatted table with per-item and average scores.
- **report_json()**: Generates a JSON representation of the evaluation results.

### cli.py

The Typer-based CLI application with two commands:

- **evaluate-cmd**: Evaluates a single set of predictions against references.
- **compare**: Compares two sets of predictions against the same references.

## Data Flow

```
JSON files → CLI (load & parse) → evaluator (compute scores) → reporter (format) → stdout
```

## Extensibility

New metrics can be added by:

1. Defining a function with the signature `(predicted: str, expected: str) -> float`.
2. Adding it to `METRICS_REGISTRY` in `metrics.py`.
3. Users can select it via the `--metrics` CLI flag.
