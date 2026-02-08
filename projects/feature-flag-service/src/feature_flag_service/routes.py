"""API routes for the feature flag service."""

from fastapi import APIRouter, Depends, HTTPException, Query

from .auth import require_api_key
from .database import FlagDatabase
from .models import (
    EvaluateRequest,
    EvaluateResponse,
    FeatureFlag,
    FeatureFlagCreate,
    FeatureFlagUpdate,
)

router = APIRouter()

# Global database instance, set during app startup
db: FlagDatabase | None = None


def get_db() -> FlagDatabase:
    """Return the database instance."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/api/flags", status_code=201, response_model=FeatureFlag)
async def create_flag(
    flag: FeatureFlagCreate,
    _api_key: str = Depends(require_api_key),
    database: FlagDatabase = Depends(get_db),
) -> FeatureFlag:
    """Create a new feature flag."""
    existing = database.get_flag(flag.name)
    if existing is not None:
        raise HTTPException(status_code=409, detail=f"Flag '{flag.name}' already exists")
    return database.create_flag(flag)


@router.get("/api/flags", response_model=list[FeatureFlag])
async def list_flags(
    tag: str | None = Query(default=None, description="Filter flags by tag"),
    database: FlagDatabase = Depends(get_db),
) -> list[FeatureFlag]:
    """List all feature flags, optionally filtered by tag."""
    return database.list_flags(tag=tag)


@router.get("/api/flags/{name}", response_model=FeatureFlag)
async def get_flag(
    name: str,
    database: FlagDatabase = Depends(get_db),
) -> FeatureFlag:
    """Get a specific feature flag by name."""
    flag = database.get_flag(name)
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{name}' not found")
    return flag


@router.put("/api/flags/{name}", response_model=FeatureFlag)
async def update_flag(
    name: str,
    update: FeatureFlagUpdate,
    _api_key: str = Depends(require_api_key),
    database: FlagDatabase = Depends(get_db),
) -> FeatureFlag:
    """Update an existing feature flag."""
    flag = database.update_flag(name, update)
    if flag is None:
        raise HTTPException(status_code=404, detail=f"Flag '{name}' not found")
    return flag


@router.delete("/api/flags/{name}", status_code=204)
async def delete_flag(
    name: str,
    _api_key: str = Depends(require_api_key),
    database: FlagDatabase = Depends(get_db),
) -> None:
    """Delete a feature flag."""
    deleted = database.delete_flag(name)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Flag '{name}' not found")


@router.post("/api/evaluate", response_model=EvaluateResponse)
async def evaluate_flag(
    request: EvaluateRequest,
    database: FlagDatabase = Depends(get_db),
) -> EvaluateResponse:
    """Evaluate a feature flag for a given user."""
    return database.evaluate_flag(request.flag_name, request.user_id)
