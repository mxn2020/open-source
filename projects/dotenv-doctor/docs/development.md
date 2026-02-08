# Development Guide

## Prerequisites

- Python 3.12 or later
- pip

## Setup

```bash
cd projects/dotenv-doctor
pip install -e ".[dev]"
```

This installs dotenv-doctor in editable mode along with all development dependencies (pytest, ruff, black).

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=dotenv_doctor
```

## Linting

```bash
ruff check src/ tests/
```

Auto-fix:

```bash
ruff check --fix src/ tests/
```

## Formatting

```bash
black src/ tests/
```

Check without modifying:

```bash
black --check src/ tests/
```

## Project Structure

```
projects/dotenv-doctor/
├── src/dotenv_doctor/     # Source code
│   ├── __init__.py        # Package version
│   ├── cli.py             # CLI entry point (Typer app)
│   ├── parser.py          # .env file parsing
│   ├── validator.py       # Validation rules
│   └── reporter.py        # Output formatting
├── tests/                 # Test suite
│   ├── test_parser.py
│   ├── test_validator.py
│   └── test_cli.py
├── examples/              # Example .env files
├── docs/                  # Documentation
└── pyproject.toml         # Project configuration
```

## Adding a New Validation Rule

1. Add a `_check_*` function in `validator.py` that returns `list[Issue]`.
2. Call the new function from `validate_env()`.
3. Add tests in `test_validator.py`.
4. Update the README validation rules table.

## Making a Release

1. Update `__version__` in `src/dotenv_doctor/__init__.py`.
2. Update `version` in `pyproject.toml`.
3. Add an entry to `CHANGELOG.md`.
4. Tag the commit: `git tag v<version>`.
