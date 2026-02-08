"""Parse .env files into structured entries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EnvEntry:
    """A single parsed environment variable entry."""

    key: str
    value: str
    line_number: int
    raw_line: str


_EXPORT_PREFIX = re.compile(r"^export\s+")


def parse_line(line: str, line_number: int) -> EnvEntry | None:
    """Parse a single .env line into an EnvEntry, or None if not a variable definition."""
    stripped = line.strip()

    # Skip empty lines and comments
    if not stripped or stripped.startswith("#"):
        return None

    # Remove optional 'export' prefix
    stripped = _EXPORT_PREFIX.sub("", stripped)

    # Must contain '=' to be a valid assignment
    if "=" not in stripped:
        return None

    key, _, raw_value = stripped.partition("=")
    key = key.strip()

    if not key:
        return None

    value = _parse_value(raw_value)
    return EnvEntry(key=key, value=value, line_number=line_number, raw_line=line)


def _parse_value(raw: str) -> str:
    """Extract the value, handling quotes and inline comments."""
    raw = raw.strip()

    if not raw:
        return ""

    # Double-quoted value
    if raw.startswith('"'):
        end = raw.find('"', 1)
        if end != -1:
            return raw[1:end]
        # No closing quote — take everything after the opening quote
        return raw[1:]

    # Single-quoted value
    if raw.startswith("'"):
        end = raw.find("'", 1)
        if end != -1:
            return raw[1:end]
        return raw[1:]

    # Unquoted value — strip inline comments
    if " #" in raw:
        raw = raw[: raw.index(" #")]

    return raw.strip()


def parse_file(path: str | Path) -> list[EnvEntry]:
    """Parse a .env file and return a list of EnvEntry objects."""
    path = Path(path)
    entries: list[EnvEntry] = []
    with path.open(encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            entry = parse_line(line, line_number)
            if entry is not None:
                entries.append(entry)
    return entries
