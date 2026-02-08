"""Categorize and summarize parsed log entries."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from error_log_summarizer.parser import LogEntry

# Keyword patterns mapped to category names
_CATEGORY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ConnectionError", re.compile(r"connect|connection|refused|reset|unreachable", re.I)),
    ("TimeoutError", re.compile(r"timeout|timed?\s*out", re.I)),
    ("FileNotFound", re.compile(r"file\s*not\s*found|no\s*such\s*file|enoent", re.I)),
    ("PermissionError", re.compile(r"permission|denied|forbidden|access\s*denied", re.I)),
    ("MemoryError", re.compile(r"memory|out\s*of\s*memory|oom|heap", re.I)),
    ("SyntaxError", re.compile(r"syntax|parse\s*error|unexpected\s*token", re.I)),
]


@dataclass
class Summary:
    """Aggregated summary of log entries."""

    total_entries: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    categories: dict[str, int] = field(default_factory=dict)
    top_errors: list[tuple[str, int]] = field(default_factory=list)


def _classify_message(message: str) -> str:
    """Return the category name for a log message based on keyword matching."""
    for name, pattern in _CATEGORY_PATTERNS:
        if pattern.search(message):
            return name
    return "Generic"


def categorize_errors(entries: list[LogEntry]) -> dict[str, list[LogEntry]]:
    """Group log entries by error category.

    Only entries with level ERROR or CRITICAL are categorized.

    Args:
        entries: Parsed log entries.

    Returns:
        A dict mapping category names to lists of matching LogEntry objects.
    """
    groups: dict[str, list[LogEntry]] = {}
    for entry in entries:
        if entry.level in ("ERROR", "CRITICAL"):
            cat = _classify_message(entry.message)
            groups.setdefault(cat, []).append(entry)
    return groups


_NORMALIZE_RE = re.compile(r"\d[\d./:_-]*\w*")


def _normalize_message(message: str) -> str:
    """Collapse numbers/timestamps so similar messages group together."""
    return _NORMALIZE_RE.sub("<N>", message).strip()


def summarize(entries: list[LogEntry], top: int = 10) -> Summary:
    """Produce an aggregated summary of all log entries.

    Args:
        entries: Parsed log entries.
        top: Number of most-frequent error messages to include.

    Returns:
        A Summary dataclass with counts, categories, and top errors.
    """
    summary = Summary(total_entries=len(entries))

    error_messages: list[str] = []
    for entry in entries:
        if entry.level in ("ERROR", "CRITICAL"):
            summary.error_count += 1
            error_messages.append(entry.message)
        elif entry.level == "WARNING":
            summary.warning_count += 1
        else:
            summary.info_count += 1

    # Category counts
    categories = categorize_errors(entries)
    summary.categories = {cat: len(items) for cat, items in categories.items()}

    # Top errors by normalized message frequency
    normalized = [_normalize_message(m) for m in error_messages]
    counter = Counter(normalized)
    summary.top_errors = counter.most_common(top)

    return summary
