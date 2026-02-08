"""Command-line interface for model-output-evaluator."""

import json
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from model_output_evaluator.evaluator import evaluate
from model_output_evaluator.reporter import report_json, report_text

app = typer.Typer(
    name="model-eval",
    help="Evaluate and score model outputs against expected results.",
    add_completion=False,
)
console = Console()


def _load_json_strings(path: Path) -> list[str]:
    """Load a JSON file that contains an array of strings."""
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        console.print(f"[red]Error reading {path}: {e}[/red]")
        raise typer.Exit(code=2) from e

    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        console.print(f"[red]Error: {path} must contain a JSON array of strings.[/red]")
        raise typer.Exit(code=2)

    return data


@app.command()
def evaluate_cmd(
    predictions: Annotated[
        Path, typer.Option("--predictions", "-p", help="JSON file with predicted strings.")
    ],
    references: Annotated[
        Path, typer.Option("--references", "-r", help="JSON file with reference strings.")
    ],
    metrics: Annotated[
        Optional[str],
        typer.Option("--metrics", "-m", help="Comma-separated list of metrics to use."),
    ] = None,
    output_json: Annotated[
        bool, typer.Option("--json", help="Output results as JSON.")
    ] = False,
) -> None:
    """Evaluate model predictions against reference outputs."""
    preds = _load_json_strings(predictions)
    refs = _load_json_strings(references)

    metric_list = [m.strip() for m in metrics.split(",")] if metrics else None

    try:
        summary = evaluate(preds, refs, metric_list)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=2) from e

    if output_json:
        output = report_json(summary)
    else:
        output = report_text(summary)

    console.print(output) if not output_json else sys.stdout.write(output + "\n")


@app.command()
def compare(
    a: Annotated[
        Path, typer.Option("--a", help="JSON file with first set of predictions.")
    ],
    b: Annotated[
        Path, typer.Option("--b", help="JSON file with second set of predictions.")
    ],
    references: Annotated[
        Path, typer.Option("--references", "-r", help="JSON file with reference strings.")
    ],
    metrics: Annotated[
        Optional[str],
        typer.Option("--metrics", "-m", help="Comma-separated list of metrics to use."),
    ] = None,
    output_json: Annotated[
        bool, typer.Option("--json", help="Output results as JSON.")
    ] = False,
) -> None:
    """Compare two sets of predictions against the same references."""
    preds_a = _load_json_strings(a)
    preds_b = _load_json_strings(b)
    refs = _load_json_strings(references)

    metric_list = [m.strip() for m in metrics.split(",")] if metrics else None

    try:
        summary_a = evaluate(preds_a, refs, metric_list)
        summary_b = evaluate(preds_b, refs, metric_list)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=2) from e

    if output_json:
        data = {
            "model_a": json.loads(report_json(summary_a)),
            "model_b": json.loads(report_json(summary_b)),
        }
        sys.stdout.write(json.dumps(data, indent=2) + "\n")
    else:
        console.print("[bold blue]Model A Results[/bold blue]")
        console.print(report_text(summary_a))
        console.print()
        console.print("[bold green]Model B Results[/bold green]")
        console.print(report_text(summary_b))
