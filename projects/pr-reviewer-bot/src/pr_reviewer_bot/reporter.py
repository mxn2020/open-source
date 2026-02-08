"""Format review comments for output."""

from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table
from rich.text import Text

from pr_reviewer_bot.analyzer import ReviewComment, Severity

_SEVERITY_STYLES: dict[Severity, str] = {
    Severity.ERROR: "bold red",
    Severity.WARNING: "bold yellow",
    Severity.INFO: "bold cyan",
}

_SEVERITY_EMOJI: dict[Severity, str] = {
    Severity.ERROR: "🔴",
    Severity.WARNING: "🟡",
    Severity.INFO: "🔵",
}


def report_text(comments: list[ReviewComment]) -> str:
    """Render review comments as a Rich-formatted text table.

    Args:
        comments: Review comments to format.

    Returns:
        Formatted string suitable for terminal output.
    """
    if not comments:
        return "✅ No issues found."

    console = Console(record=True, width=120)

    table = Table(title="PR Review Results", show_lines=True)
    table.add_column("Severity", justify="center", width=10)
    table.add_column("File", style="green")
    table.add_column("Line", justify="right", width=6)
    table.add_column("Rule", style="dim")
    table.add_column("Message")

    for comment in comments:
        emoji = _SEVERITY_EMOJI[comment.severity]
        severity_text = Text(f"{emoji} {comment.severity.value}")
        severity_text.stylize(_SEVERITY_STYLES[comment.severity])
        line_str = str(comment.line) if comment.line > 0 else "-"
        table.add_row(severity_text, comment.file, line_str, comment.rule, comment.message)

    error_count = sum(1 for c in comments if c.severity == Severity.ERROR)
    warning_count = sum(1 for c in comments if c.severity == Severity.WARNING)
    info_count = sum(1 for c in comments if c.severity == Severity.INFO)

    console.print(table)
    console.print(
        f"\nSummary: {error_count} error(s), {warning_count} warning(s), {info_count} info(s)"
    )

    return console.export_text()


def report_json(comments: list[ReviewComment]) -> str:
    """Render review comments as JSON for CI integration.

    Args:
        comments: Review comments to format.

    Returns:
        A JSON string containing the list of comments plus a summary.
    """
    data = {
        "comments": [
            {
                "file": c.file,
                "line": c.line,
                "severity": c.severity.value,
                "message": c.message,
                "rule": c.rule,
            }
            for c in comments
        ],
        "summary": {
            "total": len(comments),
            "errors": sum(1 for c in comments if c.severity == Severity.ERROR),
            "warnings": sum(1 for c in comments if c.severity == Severity.WARNING),
            "infos": sum(1 for c in comments if c.severity == Severity.INFO),
        },
    }
    return json.dumps(data, indent=2)
