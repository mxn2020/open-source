"""Pydantic models for the feature flag service."""

import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class FeatureFlagCreate(BaseModel):
    """Schema for creating a new feature flag."""

    name: str
    description: str = ""
    enabled: bool = False
    percentage: int = Field(default=100, ge=0, le=100)
    tags: list[str] = Field(default_factory=list)


class FeatureFlagUpdate(BaseModel):
    """Schema for updating an existing feature flag."""

    name: str | None = None
    description: str | None = None
    enabled: bool | None = None
    percentage: int | None = Field(default=None, ge=0, le=100)
    tags: list[str] | None = None


class FeatureFlag(BaseModel):
    """Full feature flag representation."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    enabled: bool = False
    percentage: int = Field(default=100, ge=0, le=100)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvaluateRequest(BaseModel):
    """Schema for evaluating a feature flag."""

    flag_name: str
    user_id: str | None = None


class EvaluateResponse(BaseModel):
    """Response from evaluating a feature flag."""

    flag_name: str
    enabled: bool
    reason: str
