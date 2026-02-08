# Contributing to Config Drift Detector

Thank you for your interest in contributing! This document provides guidelines
for contributing to the project.

## Getting Started

1. Fork and clone the repository.
2. Create a virtual environment and install development dependencies:
   ```bash
   cd projects/config-drift-detector
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```
3. Create a feature branch: `git checkout -b my-feature`

## Development Workflow

- **Run tests:** `python -m pytest tests/ -v`
- **Run linter:** `ruff check src/ tests/`
- **Format code:** `black src/ tests/`

## Pull Request Guidelines

- Keep changes focused and small.
- Add or update tests for any new functionality.
- Ensure all tests pass before submitting.
- Follow existing code style (enforced by Ruff and Black).

## Reporting Issues

Open a GitHub issue with a clear description of the problem, steps to
reproduce, and expected vs. actual behavior.

## Code of Conduct

Please be respectful and constructive in all interactions. See the repository
root `CODE_OF_CONDUCT.md` for details.
