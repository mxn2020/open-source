# Development Guide

## Prerequisites

- Python 3.12 or later
- pip

## Setup

```bash
cd projects/good-first-issue-generator
pip install -e ".[dev]"
```

This installs the package in editable mode along with all development dependencies:
pytest, pytest-cov, ruff, and black.

## Running Tests

Run the full test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=good_first_issue_generator --cov-report=term-missing
```

Run a specific test file:

```bash
pytest tests/test_scanner.py
```

## Linting and Formatting

Check for lint issues:

```bash
ruff check src/ tests/
```

Auto-fix lint issues:

```bash
ruff check --fix src/ tests/
```

Format code:

```bash
black src/ tests/
```

Check formatting without changes:

```bash
black --check src/ tests/
```

## Project Configuration

All configuration is in `pyproject.toml`:

- **Line length**: 99 characters (both Ruff and Black)
- **Test directory**: `tests/`
- **Source directory**: `src/`

## Adding a New Detection Rule

1. Create a private function in `scanner.py` following the pattern:

   ```python
   def _find_new_pattern(filepath: str, lines: list[str]) -> list[CodeOpportunity]:
       opportunities = []
       # Detection logic here
       return opportunities
   ```

2. Call it from `scan_directory()` in the file iteration loop.

3. Add a case to `_make_issue()` in `generator.py` to generate the issue template.

4. Add the type to `TYPE_LABELS` in `generator.py`.

5. Write tests in `test_scanner.py` and `test_generator.py`.

## Release Process

1. Update the version in `src/good_first_issue_generator/__init__.py`
2. Update the version in `pyproject.toml`
3. Add a new section to `CHANGELOG.md`
4. Tag the release and push
