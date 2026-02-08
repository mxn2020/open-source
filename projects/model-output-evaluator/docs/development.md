# Development Guide

## Prerequisites

- Python 3.12 or later.
- A virtual environment manager (venv, virtualenv, or similar).

## Setup

```bash
cd projects/model-output-evaluator
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=model_output_evaluator --cov-report=term-missing
```

## Linting and Formatting

```bash
ruff check src/ tests/
black --check src/ tests/
```

To auto-fix:

```bash
ruff check --fix src/ tests/
black src/ tests/
```

## Project Structure

```
projects/model-output-evaluator/
├── pyproject.toml              # Build config, dependencies, tool settings
├── src/
│   └── model_output_evaluator/
│       ├── __init__.py         # Package version
│       ├── cli.py              # Typer CLI commands
│       ├── evaluator.py        # Core evaluation logic and dataclasses
│       ├── metrics.py          # Metric functions and registry
│       └── reporter.py         # Text and JSON output formatters
├── tests/
│   ├── test_cli.py             # CLI integration tests
│   ├── test_evaluator.py       # Evaluator unit tests
│   └── test_metrics.py         # Metric function unit tests
├── examples/
│   ├── predictions.json        # Sample predictions
│   └── references.json         # Sample references
└── docs/
    ├── design.md               # Architecture and design decisions
    ├── cli.md                  # CLI reference documentation
    └── development.md          # This file
```

## Adding a New Metric

1. Define a function in `src/model_output_evaluator/metrics.py`:

   ```python
   def my_new_metric(predicted: str, expected: str) -> float:
       # Return a value between 0.0 and 1.0
       ...
   ```

2. Register it in `METRICS_REGISTRY`:

   ```python
   METRICS_REGISTRY["my_new_metric"] = my_new_metric
   ```

3. Add tests in `tests/test_metrics.py`.

4. Optionally add it to `DEFAULT_METRICS` if it should be included by default.
