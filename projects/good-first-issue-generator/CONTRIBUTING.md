# Contributing to Good First Issue Generator

Thank you for your interest in contributing to the Good First Issue Generator.

## Getting Started

1. Clone the repository and navigate to the project:

   ```bash
   cd projects/good-first-issue-generator
   ```

2. Install in development mode:

   ```bash
   pip install -e ".[dev]"
   ```

3. Run the test suite to confirm everything works:

   ```bash
   pytest
   ```

## Development Workflow

1. Create a branch for your changes
2. Make your changes with appropriate test coverage
3. Run linting and formatting:

   ```bash
   ruff check src/ tests/
   black src/ tests/
   ```

4. Run the full test suite:

   ```bash
   pytest --cov=good_first_issue_generator
   ```

5. Submit a pull request with a clear description of your changes

## Code Style

- Line length: 99 characters (enforced by Ruff and Black)
- Follow existing code conventions in the project
- Add docstrings to all public functions and classes
- Add type hints to all function signatures

## Adding New Opportunity Types

To add a new type of code improvement opportunity:

1. Add a detection function in `scanner.py` (follow the pattern of `_find_todos`)
2. Add the new type to the `_make_issue` function in `generator.py`
3. Add the type labels mapping in `generator.py`
4. Add tests in `test_scanner.py` and `test_generator.py`

## Reporting Issues

If you find a bug or have a feature request, please open an issue with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior (for bugs)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
