# CLI Reference

## Installation

```bash
pip install -e ".[dev]"
```

## Commands

### evaluate-cmd

Evaluate model predictions against reference outputs.

```bash
model-eval evaluate-cmd --predictions <file> --references <file> [--metrics m1,m2] [--json]
```

**Options:**

| Flag | Short | Description |
|------|-------|-------------|
| `--predictions` | `-p` | Path to a JSON file containing an array of predicted strings. |
| `--references` | `-r` | Path to a JSON file containing an array of reference strings. |
| `--metrics` | `-m` | Comma-separated list of metrics to use. Defaults to: `exact_match`, `contains_match`, `levenshtein_similarity`, `jaccard_similarity`. |
| `--json` | | Output results as JSON instead of a formatted table. |

**Example:**

```bash
model-eval evaluate-cmd \
    --predictions examples/predictions.json \
    --references examples/references.json

model-eval evaluate-cmd \
    --predictions examples/predictions.json \
    --references examples/references.json \
    --metrics exact_match,bleu_score_simple \
    --json
```

### compare

Compare two sets of predictions against the same references.

```bash
model-eval compare --a <file> --b <file> --references <file> [--metrics m1,m2] [--json]
```

**Options:**

| Flag | Short | Description |
|------|-------|-------------|
| `--a` | | Path to a JSON file with the first set of predictions. |
| `--b` | | Path to a JSON file with the second set of predictions. |
| `--references` | `-r` | Path to a JSON file containing reference strings. |
| `--metrics` | `-m` | Comma-separated list of metrics. |
| `--json` | | Output results as JSON. |

**Example:**

```bash
model-eval compare \
    --a model_a_predictions.json \
    --b model_b_predictions.json \
    --references examples/references.json
```

## Available Metrics

| Metric | Description |
|--------|-------------|
| `exact_match` | 1.0 if strings are identical, 0.0 otherwise. |
| `contains_match` | 1.0 if the expected string is a substring of the predicted string. |
| `levenshtein_similarity` | 1 - (edit_distance / max_len). |
| `jaccard_similarity` | Token-level Jaccard index (intersection / union of word sets). |
| `bleu_score_simple` | Simplified unigram BLEU precision (overlap of words / predicted words). |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success. |
| 2 | Error (invalid input, mismatched lengths, unknown metric, etc.). |

## Input Format

Both `--predictions` and `--references` files must be JSON files containing an array
of strings:

```json
[
    "First output string.",
    "Second output string.",
    "Third output string."
]
```

The predictions and references arrays must have the same length.
