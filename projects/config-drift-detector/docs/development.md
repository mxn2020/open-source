# Development Guide

## Prerequisites

- Python 3.12 or later
- pip

## Setup

```bash
cd projects/config-drift-detector

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=config_drift_detector --cov-report=term-missing

# Run a specific test file
python -m pytest tests/test_comparator.py -v
```

## Linting and Formatting

```bash
# Check for lint errors
ruff check src/ tests/

# Auto-fix lint issues
ruff check --fix src/ tests/

# Format code
black src/ tests/

# Check formatting without changing files
black --check src/ tests/
```

## Project Layout

```
projects/config-drift-detector/
├── src/config_drift_detector/   # Package source code
│   ├── __init__.py              # Version
│   ├── cli.py                   # Typer CLI app
│   ├── comparator.py            # Dict comparison logic
│   ├── parsers.py               # File format parsers
│   └── reporter.py              # Output formatters
├── tests/                       # Test suite
│   ├── test_cli.py
│   ├── test_comparator.py
│   └── test_parsers.py
├── examples/                    # Sample config files
├── docs/                        # Documentation
└── pyproject.toml               # Build & tool configuration
```

## Adding a New Format

1. Add the extension to `SUPPORTED_EXTENSIONS` in `parsers.py`.
2. Add the parsing logic in the `parse_file` function.
3. Add tests in `tests/test_parsers.py`.
4. Update the README and CLI docs.

## Running the CLI Locally

```bash
# After pip install -e .
drift check --a examples/config_a.yaml --b examples/config_b.yaml

# Or run directly via Python
python -m config_drift_detector.cli check --a examples/config_a.yaml --b examples/config_b.yaml
```
