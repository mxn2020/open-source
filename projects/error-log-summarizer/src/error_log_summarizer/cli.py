"""Command-line interface for error-log-summarizer."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from error_log_summarizer.categorizer import categorize_errors, summarize
from error_log_summarizer.parser import parse_log_file
from error_log_summarizer.reporter import (
    report_categories_json,
    report_categories_text,
    report_json,
    report_text,
)

app = typer.Typer(
    name="error-log-summarizer",
    help="Summarize and categorize error logs.",
    add_completion=False,
)

console = Console()


@app.command("summarize")
def summarize_cmd(
    logfile: Annotated[Path, typer.Argument(help="Path to the log file to analyze")],
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
    top: Annotated[int, typer.Option("--top", "-n", help="Number of top errors to show")] = 10,
) -> None:
    """Parse a log file and display an aggregated summary."""
    try:
        entries = parse_log_file(str(logfile))
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {logfile}")
        raise typer.Exit(code=2)
    except PermissionError:
        console.print(f"[red]Error:[/red] Permission denied: {logfile}")
        raise typer.Exit(code=2)

    if not entries:
        console.print("[yellow]No log entries found in the file.[/yellow]")
        raise typer.Exit(code=0)

    summary = summarize(entries, top=top)

    if output_json:
        console.print(report_json(summary))
    else:
        console.print(report_text(summary), highlight=False)

    if summary.error_count > 0:
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


@app.command("categorize")
def categorize_cmd(
    logfile: Annotated[Path, typer.Argument(help="Path to the log file to analyze")],
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Parse a log file and display errors grouped by category."""
    try:
        entries = parse_log_file(str(logfile))
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {logfile}")
        raise typer.Exit(code=2)
    except PermissionError:
        console.print(f"[red]Error:[/red] Permission denied: {logfile}")
        raise typer.Exit(code=2)

    categories = categorize_errors(entries)

    if output_json:
        console.print(report_categories_json(categories))
    else:
        console.print(report_categories_text(categories), highlight=False)

    if any(categories.values()):
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
