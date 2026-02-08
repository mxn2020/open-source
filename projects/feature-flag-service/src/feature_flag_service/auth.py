"""API key authentication for admin endpoints."""

import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key() -> str:
    """Return the configured API key from environment or default."""
    return os.environ.get("FF_API_KEY", "dev-api-key")


async def require_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> str:
    """Dependency that enforces API key authentication."""
    expected = get_api_key()
    if api_key is None or api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key
