# Contributing to retry-with-backoff

Thank you for your interest in contributing! This document provides guidelines for
contributing to the project.

## Getting Started

1. Fork and clone the repository.
2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Run the tests to make sure everything is working:

   ```bash
   python -m pytest tests/ -v
   ```

## Development Workflow

1. Create a feature branch from `main`.
2. Make your changes, adding tests for new functionality.
3. Ensure all tests pass: `python -m pytest tests/ -v`
4. Ensure code passes linting: `ruff check src/ tests/`
5. Ensure code is formatted: `black --check src/ tests/`
6. Submit a pull request.

## Code Style

- Follow PEP 8 guidelines.
- Line length limit is 99 characters (configured in `pyproject.toml`).
- Use type hints for all public APIs.
- Write docstrings for all public classes and functions.

## Testing

- All new features must include tests.
- Tests are in the `tests/` directory using `pytest`.
- Aim for high test coverage.

## Reporting Issues

- Use the GitHub issue tracker.
- Include a minimal reproducible example when reporting bugs.
- Describe expected vs actual behavior.
