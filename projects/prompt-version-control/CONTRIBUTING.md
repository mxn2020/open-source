# Contributing to Prompt Version Control

Thank you for your interest in contributing to prompt-version-control! This document provides
guidelines and instructions for contributing.

## Getting Started

1. Fork and clone the repository.
2. Navigate to the project directory:
   ```bash
   cd projects/prompt-version-control
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and write tests.
3. Run the test suite:
   ```bash
   pytest
   ```
4. Run the linter and formatter:
   ```bash
   ruff check src/ tests/
   black src/ tests/
   ```
5. Commit your changes with a descriptive message.
6. Open a pull request.

## Code Style

- Follow PEP 8 conventions.
- Use type hints for all function signatures.
- Maximum line length is 99 characters (enforced by ruff and black).
- Write docstrings for all public functions and classes.

## Testing

- All new features must include tests.
- Tests are located in the `tests/` directory.
- Use `pytest` as the test runner.
- Aim for high test coverage.

## Reporting Issues

- Use GitHub Issues to report bugs or request features.
- Include steps to reproduce bugs.
- Provide the Python version and operating system.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
