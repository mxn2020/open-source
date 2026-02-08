"""Command-line interface for dotenv-doctor."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from dotenv_doctor.parser import parse_file
from dotenv_doctor.reporter import report_json, report_text
from dotenv_doctor.validator import Severity, validate_env

app = typer.Typer(
    name="dotenv-doctor",
    help="Validate and diagnose .env files.",
    add_completion=False,
)
console = Console()


@app.command()
def check(
    envfile: Annotated[Path, typer.Argument(help="Path to the .env file to validate")],
    template: Annotated[
        Optional[Path], typer.Option("--template", "-t", help="Template file to compare against")
    ] = None,
    output_json: Annotated[
        bool, typer.Option("--json", "-j", help="Output results as JSON")
    ] = False,
) -> None:
    """Validate a .env file, optionally against a template."""
    if not envfile.is_file():
        console.print(f"[red]Error:[/red] file not found: {envfile}")
        raise typer.Exit(code=2)

    entries = parse_file(envfile)

    template_entries = None
    if template is not None:
        if not template.is_file():
            console.print(f"[red]Error:[/red] template file not found: {template}")
            raise typer.Exit(code=2)
        template_entries = parse_file(template)

    issues = validate_env(entries, template_entries)

    if output_json:
        console.print(report_json(issues), highlight=False)
    else:
        console.print(report_text(issues), highlight=False)

    if any(i.severity == Severity.ERROR for i in issues):
        raise typer.Exit(code=1)
    if issues:
        raise typer.Exit(code=0)


@app.command()
def compare(
    file1: Annotated[Path, typer.Argument(help="First .env file")],
    file2: Annotated[Path, typer.Argument(help="Second .env file")],
    output_json: Annotated[
        bool, typer.Option("--json", "-j", help="Output results as JSON")
    ] = False,
) -> None:
    """Compare two .env files and show differences."""
    for f in (file1, file2):
        if not f.is_file():
            console.print(f"[red]Error:[/red] file not found: {f}")
            raise typer.Exit(code=2)

    entries1 = parse_file(file1)
    entries2 = parse_file(file2)

    keys1 = {e.key: e.value for e in entries1}
    keys2 = {e.key: e.value for e in entries2}

    all_keys = sorted(set(keys1) | set(keys2))

    differences: list[dict[str, str]] = []
    for key in all_keys:
        in1 = key in keys1
        in2 = key in keys2
        if in1 and not in2:
            differences.append({"key": key, "status": "only in file1", "file1": keys1[key]})
        elif in2 and not in1:
            differences.append({"key": key, "status": "only in file2", "file2": keys2[key]})
        elif keys1[key] != keys2[key]:
            differences.append(
                {
                    "key": key,
                    "status": "different",
                    "file1": keys1[key],
                    "file2": keys2[key],
                }
            )

    if output_json:
        import json

        console.print(json.dumps(differences, indent=2), highlight=False)
    else:
        _print_compare_table(differences, file1, file2)

    if differences:
        raise typer.Exit(code=1)


def _print_compare_table(differences: list[dict[str, str]], file1: Path, file2: Path) -> None:
    from rich.table import Table

    if not differences:
        console.print("[green]Files are identical.[/green]")
        return

    table = Table(title=f"Comparing {file1} ↔ {file2}")
    table.add_column("Key", style="bold", width=30)
    table.add_column("Status", width=16)
    table.add_column(str(file1), width=30)
    table.add_column(str(file2), width=30)

    for diff in differences:
        status = diff["status"]
        style = {"only in file1": "yellow", "only in file2": "cyan", "different": "red"}.get(
            status, ""
        )
        table.add_row(
            diff["key"],
            f"[{style}]{status}[/{style}]",
            diff.get("file1", "-"),
            diff.get("file2", "-"),
        )

    console.print(table)
