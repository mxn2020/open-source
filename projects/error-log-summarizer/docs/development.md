# Development Guide

## Prerequisites

- Python 3.12 or later
- pip

## Setup

Clone the repository and install in editable mode with development dependencies:

```bash
cd projects/error-log-summarizer
pip install -e ".[dev]"
```

## Running Tests

Run the full test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=error_log_summarizer --cov-report=term-missing
```

Run a single test file:

```bash
pytest tests/test_parser.py -v
```

## Linting and Formatting

Check for lint errors:

```bash
ruff check src/ tests/
```

Auto-fix lint errors:

```bash
ruff check --fix src/ tests/
```

Check formatting:

```bash
black --check src/ tests/
```

Apply formatting:

```bash
black src/ tests/
```

## Project Structure

```
projects/error-log-summarizer/
├── src/error_log_summarizer/
│   ├── __init__.py        # Package version
│   ├── cli.py             # Typer CLI commands
│   ├── parser.py          # Log format detection and parsing
│   ├── categorizer.py     # Error categorization and summary
│   └── reporter.py        # Text and JSON output formatters
├── tests/
│   ├── test_parser.py     # Parser unit tests
│   ├── test_categorizer.py# Categorizer unit tests
│   └── test_cli.py        # CLI integration tests
├── examples/              # Sample log files
├── docs/                  # Documentation
├── pyproject.toml         # Build configuration
└── README.md
```

## Adding a New Log Format

1. Define a compiled regex in `parser.py` with named groups.
2. Add a match attempt in `_parse_line()` in the appropriate priority position.
3. Write test cases in `tests/test_parser.py` covering valid and edge cases.
4. Update `docs/cli.md` with the new format syntax.

## Adding a New Error Category

1. Add a `(name, compiled_regex)` tuple to `_CATEGORY_PATTERNS` in `categorizer.py`.
2. Write test cases in `tests/test_categorizer.py`.
3. Update the README.

## Release Process

1. Update `__version__` in `src/error_log_summarizer/__init__.py`.
2. Update `version` in `pyproject.toml`.
3. Add a changelog entry in `CHANGELOG.md`.
4. Tag the release: `git tag v<version>`.
5. Build: `python -m build`.
6. Publish: `twine upload dist/*`.
