"""Tests for prompt version control models."""

from prompt_version_control.models import PromptRecord, PromptVersion


class TestPromptVersion:
    def test_create_with_defaults(self):
        v = PromptVersion(version="1.0", content="Hello, world!")
        assert v.version == "1.0"
        assert v.content == "Hello, world!"
        assert v.metadata == {}
        assert v.parent_version is None
        assert v.created_at is not None

    def test_create_with_all_fields(self):
        v = PromptVersion(
            version="2.0",
            content="Summarize this.",
            metadata={"model": "gpt-4", "temperature": "0.7"},
            created_at="2025-01-01T00:00:00+00:00",
            parent_version="1.0",
        )
        assert v.version == "2.0"
        assert v.metadata["model"] == "gpt-4"
        assert v.parent_version == "1.0"

    def test_to_dict(self):
        v = PromptVersion(
            version="1.0",
            content="test",
            metadata={"key": "value"},
            created_at="2025-01-01T00:00:00+00:00",
            parent_version=None,
        )
        d = v.to_dict()
        assert d["version"] == "1.0"
        assert d["content"] == "test"
        assert d["metadata"] == {"key": "value"}
        assert d["parent_version"] is None


class TestPromptRecord:
    def test_create_empty(self):
        r = PromptRecord(name="greeting")
        assert r.name == "greeting"
        assert r.description == ""
        assert r.versions == []
        assert r.tags == {}

    def test_latest_version_empty(self):
        r = PromptRecord(name="test")
        assert r.latest_version() is None

    def test_latest_version(self):
        v1 = PromptVersion(version="1.0", content="v1")
        v2 = PromptVersion(version="2.0", content="v2")
        r = PromptRecord(name="test", versions=[v1, v2])
        assert r.latest_version() == v2

    def test_get_version(self):
        v1 = PromptVersion(version="1.0", content="v1")
        v2 = PromptVersion(version="2.0", content="v2")
        r = PromptRecord(name="test", versions=[v1, v2])
        assert r.get_version("1.0") == v1
        assert r.get_version("3.0") is None

    def test_to_dict(self):
        v = PromptVersion(version="1.0", content="test", created_at="2025-01-01T00:00:00+00:00")
        r = PromptRecord(
            name="greeting", description="A greeting", versions=[v], tags={"prod": "1.0"}
        )
        d = r.to_dict()
        assert d["name"] == "greeting"
        assert d["description"] == "A greeting"
        assert len(d["versions"]) == 1
        assert d["tags"]["prod"] == "1.0"
