# Contributing to Error Log Summarizer

Thank you for your interest in contributing to Error Log Summarizer.

## Getting Started

1. Fork and clone the repository.
2. Install the project in development mode:

   ```bash
   cd projects/error-log-summarizer
   pip install -e ".[dev]"
   ```

3. Run the test suite to confirm everything works:

   ```bash
   pytest
   ```

## Development Workflow

1. Create a feature branch from `main`.
2. Make your changes, keeping commits focused and well-described.
3. Add or update tests to cover your changes.
4. Run the full test and lint suite:

   ```bash
   pytest --cov=error_log_summarizer
   ruff check src/ tests/
   black --check src/ tests/
   ```

5. Submit a pull request.

## Code Style

This project uses:

- **Black** for code formatting with a line length of 99.
- **Ruff** for linting with a line length of 99.

Run formatters before committing:

```bash
black src/ tests/
ruff check --fix src/ tests/
```

## Adding a New Log Format

1. Add a regex pattern in `src/error_log_summarizer/parser.py`.
2. Update the `_parse_line()` function to try the new pattern.
3. Add test cases in `tests/test_parser.py`.
4. Update the README and `docs/cli.md` with format examples.

## Adding a New Error Category

1. Add a pattern tuple to `_CATEGORY_PATTERNS` in `src/error_log_summarizer/categorizer.py`.
2. Add test cases in `tests/test_categorizer.py`.
3. Update the README.

## Reporting Issues

Open an issue on GitHub with:

- Steps to reproduce the problem.
- Expected and actual behavior.
- A sample log file (redacted of sensitive data) if applicable.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
