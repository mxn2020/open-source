"""Log file parser with auto-detection of common log formats."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass
class LogEntry:
    """A single parsed log entry."""

    timestamp: str
    level: str
    message: str
    source: str = ""


# Syslog: "Jan 15 10:30:00 myhost myservice[1234]: some message"
_SYSLOG_RE = re.compile(
    r"^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<hostname>\S+)\s+"
    r"(?P<service>[^\[:]+)(?:\[\d+\])?:\s+"
    r"(?P<message>.+)$"
)

# Apache/Nginx: "[Wed Jan 15 10:30:00 2024] [error] something failed"
_APACHE_RE = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s+" r"\[(?P<level>[^\]]+)\]\s+" r"(?P<message>.+)$"
)

# Generic: "2024-01-15 10:30:00 ERROR something failed"
_GENERIC_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\s+"
    r"(?P<message>.+)$",
    re.IGNORECASE,
)

_LEVEL_NORMALIZE = {
    "warn": "WARNING",
    "fatal": "CRITICAL",
    "emerg": "CRITICAL",
    "crit": "CRITICAL",
    "err": "ERROR",
    "notice": "INFO",
}

# Syslog messages that imply error-level severity
_SYSLOG_ERROR_KEYWORDS = [
    "error",
    "fail",
    "critical",
    "fatal",
    "segfault",
    "panic",
    "denied",
    "refused",
]
_SYSLOG_WARNING_KEYWORDS = ["warn", "timeout", "retry"]


def _normalize_level(level: str) -> str:
    """Normalize log level strings to standard names."""
    lower = level.strip().lower()
    if lower in _LEVEL_NORMALIZE:
        return _LEVEL_NORMALIZE[lower]
    for standard in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        if lower == standard.lower():
            return standard
    return level.upper()


def _infer_syslog_level(message: str) -> str:
    """Infer a severity level from a syslog message by keyword matching."""
    lower = message.lower()
    for kw in _SYSLOG_ERROR_KEYWORDS:
        if kw in lower:
            return "ERROR"
    for kw in _SYSLOG_WARNING_KEYWORDS:
        if kw in lower:
            return "WARNING"
    return "INFO"


def _parse_line(line: str) -> LogEntry | None:
    """Attempt to parse a single log line in any supported format."""
    stripped = line.strip()
    if not stripped:
        return None

    # Try JSON first
    if stripped.startswith("{"):
        try:
            obj = json.loads(stripped)
            if "level" in obj and "message" in obj:
                return LogEntry(
                    timestamp=str(obj.get("timestamp", "")),
                    level=_normalize_level(str(obj["level"])),
                    message=str(obj["message"]),
                    source=str(obj.get("source", "")),
                )
        except (json.JSONDecodeError, KeyError):
            pass

    # Try generic format (most specific timestamp pattern)
    m = _GENERIC_RE.match(stripped)
    if m:
        return LogEntry(
            timestamp=m.group("timestamp"),
            level=_normalize_level(m.group("level")),
            message=m.group("message"),
        )

    # Try Apache/Nginx format
    m = _APACHE_RE.match(stripped)
    if m:
        return LogEntry(
            timestamp=m.group("timestamp"),
            level=_normalize_level(m.group("level")),
            message=m.group("message"),
        )

    # Try syslog format
    m = _SYSLOG_RE.match(stripped)
    if m:
        message = m.group("message")
        return LogEntry(
            timestamp=m.group("timestamp"),
            level=_infer_syslog_level(message),
            message=message,
            source=m.group("service").strip(),
        )

    return None


def parse_log_file(path: str) -> list[LogEntry]:
    """Parse a log file, auto-detecting the format.

    Reads every line and attempts to parse it using all supported formats.
    Lines that cannot be parsed are silently skipped.

    Args:
        path: Filesystem path to the log file.

    Returns:
        A list of parsed LogEntry objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    entries: list[LogEntry] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            entry = _parse_line(line)
            if entry is not None:
                entries.append(entry)
    return entries
