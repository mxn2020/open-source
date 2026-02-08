# Contributing to Model Output Evaluator

Thank you for your interest in contributing to this project. This document provides
guidelines for contributing.

## Development Setup

1. Clone the repository and navigate to the project directory:

   ```bash
   cd projects/model-output-evaluator
   ```

2. Create a virtual environment and install the package with dev dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Run the tests:

   ```bash
   pytest
   ```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and
[Black](https://black.readthedocs.io/) for formatting, both configured with a
line length of 99 characters.

```bash
ruff check src/ tests/
black --check src/ tests/
```

## Adding a New Metric

1. Implement the metric function in `src/model_output_evaluator/metrics.py`. The function
   must accept two string arguments (`predicted` and `expected`) and return a float
   between 0.0 and 1.0.
2. Add the metric to the `METRICS_REGISTRY` dictionary in the same file.
3. Write tests for the new metric in `tests/test_metrics.py`.
4. Update documentation in `docs/cli.md` and `docs/design.md`.

## Pull Request Process

1. Ensure all tests pass and linting is clean.
2. Update the CHANGELOG.md with your changes under an "Unreleased" section.
3. Submit a pull request with a clear description of the change.

## Reporting Issues

Please open an issue on the repository with a clear description of the problem,
including steps to reproduce it and the expected vs. actual behavior.
