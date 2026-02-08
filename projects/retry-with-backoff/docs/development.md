# Development Guide

## Prerequisites

- Python 3.12 or later

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd projects/retry-with-backoff

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=retry_with_backoff --cov-report=term-missing

# Run a specific test file
python -m pytest tests/test_strategies.py -v
```

## Linting and Formatting

```bash
# Check linting
ruff check src/ tests/

# Auto-fix lint issues
ruff check --fix src/ tests/

# Check formatting
black --check src/ tests/

# Apply formatting
black src/ tests/
```

## Project Structure

```
projects/retry-with-backoff/
├── src/retry_with_backoff/     # Source code
│   ├── __init__.py             # Public API exports
│   ├── strategies.py           # Backoff strategy implementations
│   ├── retry.py                # retry and async_retry decorators
│   └── exceptions.py           # Custom exceptions
├── tests/                      # Test suite
│   ├── test_strategies.py      # Strategy unit tests
│   ├── test_retry.py           # Retry decorator tests
│   └── test_decorator.py       # Decorator behavior and async tests
├── examples/                   # Usage examples
├── docs/                       # Documentation
└── pyproject.toml              # Project configuration
```

## Adding a New Strategy

1. Create a class that extends `BackoffStrategy` in `strategies.py`.
2. Implement the `delay(attempt: int) -> float` method.
3. Export it from `__init__.py`.
4. Add tests in `test_strategies.py`.
5. Document it in `docs/api.md` and `README.md`.
