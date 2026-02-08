"""CLI entry point for pr-reviewer-bot."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from pr_reviewer_bot.analyzer import Severity, analyze_diff
from pr_reviewer_bot.diff_parser import parse_diff
from pr_reviewer_bot.reporter import report_json, report_text

app = typer.Typer(
    name="pr-reviewer",
    help="Automated PR review suggestions by analyzing diffs.",
    add_completion=False,
)
console = Console(stderr=True)


@app.command()
def review(
    diff_file: Optional[str] = typer.Argument(  # noqa: UP007
        None,
        help="Path to a diff file, or '-' to read from stdin. Reads stdin if omitted.",
    ),
    output_json: bool = typer.Option(
        False,
        "--json",
        help="Output results as JSON for CI integration.",
    ),
    severity: str = typer.Option(
        "info",
        "--severity",
        help="Minimum severity to report: info, warning, or error.",
    ),
) -> None:
    """Analyze a unified diff and output review comments."""
    severity_order = {"info": 0, "warning": 1, "error": 2}
    severity_lower = severity.lower()
    if severity_lower not in severity_order:
        console.print(f"[red]Invalid severity: {severity}. Use info, warning, or error.[/red]")
        raise SystemExit(2)

    min_severity = severity_order[severity_lower]

    try:
        if diff_file is None or diff_file == "-":
            diff_text = sys.stdin.read()
        else:
            path = Path(diff_file)
            if not path.exists():
                console.print(f"[red]File not found: {diff_file}[/red]")
                raise SystemExit(2)
            diff_text = path.read_text()
    except KeyboardInterrupt:
        raise SystemExit(2)
    except SystemExit:
        raise
    except Exception as exc:
        console.print(f"[red]Error reading input: {exc}[/red]")
        raise SystemExit(2)

    if not diff_text.strip():
        console.print("[yellow]No diff content provided.[/yellow]")
        raise SystemExit(0)

    files = parse_diff(diff_text)
    comments = analyze_diff(files)

    # Filter by minimum severity
    comments = [c for c in comments if severity_order[c.severity.value] >= min_severity]

    if output_json:
        typer.echo(report_json(comments))
    else:
        typer.echo(report_text(comments))

    has_errors = any(c.severity == Severity.ERROR for c in comments)
    has_warnings = any(c.severity == Severity.WARNING for c in comments)

    if has_errors or has_warnings:
        raise SystemExit(1)
    raise SystemExit(0)
