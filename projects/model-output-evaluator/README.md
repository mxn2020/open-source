# Model Output Evaluator

A command-line tool for evaluating and scoring model outputs against expected reference
results. Provides multiple text comparison metrics and outputs results as formatted
tables or JSON.

## Features

- **Five evaluation metrics**: exact match, contains match, Levenshtein similarity,
  Jaccard similarity, and simplified unigram BLEU.
- **Evaluate command**: Score a set of model predictions against references.
- **Compare command**: Compare two models' predictions side by side.
- **Flexible output**: Rich-formatted tables for human consumption or JSON for
  programmatic use.
- **Extensible**: Add custom metrics by implementing a simple function interface.

## Installation

```bash
cd projects/model-output-evaluator
pip install -e ".[dev]"
```

## Quick Start

Evaluate predictions against references:

```bash
model-eval evaluate-cmd \
    --predictions examples/predictions.json \
    --references examples/references.json
```

Output as JSON:

```bash
model-eval evaluate-cmd \
    --predictions examples/predictions.json \
    --references examples/references.json \
    --json
```

Select specific metrics:

```bash
model-eval evaluate-cmd \
    --predictions examples/predictions.json \
    --references examples/references.json \
    --metrics exact_match,bleu_score_simple
```

Compare two models:

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
| `contains_match` | 1.0 if expected is a substring of predicted. |
| `levenshtein_similarity` | 1 - (edit_distance / max_len). |
| `jaccard_similarity` | Token-level Jaccard index (intersection / union of word sets). |
| `bleu_score_simple` | Simplified unigram BLEU precision (overlap / predicted words). |

All metrics return a float between 0.0 and 1.0.

## Input Format

Both predictions and references files must be JSON arrays of strings:

```json
[
    "First output.",
    "Second output.",
    "Third output."
]
```

The two arrays must have the same length.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
black --check src/ tests/
```

See [docs/development.md](docs/development.md) for the full development guide,
[docs/cli.md](docs/cli.md) for the CLI reference, and
[docs/design.md](docs/design.md) for the architecture overview.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
