"""Parse unified diff format (git diff output) into structured data."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class DiffHunk:
    """Represents a single hunk in a unified diff."""

    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)


@dataclass
class DiffFile:
    """Represents a single file's changes in a diff."""

    filename: str
    added_lines: list[tuple[int, str]] = field(default_factory=list)
    removed_lines: list[tuple[int, str]] = field(default_factory=list)
    hunks: list[DiffHunk] = field(default_factory=list)


_HUNK_HEADER_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def parse_diff(diff_text: str) -> list[DiffFile]:
    """Parse a complete unified diff into structured data.

    Args:
        diff_text: Raw unified diff text (e.g. output of ``git diff``).

    Returns:
        A list of :class:`DiffFile` objects, one per file in the diff.
    """
    files: list[DiffFile] = []
    current_file: DiffFile | None = None
    current_hunk: DiffHunk | None = None
    new_line_num = 0
    old_line_num = 0

    for raw_line in diff_text.splitlines():
        # Detect file header
        if raw_line.startswith("diff --git"):
            current_hunk = None
            continue

        if raw_line.startswith("+++ b/") or raw_line.startswith("+++ "):
            filename = raw_line.removeprefix("+++ b/").removeprefix("+++ ")
            current_file = DiffFile(filename=filename)
            files.append(current_file)
            current_hunk = None
            continue

        if raw_line.startswith("--- "):
            continue

        # Detect hunk header
        hunk_match = _HUNK_HEADER_RE.match(raw_line)
        if hunk_match and current_file is not None:
            old_start = int(hunk_match.group(1))
            old_count = int(hunk_match.group(2)) if hunk_match.group(2) else 1
            new_start = int(hunk_match.group(3))
            new_count = int(hunk_match.group(4)) if hunk_match.group(4) else 1
            current_hunk = DiffHunk(
                old_start=old_start,
                old_count=old_count,
                new_start=new_start,
                new_count=new_count,
            )
            current_file.hunks.append(current_hunk)
            old_line_num = old_start
            new_line_num = new_start
            continue

        if current_hunk is None or current_file is None:
            continue

        current_hunk.lines.append(raw_line)

        if raw_line.startswith("+"):
            content = raw_line[1:]
            current_file.added_lines.append((new_line_num, content))
            new_line_num += 1
        elif raw_line.startswith("-"):
            content = raw_line[1:]
            current_file.removed_lines.append((old_line_num, content))
            old_line_num += 1
        else:
            # Context line
            old_line_num += 1
            new_line_num += 1

    return files
