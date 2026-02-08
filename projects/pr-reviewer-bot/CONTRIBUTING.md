# Contributing to pr-reviewer-bot

Thank you for your interest in contributing to pr-reviewer-bot! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository and navigate to the project directory:

   ```bash
   cd projects/pr-reviewer-bot
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Run the test suite to verify your setup:

   ```bash
   pytest
   ```

## Making Changes

1. Create a feature branch from `main`.
2. Write tests for any new functionality.
3. Ensure all tests pass with `pytest`.
4. Format code with `black` and lint with `ruff`:

   ```bash
   black src/ tests/
   ruff check src/ tests/
   ```

5. Submit a pull request with a clear description of your changes.

## Adding New Rules

To add a new analysis rule:

1. Open `src/pr_reviewer_bot/analyzer.py`.
2. Add your pattern or logic inside the `analyze_diff` function.
3. Use an appropriate `Severity` level (info, warning, or error).
4. Add tests in `tests/test_analyzer.py`.

## Code Style

- Line length: 99 characters (configured in `pyproject.toml`).
- Follow PEP 8 conventions.
- Use type hints for all function signatures.

## Reporting Issues

Open an issue on the repository with:

- A clear description of the problem.
- Steps to reproduce.
- Expected vs actual behaviour.
