# Contributing to dotenv-doctor

Thank you for your interest in contributing! This document explains how to get started.

## Getting Started

1. Fork and clone the repository.
2. Navigate to the project directory:
   ```bash
   cd projects/dotenv-doctor
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run the tests:
   ```bash
   pytest
   ```

## Development Workflow

1. Create a feature branch from `main`.
2. Write your code and add tests.
3. Ensure all tests pass: `pytest`
4. Lint your code: `ruff check src/ tests/`
5. Format your code: `black src/ tests/`
6. Submit a pull request.

## Code Style

- Line length: 99 characters.
- Use [Ruff](https://docs.astral.sh/ruff/) for linting and [Black](https://black.readthedocs.io/) for formatting.
- Write type hints for all public function signatures.
- Write docstrings for all public modules, classes, and functions.

## Testing

- All new features must include tests.
- Use `pytest` as the test framework.
- Place tests in the `tests/` directory with a `test_` prefix.

## Reporting Issues

Open an issue describing the problem, including steps to reproduce and the expected vs actual behavior.
