"""CLI interface for config-drift-detector powered by Typer."""

from __future__ import annotations

from typing import Annotated, Optional

import typer
from rich.console import Console

from config_drift_detector import __version__
from config_drift_detector.comparator import compare_configs, filter_by_tags
from config_drift_detector.parsers import parse_file
from config_drift_detector.reporter import report_json, report_text

app = typer.Typer(
    name="drift",
    help="Detect configuration drift between two files.",
    add_completion=False,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"config-drift-detector {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", help="Show version and exit.", callback=_version_callback, is_eager=True),
    ] = None,
) -> None:
    """Config Drift Detector — find differences between configuration sources."""


@app.command()
def check(
    a: Annotated[str, typer.Option("--a", help="Path to the first (baseline) config file.")],
    b: Annotated[str, typer.Option("--b", help="Path to the second (target) config file.")],
    output_json: Annotated[bool, typer.Option("--json", help="Output results as JSON.")] = False,
    tags: Annotated[Optional[str], typer.Option("--tags", help="Comma-separated top-level keys to compare.")] = None,
) -> None:
    """Compare two configuration files and report any drift."""
    try:
        config_a = parse_file(a)
        config_b = parse_file(b)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        config_a, config_b = filter_by_tags(config_a, config_b, tag_list)

    drifts = compare_configs(config_a, config_b)

    if not drifts:
        if output_json:
            console.print("[]")
        else:
            console.print("[green]No configuration drift detected.[/green]")
        raise typer.Exit(code=0)

    if output_json:
        console.print(report_json(drifts))
    else:
        console.print(report_text(drifts))

    raise typer.Exit(code=1)
