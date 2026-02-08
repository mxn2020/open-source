"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from feature_flag_service.models import (
    EvaluateRequest,
    EvaluateResponse,
    FeatureFlag,
    FeatureFlagCreate,
    FeatureFlagUpdate,
)


class TestFeatureFlagCreate:
    def test_minimal_create(self):
        flag = FeatureFlagCreate(name="test-flag")
        assert flag.name == "test-flag"
        assert flag.description == ""
        assert flag.enabled is False
        assert flag.percentage == 100
        assert flag.tags == []

    def test_full_create(self):
        flag = FeatureFlagCreate(
            name="beta-feature",
            description="A beta feature",
            enabled=True,
            percentage=50,
            tags=["beta", "ui"],
        )
        assert flag.name == "beta-feature"
        assert flag.description == "A beta feature"
        assert flag.enabled is True
        assert flag.percentage == 50
        assert flag.tags == ["beta", "ui"]

    def test_percentage_validation_too_low(self):
        with pytest.raises(ValidationError):
            FeatureFlagCreate(name="bad", percentage=-1)

    def test_percentage_validation_too_high(self):
        with pytest.raises(ValidationError):
            FeatureFlagCreate(name="bad", percentage=101)


class TestFeatureFlagUpdate:
    def test_all_none(self):
        update = FeatureFlagUpdate()
        assert update.name is None
        assert update.description is None
        assert update.enabled is None
        assert update.percentage is None
        assert update.tags is None

    def test_partial_update(self):
        update = FeatureFlagUpdate(enabled=True, percentage=75)
        assert update.enabled is True
        assert update.percentage == 75
        assert update.name is None

    def test_percentage_validation(self):
        with pytest.raises(ValidationError):
            FeatureFlagUpdate(percentage=200)


class TestFeatureFlag:
    def test_defaults(self):
        flag = FeatureFlag(name="my-flag")
        assert flag.id is not None
        assert len(flag.id) == 36  # UUID format
        assert flag.name == "my-flag"
        assert flag.enabled is False
        assert flag.percentage == 100
        assert flag.created_at is not None
        assert flag.updated_at is not None

    def test_unique_ids(self):
        flag1 = FeatureFlag(name="a")
        flag2 = FeatureFlag(name="b")
        assert flag1.id != flag2.id


class TestEvaluateRequest:
    def test_minimal(self):
        req = EvaluateRequest(flag_name="my-flag")
        assert req.flag_name == "my-flag"
        assert req.user_id is None

    def test_with_user_id(self):
        req = EvaluateRequest(flag_name="my-flag", user_id="user-123")
        assert req.user_id == "user-123"


class TestEvaluateResponse:
    def test_response(self):
        resp = EvaluateResponse(flag_name="f", enabled=True, reason="ok")
        assert resp.flag_name == "f"
        assert resp.enabled is True
        assert resp.reason == "ok"
