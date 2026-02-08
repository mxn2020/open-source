"""Tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient

from feature_flag_service import routes
from feature_flag_service.app import app
from feature_flag_service.database import FlagDatabase

API_KEY = "test-api-key"


@pytest.fixture(autouse=True)
def _setup_db(tmp_path, monkeypatch):
    """Provide a fresh database and API key for each test."""
    monkeypatch.setenv("FF_API_KEY", API_KEY)
    routes.db = FlagDatabase(db_path=str(tmp_path / "test.db"))
    yield
    routes.db = None


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers():
    return {"X-API-Key": API_KEY}


class TestHealthCheck:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}


class TestCreateFlag:
    def test_create(self, client, auth_headers):
        resp = client.post(
            "/api/flags",
            json={"name": "new-flag", "description": "A flag", "enabled": True},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "new-flag"
        assert data["enabled"] is True
        assert "id" in data

    def test_create_without_auth(self, client):
        resp = client.post("/api/flags", json={"name": "no-auth"})
        assert resp.status_code == 401

    def test_create_wrong_api_key(self, client):
        resp = client.post(
            "/api/flags", json={"name": "bad"}, headers={"X-API-Key": "wrong"}
        )
        assert resp.status_code == 401

    def test_create_duplicate(self, client, auth_headers):
        client.post("/api/flags", json={"name": "dup"}, headers=auth_headers)
        resp = client.post("/api/flags", json={"name": "dup"}, headers=auth_headers)
        assert resp.status_code == 409


class TestListFlags:
    def test_list_empty(self, client):
        resp = client.get("/api/flags")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_with_flags(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "a", "tags": ["x"]},
            headers=auth_headers,
        )
        client.post("/api/flags", json={"name": "b"}, headers=auth_headers)
        resp = client.get("/api/flags")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_list_filter_by_tag(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "tagged", "tags": ["beta"]},
            headers=auth_headers,
        )
        client.post("/api/flags", json={"name": "untagged"}, headers=auth_headers)
        resp = client.get("/api/flags", params={"tag": "beta"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "tagged"


class TestGetFlag:
    def test_get_existing(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "my-flag", "description": "desc"},
            headers=auth_headers,
        )
        resp = client.get("/api/flags/my-flag")
        assert resp.status_code == 200
        assert resp.json()["name"] == "my-flag"

    def test_get_nonexistent(self, client):
        resp = client.get("/api/flags/nope")
        assert resp.status_code == 404


class TestUpdateFlag:
    def test_update(self, client, auth_headers):
        client.post("/api/flags", json={"name": "upd"}, headers=auth_headers)
        resp = client.put(
            "/api/flags/upd",
            json={"enabled": True, "percentage": 50},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["enabled"] is True
        assert data["percentage"] == 50

    def test_update_without_auth(self, client, auth_headers):
        client.post("/api/flags", json={"name": "upd"}, headers=auth_headers)
        resp = client.put("/api/flags/upd", json={"enabled": True})
        assert resp.status_code == 401

    def test_update_nonexistent(self, client, auth_headers):
        resp = client.put(
            "/api/flags/nope", json={"enabled": True}, headers=auth_headers
        )
        assert resp.status_code == 404


class TestDeleteFlag:
    def test_delete(self, client, auth_headers):
        client.post("/api/flags", json={"name": "del"}, headers=auth_headers)
        resp = client.delete("/api/flags/del", headers=auth_headers)
        assert resp.status_code == 204
        assert client.get("/api/flags/del").status_code == 404

    def test_delete_without_auth(self, client, auth_headers):
        client.post("/api/flags", json={"name": "del"}, headers=auth_headers)
        resp = client.delete("/api/flags/del")
        assert resp.status_code == 401

    def test_delete_nonexistent(self, client, auth_headers):
        resp = client.delete("/api/flags/nope", headers=auth_headers)
        assert resp.status_code == 404


class TestEvaluate:
    def test_evaluate_enabled(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "live", "enabled": True},
            headers=auth_headers,
        )
        resp = client.post("/api/evaluate", json={"flag_name": "live"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["flag_name"] == "live"
        assert data["enabled"] is True

    def test_evaluate_disabled(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "off", "enabled": False},
            headers=auth_headers,
        )
        resp = client.post("/api/evaluate", json={"flag_name": "off"})
        assert resp.status_code == 200
        assert resp.json()["enabled"] is False

    def test_evaluate_not_found(self, client):
        resp = client.post("/api/evaluate", json={"flag_name": "missing"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["enabled"] is False
        assert "not found" in data["reason"].lower()

    def test_evaluate_with_user(self, client, auth_headers):
        client.post(
            "/api/flags",
            json={"name": "rollout", "enabled": True, "percentage": 50},
            headers=auth_headers,
        )
        resp = client.post(
            "/api/evaluate",
            json={"flag_name": "rollout", "user_id": "user-1"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data["enabled"], bool)
