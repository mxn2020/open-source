# Feature Flag Service

A feature flag management REST API built with [FastAPI](https://fastapi.tiangolo.com/) and SQLite.
Feature flags (also known as feature toggles) let you enable or disable features at runtime
without deploying new code. This service supports percentage-based rollouts with consistent
user bucketing, tag-based organization, and API key authentication for admin operations.

## Features

- **CRUD management** of feature flags via a REST API.
- **Percentage-based rollouts** with consistent user bucketing (SHA-256 hashing).
- **Tag-based organization** for filtering and grouping flags.
- **API key authentication** for admin endpoints (create, update, delete).
- **Unauthenticated read access** for flag evaluation and listing.
- **SQLite storage** with no external database dependencies.
- **Health check endpoint** for monitoring.
- **CORS enabled** out of the box.

## Quick Start

### Prerequisites

- Python 3.12 or later

### Installation

```bash
cd projects/feature-flag-service
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running the Server

```bash
uvicorn feature_flag_service.app:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs are at
`http://localhost:8000/docs`.

### Configuration

| Environment Variable | Description                  | Default         |
| -------------------- | ---------------------------- | --------------- |
| `FF_API_KEY`         | API key for admin endpoints  | `dev-api-key`   |

Set a strong API key in production:

```bash
export FF_API_KEY="your-secret-key"
```

## API Reference

### Health Check

```
GET /health
```

Returns `{"status": "healthy"}`.

### Create a Flag

```
POST /api/flags
X-API-Key: <key>

{
  "name": "dark-mode",
  "description": "Enable dark mode UI",
  "enabled": true,
  "percentage": 100,
  "tags": ["ui", "beta"]
}
```

### List Flags

```
GET /api/flags
GET /api/flags?tag=beta
```

### Get a Flag

```
GET /api/flags/{name}
```

### Update a Flag

```
PUT /api/flags/{name}
X-API-Key: <key>

{
  "enabled": false,
  "percentage": 50
}
```

### Delete a Flag

```
DELETE /api/flags/{name}
X-API-Key: <key>
```

### Evaluate a Flag

```
POST /api/evaluate

{
  "flag_name": "dark-mode",
  "user_id": "user-123"
}
```

Response:

```json
{
  "flag_name": "dark-mode",
  "enabled": true,
  "reason": "User is in rollout group (50%)"
}
```

## Percentage Rollouts

When a flag has `enabled: true` and a `percentage` less than 100, the service uses consistent
hashing to determine whether a given user is in the rollout group. The hash is computed from
the flag name and user ID (`SHA-256(flag_name:user_id) mod 100`), ensuring the same user
always gets the same result for a given flag.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
projects/feature-flag-service/
├── src/feature_flag_service/
│   ├── __init__.py        # Package version
│   ├── app.py             # FastAPI application
│   ├── models.py          # Pydantic data models
│   ├── database.py        # SQLite database layer
│   ├── auth.py            # API key authentication
│   └── routes.py          # API route handlers
├── tests/
│   ├── test_api.py        # API endpoint tests
│   ├── test_models.py     # Model validation tests
│   └── test_database.py   # Database operation tests
├── examples/
│   └── usage.py           # Example API client script
└── docs/
    ├── design.md          # Architecture and design
    ├── api.md             # API reference
    └── development.md     # Development guide
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
