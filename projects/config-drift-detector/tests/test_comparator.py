"""Tests for config_drift_detector.comparator."""

from __future__ import annotations

from config_drift_detector.comparator import DriftItem, compare_configs, filter_by_tags

# -- Basic comparison -------------------------------------------------------


def test_identical_configs():
    cfg = {"a": 1, "b": {"c": 2}}
    assert compare_configs(cfg, cfg) == []


def test_added_key():
    a = {"x": 1}
    b = {"x": 1, "y": 2}
    drifts = compare_configs(a, b)
    assert drifts == [DriftItem(path="y", type="added", old_value=None, new_value=2)]


def test_removed_key():
    a = {"x": 1, "y": 2}
    b = {"x": 1}
    drifts = compare_configs(a, b)
    assert drifts == [DriftItem(path="y", type="removed", old_value=2, new_value=None)]


def test_changed_value():
    a = {"x": 1}
    b = {"x": 99}
    drifts = compare_configs(a, b)
    assert drifts == [DriftItem(path="x", type="changed", old_value=1, new_value=99)]


# -- Nested comparison ------------------------------------------------------


def test_nested_changed():
    a = {"db": {"host": "localhost", "port": 5432}}
    b = {"db": {"host": "remotehost", "port": 5432}}
    drifts = compare_configs(a, b)
    assert len(drifts) == 1
    assert drifts[0].path == "db.host"
    assert drifts[0].type == "changed"


def test_nested_added():
    a = {"db": {"host": "localhost"}}
    b = {"db": {"host": "localhost", "port": 5432}}
    drifts = compare_configs(a, b)
    assert drifts == [DriftItem(path="db.port", type="added", old_value=None, new_value=5432)]


def test_deeply_nested():
    a = {"a": {"b": {"c": {"d": 1}}}}
    b = {"a": {"b": {"c": {"d": 2}}}}
    drifts = compare_configs(a, b)
    assert len(drifts) == 1
    assert drifts[0].path == "a.b.c.d"


# -- Multiple drifts -------------------------------------------------------


def test_multiple_drifts():
    a = {"x": 1, "y": 2, "z": 3}
    b = {"x": 10, "y": 2, "w": 4}
    drifts = compare_configs(a, b)
    paths = {d.path for d in drifts}
    types = {d.path: d.type for d in drifts}
    assert paths == {"w", "x", "z"}
    assert types["w"] == "added"
    assert types["x"] == "changed"
    assert types["z"] == "removed"


# -- Tag filtering ----------------------------------------------------------


def test_filter_by_tags():
    a = {"db": {"host": "h1"}, "cache": {"ttl": 60}, "logging": {"level": "info"}}
    b = {"db": {"host": "h2"}, "cache": {"ttl": 120}, "logging": {"level": "debug"}}
    fa, fb = filter_by_tags(a, b, ["db", "cache"])
    drifts = compare_configs(fa, fb)
    paths = {d.path for d in drifts}
    assert "db.host" in paths
    assert "cache.ttl" in paths
    assert "logging.level" not in paths


def test_filter_by_tags_missing_key():
    a = {"db": {"host": "h1"}}
    b = {"db": {"host": "h2"}}
    fa, fb = filter_by_tags(a, b, ["nonexistent"])
    assert fa == {}
    assert fb == {}
    assert compare_configs(fa, fb) == []
