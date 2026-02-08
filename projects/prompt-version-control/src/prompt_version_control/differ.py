"""Diff utility for comparing prompt versions."""

from __future__ import annotations

import difflib

from prompt_version_control.models import PromptVersion


def diff_versions(v1: PromptVersion, v2: PromptVersion) -> str:
    """Show a unified diff between two prompt versions.

    Args:
        v1: The first (older) prompt version.
        v2: The second (newer) prompt version.

    Returns:
        A string containing the unified diff output.
    """
    lines1 = v1.content.splitlines(keepends=True)
    lines2 = v2.content.splitlines(keepends=True)

    diff = difflib.unified_diff(
        lines1,
        lines2,
        fromfile=f"version {v1.version}",
        tofile=f"version {v2.version}",
        lineterm="",
    )
    return "\n".join(diff)
