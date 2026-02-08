# Development Guide

This document covers setting up and working with the Feature Flag Service codebase.

## Prerequisites

- Python 3.12 or later
- pip

## Setup

```bash
cd projects/feature-flag-service
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

This installs the package in editable mode along with all development dependencies
(pytest, httpx, ruff, black).

## Running the Server

```bash
uvicorn feature_flag_service.app:app --reload
```

The server starts at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the
interactive Swagger UI documentation.

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=feature_flag_service --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_api.py -v

# Run specific test class or method
python -m pytest tests/test_api.py::TestCreateFlag -v
python -m pytest tests/test_api.py::TestCreateFlag::test_create -v
```

Tests use temporary SQLite databases (via `tmp_path` fixture) so they run in isolation
and do not affect any persistent data.

## Linting and Formatting

```bash
# Check linting
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Check formatting
black --check src/ tests/

# Apply formatting
black src/ tests/
```

Both Ruff and Black are configured with a line length of 99 in `pyproject.toml`.

## Project Layout

```
src/feature_flag_service/
├── __init__.py    # Package version (__version__)
├── app.py         # FastAPI app setup, CORS, lifespan
├── models.py      # Pydantic request/response models
├── database.py    # SQLite storage and flag evaluation
├── auth.py        # API key authentication dependency
└── routes.py      # HTTP endpoint handlers
```

## Key Design Patterns

### Dependency Injection

FastAPI's dependency injection is used for both database access and authentication:

```python
@router.post("/api/flags", status_code=201)
async def create_flag(
    flag: FeatureFlagCreate,
    _api_key: str = Depends(require_api_key),
    database: FlagDatabase = Depends(get_db),
) -> FeatureFlag:
    ...
```

### Database Initialization

The database is initialized during app startup using FastAPI's lifespan context manager.
In tests, the database is replaced with a temporary instance via the `_setup_db` fixture.

### Test Isolation

Each test gets a fresh database by using pytest's `tmp_path` fixture to create a unique
SQLite file. The `monkeypatch` fixture is used to set the API key for test authentication.

## Environment Variables

| Variable    | Description                 | Default       |
| ----------- | --------------------------- | ------------- |
| `FF_API_KEY`| API key for admin endpoints | `dev-api-key` |
