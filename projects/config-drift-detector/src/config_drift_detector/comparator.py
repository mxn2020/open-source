"""Compare two configuration dictionaries and detect drift."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DriftItem:
    """Represents a single configuration drift between two sources.

    Attributes:
        path: Dot-notation path to the drifted key (e.g. "database.host").
        type: The kind of drift — "added", "removed", or "changed".
        old_value: The value in source A (None if added).
        new_value: The value in source B (None if removed).
    """

    path: str
    type: str  # "added" | "removed" | "changed"
    old_value: Any = None
    new_value: Any = None


def compare_configs(
    a: dict,
    b: dict,
    path: str = "",
) -> list[DriftItem]:
    """Recursively compare two configuration dicts and return a list of drifts.

    Args:
        a: The first (source / baseline) configuration.
        b: The second (target / actual) configuration.
        path: Dot-notation prefix used during recursion.

    Returns:
        A list of DriftItem instances describing every difference.
    """
    drifts: list[DriftItem] = []
    all_keys = sorted(set(list(a.keys()) + list(b.keys())))

    for key in all_keys:
        current_path = f"{path}.{key}" if path else key

        if key not in a:
            drifts.append(
                DriftItem(path=current_path, type="added", old_value=None, new_value=b[key])
            )
        elif key not in b:
            drifts.append(
                DriftItem(path=current_path, type="removed", old_value=a[key], new_value=None)
            )
        elif isinstance(a[key], dict) and isinstance(b[key], dict):
            drifts.extend(compare_configs(a[key], b[key], current_path))
        elif a[key] != b[key]:
            drifts.append(
                DriftItem(path=current_path, type="changed", old_value=a[key], new_value=b[key])
            )

    return drifts


def filter_by_tags(
    a: dict,
    b: dict,
    tags: list[str],
) -> tuple[dict, dict]:
    """Filter both configs to only include the specified top-level keys (tags).

    Args:
        a: The first configuration.
        b: The second configuration.
        tags: Top-level keys to keep.

    Returns:
        A tuple of the two filtered dictionaries.
    """
    filtered_a = {k: v for k, v in a.items() if k in tags}
    filtered_b = {k: v for k, v in b.items() if k in tags}
    return filtered_a, filtered_b
