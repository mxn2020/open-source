# Development Guide

Instructions for developing and testing pr-reviewer-bot.

## Prerequisites

- Python 3.12 or later
- pip

## Setup

```bash
cd projects/pr-reviewer-bot
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
pytest --cov=pr_reviewer_bot --cov-report=term-missing
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
projects/pr-reviewer-bot/
├── src/pr_reviewer_bot/     # Main package
│   ├── __init__.py          # Version
│   ├── cli.py               # Typer CLI entry point
│   ├── diff_parser.py       # Unified diff parser
│   ├── analyzer.py          # Pattern-based analysis rules
│   └── reporter.py          # Text and JSON output formatting
├── tests/                   # Test suite
│   ├── test_diff_parser.py  # Parser tests
│   ├── test_analyzer.py     # Analyzer rule tests
│   └── test_cli.py          # CLI integration tests
├── examples/                # Sample diff files
│   ├── sample.diff          # Single-file diff with issues
│   └── multi_file.diff      # Multi-file diff with issues
└── docs/                    # Documentation
    ├── design.md            # Architecture and design
    ├── cli.md               # CLI reference
    └── development.md       # This file
```

## Adding a New Rule

1. Open `src/pr_reviewer_bot/analyzer.py`.
2. Add your detection logic inside `analyze_diff()`, iterating over `added_lines`.
3. Create a `ReviewComment` with the appropriate severity and a unique rule name.
4. Add tests in `tests/test_analyzer.py` covering both positive and negative cases.
5. Run `pytest` to verify.

## Release Process

1. Update the version in `src/pr_reviewer_bot/__init__.py` and `pyproject.toml`.
2. Update `CHANGELOG.md` with the new version and changes.
3. Commit, tag, and push.
