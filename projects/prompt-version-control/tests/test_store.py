"""Tests for the prompt store."""

import pytest

from prompt_version_control.store import PromptStore


@pytest.fixture
def store(tmp_path):
    """Create a PromptStore with a temporary database."""
    db_path = str(tmp_path / "test.db")
    s = PromptStore(db_path=db_path)
    yield s
    s.close()


class TestPromptStore:
    def test_save_and_get(self, store):
        v = store.save("greeting", "Hello!")
        assert v.version == "1.0"
        assert v.content == "Hello!"
        assert v.parent_version is None

        result = store.get("greeting")
        assert result is not None
        assert result.version == "1.0"
        assert result.content == "Hello!"

    def test_save_auto_increments_version(self, store):
        v1 = store.save("greeting", "Hello v1")
        v2 = store.save("greeting", "Hello v2")
        v3 = store.save("greeting", "Hello v3")

        assert v1.version == "1.0"
        assert v2.version == "2.0"
        assert v3.version == "3.0"
        assert v2.parent_version == "1.0"
        assert v3.parent_version == "2.0"

    def test_save_with_metadata(self, store):
        v = store.save("greeting", "Hello!", metadata={"model": "gpt-4", "temperature": "0.7"})
        assert v.metadata["model"] == "gpt-4"
        assert v.metadata["temperature"] == "0.7"

        result = store.get("greeting", "1.0")
        assert result.metadata["model"] == "gpt-4"

    def test_get_specific_version(self, store):
        store.save("greeting", "Hello v1")
        store.save("greeting", "Hello v2")

        v1 = store.get("greeting", "1.0")
        assert v1 is not None
        assert v1.content == "Hello v1"

        v2 = store.get("greeting", "2.0")
        assert v2 is not None
        assert v2.content == "Hello v2"

    def test_get_latest_version(self, store):
        store.save("greeting", "Hello v1")
        store.save("greeting", "Hello v2")

        latest = store.get("greeting")
        assert latest is not None
        assert latest.version == "2.0"
        assert latest.content == "Hello v2"

    def test_get_nonexistent(self, store):
        assert store.get("nonexistent") is None
        assert store.get("nonexistent", "1.0") is None

    def test_list_prompts(self, store):
        assert store.list_prompts() == []

        store.save("greeting", "Hello")
        store.save("summarize", "Summarize this")
        store.save("greeting", "Hello v2")

        prompts = store.list_prompts()
        assert sorted(prompts) == ["greeting", "summarize"]

    def test_list_versions(self, store):
        store.save("greeting", "Hello v1")
        store.save("greeting", "Hello v2")

        versions = store.list_versions("greeting")
        assert len(versions) == 2
        assert versions[0].version == "1.0"
        assert versions[1].version == "2.0"

    def test_list_versions_empty(self, store):
        versions = store.list_versions("nonexistent")
        assert versions == []

    def test_tag_and_get_by_tag(self, store):
        store.save("greeting", "Hello v1")
        store.save("greeting", "Hello v2")

        store.tag("greeting", "1.0", "stable")
        result = store.get_by_tag("greeting", "stable")
        assert result is not None
        assert result.version == "1.0"
        assert result.content == "Hello v1"

    def test_tag_nonexistent_version(self, store):
        store.save("greeting", "Hello")
        with pytest.raises(ValueError, match="not found"):
            store.tag("greeting", "99.0", "bad")

    def test_get_by_tag_nonexistent(self, store):
        assert store.get_by_tag("greeting", "nonexistent") is None

    def test_tag_overwrite(self, store):
        store.save("greeting", "v1")
        store.save("greeting", "v2")

        store.tag("greeting", "1.0", "latest")
        store.tag("greeting", "2.0", "latest")

        result = store.get_by_tag("greeting", "latest")
        assert result.version == "2.0"

    def test_delete(self, store):
        store.save("greeting", "Hello")
        store.save("greeting", "Hello v2")
        store.tag("greeting", "1.0", "v1")

        assert store.delete("greeting") is True
        assert store.get("greeting") is None
        assert store.list_versions("greeting") == []
        assert store.get_by_tag("greeting", "v1") is None
        assert "greeting" not in store.list_prompts()

    def test_delete_nonexistent(self, store):
        assert store.delete("nonexistent") is False
