"""CLI interface for the Good First Issue Generator."""

import os
from typing import Optional

import typer
from rich.console import Console

from good_first_issue_generator import __version__
from good_first_issue_generator.generator import generate_issues
from good_first_issue_generator.reporter import report_json, report_markdown, report_text
from good_first_issue_generator.scanner import scan_directory

app = typer.Typer(
    name="gfi",
    help="Good First Issue Generator — analyze codebases and suggest starter issues.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print the version and exit."""
    if value:
        console.print(f"good-first-issue-generator {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Good First Issue Generator CLI."""


@app.command()
def scan(
    directory: str = typer.Argument(..., help="Path to the project directory to scan."),
    max_issues: int = typer.Option(
        10, "--max", "-m", help="Maximum number of issues to generate."
    ),
    extensions: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--extensions",
        "-e",
        help="Comma-separated file extensions to scan (e.g., '.py,.ts,.js').",
    ),
    output_json: bool = typer.Option(False, "--json", "-j", help="Output results as JSON."),
    output_markdown: bool = typer.Option(
        False, "--markdown", "--md", help="Output results as Markdown."
    ),
) -> None:
    """Scan a directory and generate good first issue suggestions."""
    if not os.path.isdir(directory):
        console.print(f"[red]Error: '{directory}' is not a valid directory.[/red]")
        raise typer.Exit(code=2)

    ext_list: list[str] | None = None
    if extensions:
        ext_list = [
            e.strip() if e.strip().startswith(".") else f".{e.strip()}"
            for e in extensions.split(",")
        ]

    try:
        opportunities = scan_directory(directory, extensions=ext_list)
    except Exception as exc:
        console.print(f"[red]Error scanning directory: {exc}[/red]")
        raise typer.Exit(code=2)

    if not opportunities:
        console.print("[yellow]No improvement opportunities found in the codebase.[/yellow]")
        raise typer.Exit(code=1)

    issues = generate_issues(opportunities, max_issues=max_issues)

    if not issues:
        console.print("[yellow]No issues could be generated from the opportunities.[/yellow]")
        raise typer.Exit(code=1)

    if output_json:
        typer.echo(report_json(issues))
    elif output_markdown:
        typer.echo(report_markdown(issues))
    else:
        typer.echo(report_text(issues))

    raise typer.Exit(code=0)


@app.command()
def stats(
    directory: str = typer.Argument(..., help="Path to the project directory to analyze."),
) -> None:
    """Show statistics about code improvement opportunities in a directory."""
    if not os.path.isdir(directory):
        console.print(f"[red]Error: '{directory}' is not a valid directory.[/red]")
        raise typer.Exit(code=2)

    try:
        opportunities = scan_directory(directory)
    except Exception as exc:
        console.print(f"[red]Error scanning directory: {exc}[/red]")
        raise typer.Exit(code=2)

    total_files = set()
    counts: dict[str, int] = {}
    for opp in opportunities:
        total_files.add(opp.file)
        counts[opp.type] = counts.get(opp.type, 0) + 1

    console.print("\n[bold green]Codebase Statistics[/bold green]\n")
    console.print(f"  Files with opportunities: [cyan]{len(total_files)}[/cyan]")
    console.print(f"  Total opportunities:      [cyan]{len(opportunities)}[/cyan]\n")

    type_labels = {
        "todo": "TODO/FIXME comments",
        "missing_test": "Files without tests",
        "missing_docstring": "Missing docstrings",
        "missing_type_hint": "Missing type hints",
    }

    for opp_type, label in type_labels.items():
        count = counts.get(opp_type, 0)
        color = "green" if count == 0 else "yellow"
        console.print(f"  {label + ':':<25} [{color}]{count}[/{color}]")

    easy = sum(1 for o in opportunities if o.difficulty == "easy")
    medium = sum(1 for o in opportunities if o.difficulty == "medium")
    console.print(f"\n  Easy issues:   [green]{easy}[/green]")
    console.print(f"  Medium issues: [yellow]{medium}[/yellow]\n")

    raise typer.Exit(code=0)
