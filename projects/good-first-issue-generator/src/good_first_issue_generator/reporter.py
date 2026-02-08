"""Reporter module for formatting issue templates into various output formats."""

import json

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from good_first_issue_generator.generator import IssueTemplate


def report_text(issues: list[IssueTemplate]) -> str:
    """Render issues as Rich-formatted text suitable for terminal display.

    Args:
        issues: List of IssueTemplate objects to format.

    Returns:
        A string containing the Rich-rendered output.
    """
    console = Console(record=True, width=100)

    if not issues:
        console.print("[yellow]No good first issues found.[/yellow]")
        return console.export_text()

    console.print(f"\n[bold green]Found {len(issues)} Good First Issue(s)[/bold green]\n")

    for i, issue in enumerate(issues, start=1):
        difficulty_color = "green" if issue.difficulty == "easy" else "yellow"
        label_str = ", ".join(issue.labels)

        header = Text()
        header.append(f"#{i} ", style="bold cyan")
        header.append(issue.title, style="bold")

        panel_content = Text()
        panel_content.append("Difficulty: ", style="dim")
        panel_content.append(f"{issue.difficulty}\n", style=difficulty_color)
        panel_content.append("Labels: ", style="dim")
        panel_content.append(f"{label_str}\n\n", style="magenta")

        for body_line in issue.body.split("\n")[:8]:
            panel_content.append(f"{body_line}\n")

        console.print(Panel(panel_content, title=header, border_style="blue", expand=False))

    return console.export_text()


def report_json(issues: list[IssueTemplate]) -> str:
    """Render issues as a JSON string.

    Args:
        issues: List of IssueTemplate objects to format.

    Returns:
        A JSON string representation of the issues.
    """
    data = [
        {
            "title": issue.title,
            "body": issue.body,
            "labels": issue.labels,
            "difficulty": issue.difficulty,
        }
        for issue in issues
    ]
    return json.dumps(data, indent=2)


def report_markdown(issues: list[IssueTemplate]) -> str:
    """Render issues as Markdown suitable for GitHub.

    Args:
        issues: List of IssueTemplate objects to format.

    Returns:
        A Markdown string with all issues formatted as sections.
    """
    if not issues:
        return "# Good First Issues\n\nNo issues found.\n"

    parts: list[str] = [f"# Good First Issues\n\nFound **{len(issues)}** issue(s).\n"]

    for i, issue in enumerate(issues, start=1):
        label_badges = " ".join(f"`{label}`" for label in issue.labels)
        parts.append(
            f"---\n\n"
            f"## {i}. {issue.title}\n\n"
            f"**Difficulty:** {issue.difficulty} | **Labels:** {label_badges}\n\n"
            f"{issue.body}\n"
        )

    return "\n".join(parts)
