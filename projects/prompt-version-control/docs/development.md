# Development Guide

## Prerequisites

- Python 3.12 or later.
- pip (included with Python).

## Setup

Clone the repository and navigate to the project directory:

```bash
cd projects/prompt-version-control
```

Create a virtual environment and install the project in development mode:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running Tests

Run the full test suite with pytest:

```bash
pytest
```

Run tests with coverage reporting:

```bash
pytest --cov=prompt_version_control --cov-report=term-missing
```

## Linting and Formatting

Check code style with ruff:

```bash
ruff check src/ tests/
```

Format code with black:

```bash
black src/ tests/
```

## Project Structure

```
projects/prompt-version-control/
├── src/prompt_version_control/   # Source code
│   ├── __init__.py               # Package init with version
│   ├── cli.py                    # Typer CLI commands
│   ├── store.py                  # SQLite storage layer
│   ├── models.py                 # Data models
│   └── differ.py                 # Diff engine
├── tests/                        # Test suite
│   ├── test_cli.py               # CLI integration tests
│   ├── test_store.py             # Store unit tests
│   └── test_models.py            # Model unit tests
├── docs/                         # Documentation
├── examples/                     # Example prompt files
└── pyproject.toml                # Project configuration
```

## Architecture

The project follows a layered architecture:

1. **CLI layer** (`cli.py`): Handles argument parsing and user interaction using Typer and Rich.
2. **Storage layer** (`store.py`): Manages SQLite database operations for persisting prompts.
3. **Models** (`models.py`): Defines data structures for prompts and versions.
4. **Diff engine** (`differ.py`): Compares prompt versions using Python's difflib.

## Adding a New Command

1. Define the command function in `cli.py` with the `@app.command()` decorator.
2. Add corresponding logic in `store.py` if database access is needed.
3. Write tests in `tests/test_cli.py` and any other relevant test file.
4. Update the CLI reference in `docs/cli.md`.

## Database Schema

The SQLite database contains three tables:

- **prompts**: `(name TEXT PRIMARY KEY, description TEXT)`
- **versions**: `(id INTEGER PRIMARY KEY, name TEXT, version TEXT, content TEXT, metadata TEXT, created_at TEXT, parent_version TEXT)`
- **tags**: `(name TEXT, tag TEXT, version TEXT, PRIMARY KEY(name, tag))`
