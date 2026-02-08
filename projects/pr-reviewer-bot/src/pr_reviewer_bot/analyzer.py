"""Analyze parsed diffs and produce review comments."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from pr_reviewer_bot.diff_parser import DiffFile


class Severity(str, Enum):
    """Severity levels for review comments."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ReviewComment:
    """A single review comment attached to a file and line."""

    file: str
    line: int
    severity: Severity
    message: str
    rule: str


_SECRET_PATTERN = re.compile(
    r"(?:api_key|apikey|password|passwd|secret|token)" r"\s*[=:]\s*[\"']?[A-Za-z0-9+/=_\-]{8,}",
    re.IGNORECASE,
)

_DEBUG_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bconsole\.(log|debug|info|warn|error)\s*\("), "console.log statement"),
    (re.compile(r"\bprint\s*\("), "print() statement"),
    (re.compile(r"\bdebugger\b"), "debugger statement"),
]

_TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK)\b", re.IGNORECASE)

_MAX_LINE_LENGTH = 120
_LARGE_CHANGE_THRESHOLD = 300


def analyze_diff(files: list[DiffFile]) -> list[ReviewComment]:
    """Analyze parsed diff files and return review comments.

    Applies pattern-based rules to detect common issues in added lines.

    Args:
        files: Parsed diff files from :func:`pr_reviewer_bot.diff_parser.parse_diff`.

    Returns:
        A list of :class:`ReviewComment` instances.
    """
    comments: list[ReviewComment] = []

    for diff_file in files:
        # Large file change check
        if len(diff_file.added_lines) > _LARGE_CHANGE_THRESHOLD:
            comments.append(
                ReviewComment(
                    file=diff_file.filename,
                    line=0,
                    severity=Severity.WARNING,
                    message=(
                        f"Large change detected: {len(diff_file.added_lines)} lines added. "
                        "Consider breaking into smaller PRs."
                    ),
                    rule="large-change",
                )
            )

        for line_num, content in diff_file.added_lines:
            # Hardcoded secrets
            if _SECRET_PATTERN.search(content):
                comments.append(
                    ReviewComment(
                        file=diff_file.filename,
                        line=line_num,
                        severity=Severity.ERROR,
                        message="Possible hardcoded secret detected.",
                        rule="hardcoded-secret",
                    )
                )

            # TODO/FIXME/HACK comments
            if _TODO_PATTERN.search(content):
                match = _TODO_PATTERN.search(content)
                tag = match.group(1).upper() if match else "TODO"
                comments.append(
                    ReviewComment(
                        file=diff_file.filename,
                        line=line_num,
                        severity=Severity.INFO,
                        message=f"{tag} comment found.",
                        rule="todo-comment",
                    )
                )

            # Debug/print statements
            for pattern, description in _DEBUG_PATTERNS:
                if pattern.search(content):
                    comments.append(
                        ReviewComment(
                            file=diff_file.filename,
                            line=line_num,
                            severity=Severity.WARNING,
                            message=f"Debug statement found: {description}.",
                            rule="debug-statement",
                        )
                    )
                    break

            # Long lines
            if len(content) > _MAX_LINE_LENGTH:
                comments.append(
                    ReviewComment(
                        file=diff_file.filename,
                        line=line_num,
                        severity=Severity.INFO,
                        message=f"Line exceeds {_MAX_LINE_LENGTH} characters ({len(content)}).",
                        rule="long-line",
                    )
                )

            # Trailing whitespace
            if content != content.rstrip():
                comments.append(
                    ReviewComment(
                        file=diff_file.filename,
                        line=line_num,
                        severity=Severity.INFO,
                        message="Trailing whitespace detected.",
                        rule="trailing-whitespace",
                    )
                )

    return comments
