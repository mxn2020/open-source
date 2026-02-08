"""Tests for the database layer."""

import pytest

from feature_flag_service.database import FlagDatabase
from feature_flag_service.models import FeatureFlagCreate, FeatureFlagUpdate


@pytest.fixture()
def db(tmp_path):
    """Provide a fresh database for each test."""
    return FlagDatabase(db_path=str(tmp_path / "test.db"))


@pytest.fixture()
def sample_flag(db):
    """Create and return a sample flag."""
    return db.create_flag(
        FeatureFlagCreate(
            name="dark-mode",
            description="Enable dark mode",
            enabled=True,
            percentage=100,
            tags=["ui", "beta"],
        )
    )


class TestCreateFlag:
    def test_create_flag(self, db):
        flag = db.create_flag(FeatureFlagCreate(name="my-flag", description="A flag"))
        assert flag.name == "my-flag"
        assert flag.description == "A flag"
        assert flag.enabled is False
        assert flag.id is not None

    def test_create_duplicate_raises(self, db, sample_flag):
        with pytest.raises(Exception):
            db.create_flag(FeatureFlagCreate(name="dark-mode"))


class TestGetFlag:
    def test_get_existing(self, db, sample_flag):
        flag = db.get_flag("dark-mode")
        assert flag is not None
        assert flag.name == "dark-mode"
        assert flag.description == "Enable dark mode"

    def test_get_nonexistent(self, db):
        assert db.get_flag("nonexistent") is None


class TestListFlags:
    def test_list_empty(self, db):
        assert db.list_flags() == []

    def test_list_all(self, db, sample_flag):
        db.create_flag(FeatureFlagCreate(name="other-flag"))
        flags = db.list_flags()
        assert len(flags) == 2

    def test_list_by_tag(self, db, sample_flag):
        db.create_flag(FeatureFlagCreate(name="other-flag", tags=["backend"]))
        flags = db.list_flags(tag="ui")
        assert len(flags) == 1
        assert flags[0].name == "dark-mode"

    def test_list_by_tag_no_match(self, db, sample_flag):
        flags = db.list_flags(tag="nonexistent")
        assert len(flags) == 0


class TestUpdateFlag:
    def test_update_enabled(self, db, sample_flag):
        updated = db.update_flag("dark-mode", FeatureFlagUpdate(enabled=False))
        assert updated is not None
        assert updated.enabled is False
        assert updated.name == "dark-mode"

    def test_update_name(self, db, sample_flag):
        updated = db.update_flag("dark-mode", FeatureFlagUpdate(name="night-mode"))
        assert updated is not None
        assert updated.name == "night-mode"

    def test_update_nonexistent(self, db):
        result = db.update_flag("nope", FeatureFlagUpdate(enabled=True))
        assert result is None

    def test_update_no_changes(self, db, sample_flag):
        updated = db.update_flag("dark-mode", FeatureFlagUpdate())
        assert updated is not None
        assert updated.name == "dark-mode"

    def test_update_tags(self, db, sample_flag):
        updated = db.update_flag("dark-mode", FeatureFlagUpdate(tags=["v2"]))
        assert updated is not None
        assert updated.tags == ["v2"]


class TestDeleteFlag:
    def test_delete_existing(self, db, sample_flag):
        assert db.delete_flag("dark-mode") is True
        assert db.get_flag("dark-mode") is None

    def test_delete_nonexistent(self, db):
        assert db.delete_flag("nope") is False


class TestEvaluateFlag:
    def test_evaluate_nonexistent(self, db):
        result = db.evaluate_flag("nope")
        assert result.enabled is False
        assert "not found" in result.reason.lower()

    def test_evaluate_disabled(self, db):
        db.create_flag(FeatureFlagCreate(name="off-flag", enabled=False))
        result = db.evaluate_flag("off-flag")
        assert result.enabled is False
        assert "disabled" in result.reason.lower()

    def test_evaluate_enabled_full_rollout(self, db, sample_flag):
        result = db.evaluate_flag("dark-mode")
        assert result.enabled is True

    def test_evaluate_zero_percentage(self, db):
        db.create_flag(FeatureFlagCreate(name="zero", enabled=True, percentage=0))
        result = db.evaluate_flag("zero", user_id="user1")
        assert result.enabled is False

    def test_evaluate_with_user_id_consistent(self, db):
        db.create_flag(FeatureFlagCreate(name="partial", enabled=True, percentage=50))
        result1 = db.evaluate_flag("partial", user_id="user-42")
        result2 = db.evaluate_flag("partial", user_id="user-42")
        assert result1.enabled == result2.enabled
        assert result1.reason == result2.reason

    def test_evaluate_no_user_id_with_percentage(self, db):
        db.create_flag(FeatureFlagCreate(name="partial", enabled=True, percentage=50))
        result = db.evaluate_flag("partial")
        assert result.enabled is True
        assert "no user_id" in result.reason.lower()
