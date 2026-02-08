"""Reporting utilities for evaluation results."""

import json

from rich.console import Console
from rich.table import Table

from model_output_evaluator.evaluator import EvalSummary


def report_text(summary: EvalSummary) -> str:
    """Generate a Rich-formatted text table of evaluation results.

    Shows per-item scores and average scores across all metric columns.
    """
    console = Console(record=True, width=120)

    table = Table(title="Evaluation Results", show_lines=True)
    table.add_column("#", style="dim", justify="right")
    table.add_column("Predicted", max_width=30, overflow="ellipsis")
    table.add_column("Expected", max_width=30, overflow="ellipsis")
    for metric in summary.metric_names:
        table.add_column(metric, justify="right")

    for i, result in enumerate(summary.results):
        row = [
            str(i + 1),
            result.predicted,
            result.expected,
        ]
        for metric in summary.metric_names:
            score = result.scores[metric]
            row.append(f"{score:.4f}")
        table.add_row(*row)

    avg_row = ["", "[bold]Average[/bold]", ""]
    for metric in summary.metric_names:
        score = summary.avg_scores[metric]
        avg_row.append(f"[bold]{score:.4f}[/bold]")
    table.add_row(*avg_row)

    console.print(table)
    return console.export_text()


def report_json(summary: EvalSummary) -> str:
    """Generate a JSON string of evaluation results."""
    data = {
        "results": [
            {
                "predicted": r.predicted,
                "expected": r.expected,
                "scores": r.scores,
            }
            for r in summary.results
        ],
        "avg_scores": summary.avg_scores,
        "metric_names": summary.metric_names,
    }
    return json.dumps(data, indent=2)
