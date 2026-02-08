# Contributing to Feature Flag Service

Thank you for your interest in contributing! This document provides guidelines for
contributing to the Feature Flag Service.

## Getting Started

1. Fork and clone the repository.
2. Navigate to the project directory:
   ```bash
   cd projects/feature-flag-service
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a branch for your change:
   ```bash
   git checkout -b my-feature
   ```
2. Make your changes and add tests.
3. Run the test suite:
   ```bash
   python -m pytest tests/ -v
   ```
4. Run linting and formatting:
   ```bash
   ruff check src/ tests/
   black --check src/ tests/
   ```
5. Commit and push your changes, then open a pull request.

## Code Style

- Line length limit is 99 characters.
- Use [Ruff](https://docs.astral.sh/ruff/) for linting and [Black](https://black.readthedocs.io/) for formatting.
- Write docstrings for all public functions and classes.
- Add type hints to all function signatures.

## Testing

- All new features must include tests.
- Use `pytest` fixtures for test setup and teardown.
- Use temporary databases (via `tmp_path`) to avoid test interference.
- Aim for high test coverage across models, database, and API layers.

## Reporting Issues

- Use GitHub Issues to report bugs or request features.
- Include steps to reproduce, expected behavior, and actual behavior.
