"""Reporters that format drift results for humans and machines."""

from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table

from config_drift_detector.comparator import DriftItem

_TYPE_STYLES = {
    "added": "green",
    "removed": "red",
    "changed": "yellow",
}


def report_text(drifts: list[DriftItem]) -> str:
    """Render drifts as a Rich-formatted table and return the string.

    Args:
        drifts: List of detected drifts.

    Returns:
        The rendered table as a string.
    """
    if not drifts:
        return "No configuration drift detected."

    table = Table(title="Configuration Drift Report", show_lines=True)
    table.add_column("Path", style="cyan", no_wrap=True)
    table.add_column("Type", justify="center")
    table.add_column("Old Value", style="dim")
    table.add_column("New Value")

    for d in drifts:
        style = _TYPE_STYLES.get(d.type, "")
        table.add_row(
            d.path,
            f"[{style}]{d.type}[/{style}]",
            _fmt(d.old_value),
            _fmt(d.new_value),
        )

    console = Console(record=True, width=120)
    console.print(table)
    return console.export_text()


def report_json(drifts: list[DriftItem]) -> str:
    """Render drifts as a JSON string.

    Args:
        drifts: List of detected drifts.

    Returns:
        A JSON-formatted string.
    """
    payload = [
        {
            "path": d.path,
            "type": d.type,
            "old_value": d.old_value,
            "new_value": d.new_value,
        }
        for d in drifts
    ]
    return json.dumps(payload, indent=2, default=str)


def _fmt(value: object) -> str:
    """Format a value for display in the table."""
    if value is None:
        return "—"
    return str(value)
