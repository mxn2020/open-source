"""Output formatters for log summaries."""

from __future__ import annotations

import json as _json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from error_log_summarizer.categorizer import Summary
from error_log_summarizer.parser import LogEntry


def report_text(summary: Summary) -> str:
    """Render a human-readable summary using Rich tables and panels.

    Args:
        summary: The aggregated log summary.

    Returns:
        A string containing the rendered Rich output.
    """
    console = Console(record=True, width=100)

    # Overview panel
    overview = (
        f"[bold]Total entries:[/bold] {summary.total_entries}\n"
        f"[red]Errors:[/red] {summary.error_count}\n"
        f"[yellow]Warnings:[/yellow] {summary.warning_count}\n"
        f"[green]Info:[/green] {summary.info_count}"
    )
    console.print(Panel(overview, title="Log Summary", border_style="blue"))

    # Categories table
    if summary.categories:
        cat_table = Table(title="Error Categories")
        cat_table.add_column("Category", style="cyan")
        cat_table.add_column("Count", justify="right", style="red")
        for cat, count in sorted(summary.categories.items(), key=lambda x: -x[1]):
            cat_table.add_row(cat, str(count))
        console.print(cat_table)

    # Top errors table
    if summary.top_errors:
        err_table = Table(title="Top Error Messages")
        err_table.add_column("Message", style="white", no_wrap=False)
        err_table.add_column("Count", justify="right", style="red")
        for msg, count in summary.top_errors:
            err_table.add_row(msg, str(count))
        console.print(err_table)

    return console.export_text()


def report_json(summary: Summary) -> str:
    """Render the summary as a JSON string.

    Args:
        summary: The aggregated log summary.

    Returns:
        A pretty-printed JSON string.
    """
    data = {
        "total_entries": summary.total_entries,
        "error_count": summary.error_count,
        "warning_count": summary.warning_count,
        "info_count": summary.info_count,
        "categories": summary.categories,
        "top_errors": [{"message": m, "count": c} for m, c in summary.top_errors],
    }
    return _json.dumps(data, indent=2)


def report_categories_text(categories: dict[str, list[LogEntry]]) -> str:
    """Render categorized errors as Rich text.

    Args:
        categories: Mapping of category name to list of log entries.

    Returns:
        A string containing the rendered Rich output.
    """
    console = Console(record=True, width=100)

    if not categories:
        console.print("[green]No errors found.[/green]")
        return console.export_text()

    for cat, entries in sorted(categories.items(), key=lambda x: -len(x[1])):
        table = Table(title=f"{cat} ({len(entries)})")
        table.add_column("Timestamp", style="dim")
        table.add_column("Message", style="white", no_wrap=False)
        for entry in entries:
            table.add_row(entry.timestamp, entry.message)
        console.print(table)

    return console.export_text()


def report_categories_json(categories: dict[str, list[LogEntry]]) -> str:
    """Render categorized errors as JSON.

    Args:
        categories: Mapping of category name to list of log entries.

    Returns:
        A pretty-printed JSON string.
    """
    data = {
        cat: [
            {
                "timestamp": e.timestamp,
                "level": e.level,
                "message": e.message,
                "source": e.source,
            }
            for e in entries
        ]
        for cat, entries in categories.items()
    }
    return _json.dumps(data, indent=2)
