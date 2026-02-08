"""Format validation issues for human or machine consumption."""

from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table

from dotenv_doctor.validator import Issue, Severity

_SEVERITY_STYLES = {
    Severity.ERROR: "bold red",
    Severity.WARNING: "yellow",
    Severity.INFO: "cyan",
}


def report_text(issues: list[Issue]) -> str:
    """Return a Rich-formatted table of issues as a string."""
    if not issues:
        return "[green]No issues found.[/green]"

    console = Console(record=True, width=120)
    table = Table(title="dotenv-doctor report", show_lines=False)
    table.add_column("Severity", style="bold", width=10)
    table.add_column("Line", justify="right", width=6)
    table.add_column("Key", width=30)
    table.add_column("Message")

    for issue in issues:
        style = _SEVERITY_STYLES.get(issue.severity, "")
        table.add_row(
            f"[{style}]{issue.severity.value}[/{style}]",
            str(issue.line_number) if issue.line_number else "-",
            issue.key,
            issue.message,
        )

    console.print(table)
    return console.export_text()


def report_json(issues: list[Issue]) -> str:
    """Return issues as a JSON string."""
    data = [
        {
            "key": issue.key,
            "line_number": issue.line_number,
            "severity": issue.severity.value,
            "message": issue.message,
        }
        for issue in issues
    ]
    return json.dumps(data, indent=2)
