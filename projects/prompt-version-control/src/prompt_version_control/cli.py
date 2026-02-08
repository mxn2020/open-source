"""CLI interface for prompt version control."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from prompt_version_control.differ import diff_versions
from prompt_version_control.store import PromptStore

app = typer.Typer(
    name="pv",
    help="Prompt Version Control — version control for LLM prompts.",
    add_completion=False,
)
console = Console()

# Exit codes
EXIT_SUCCESS = 0
EXIT_NOT_FOUND = 1
EXIT_ERROR = 2


def _get_store() -> PromptStore:
    return PromptStore()


def _print_version_json(version, name: str | None = None) -> None:
    data = version.to_dict()
    if name:
        data["name"] = name
    console.print_json(json.dumps(data))


@app.command()
def save(
    name: Annotated[str, typer.Argument(help="Name of the prompt")],
    content: Annotated[Optional[str], typer.Option("--content", "-c", help="Prompt content")] = None,
    file: Annotated[Optional[Path], typer.Option("--file", "-f", help="Read content from file")] = None,
    meta: Annotated[Optional[list[str]], typer.Option("--meta", "-m", help="Metadata as key=value")] = None,
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Save a new version of a prompt."""
    if file and content:
        console.print("[red]Error:[/red] Provide either --content or --file, not both.")
        raise typer.Exit(code=EXIT_ERROR)

    if file:
        if not file.exists():
            console.print(f"[red]Error:[/red] File not found: {file}")
            raise typer.Exit(code=EXIT_ERROR)
        content = file.read_text()
    elif content is None:
        console.print("[red]Error:[/red] Provide --content or --file.")
        raise typer.Exit(code=EXIT_ERROR)

    metadata: dict = {}
    if meta:
        for item in meta:
            if "=" not in item:
                console.print(f"[red]Error:[/red] Invalid metadata format: {item} (use key=value)")
                raise typer.Exit(code=EXIT_ERROR)
            key, value = item.split("=", 1)
            metadata[key] = value

    store = _get_store()
    version = store.save(name, content, metadata)
    store.close()

    if output_json:
        _print_version_json(version, name=name)
    else:
        console.print(f"[green]Saved[/green] {name} version [bold]{version.version}[/bold]")


@app.command()
def get(
    name: Annotated[str, typer.Argument(help="Name of the prompt")],
    version: Annotated[Optional[str], typer.Option("--version", "-v", help="Version number")] = None,
    tag: Annotated[Optional[str], typer.Option("--tag", "-t", help="Tag name")] = None,
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Get a prompt version."""
    store = _get_store()

    if tag:
        result = store.get_by_tag(name, tag)
    else:
        result = store.get(name, version)

    store.close()

    if result is None:
        console.print(f"[yellow]Not found:[/yellow] {name}" + (f" version {version}" if version else "") + (f" tag {tag}" if tag else ""))
        raise typer.Exit(code=EXIT_NOT_FOUND)

    if output_json:
        _print_version_json(result, name=name)
    else:
        console.print(f"[bold]{name}[/bold] v{result.version}")
        console.print(f"Created: {result.created_at}")
        if result.metadata:
            console.print(f"Metadata: {result.metadata}")
        console.print()
        console.print(result.content)


@app.command("list")
def list_cmd(
    name: Annotated[Optional[str], typer.Option("--name", "-n", help="List versions of a specific prompt")] = None,
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """List prompts or versions of a specific prompt."""
    store = _get_store()

    if name:
        versions = store.list_versions(name)
        store.close()

        if not versions:
            console.print(f"[yellow]No versions found for:[/yellow] {name}")
            raise typer.Exit(code=EXIT_NOT_FOUND)

        if output_json:
            data = [v.to_dict() for v in versions]
            console.print_json(json.dumps(data))
        else:
            table = Table(title=f"Versions of '{name}'")
            table.add_column("Version", style="bold")
            table.add_column("Created At")
            table.add_column("Parent")
            table.add_column("Metadata")
            for v in versions:
                table.add_row(
                    v.version,
                    v.created_at,
                    v.parent_version or "-",
                    json.dumps(v.metadata) if v.metadata else "-",
                )
            console.print(table)
    else:
        prompts = store.list_prompts()
        store.close()

        if not prompts:
            console.print("[yellow]No prompts found.[/yellow]")
            raise typer.Exit(code=EXIT_NOT_FOUND)

        if output_json:
            console.print_json(json.dumps(prompts))
        else:
            table = Table(title="Prompts")
            table.add_column("Name", style="bold")
            for p in prompts:
                table.add_row(p)
            console.print(table)


@app.command()
def tag(
    name: Annotated[str, typer.Argument(help="Name of the prompt")],
    version: Annotated[str, typer.Argument(help="Version number to tag")],
    tag_name: Annotated[str, typer.Argument(help="Tag name")],
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Tag a specific version of a prompt."""
    store = _get_store()
    try:
        store.tag(name, version, tag_name)
    except ValueError as e:
        store.close()
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=EXIT_NOT_FOUND)

    store.close()

    if output_json:
        console.print_json(json.dumps({"name": name, "version": version, "tag": tag_name}))
    else:
        console.print(
            f"[green]Tagged[/green] {name} v{version} as [bold]{tag_name}[/bold]"
        )


@app.command()
def diff(
    name: Annotated[str, typer.Argument(help="Name of the prompt")],
    v1: Annotated[str, typer.Argument(help="First version")],
    v2: Annotated[str, typer.Argument(help="Second version")],
) -> None:
    """Show diff between two versions of a prompt."""
    store = _get_store()
    version1 = store.get(name, v1)
    version2 = store.get(name, v2)
    store.close()

    if version1 is None:
        console.print(f"[yellow]Not found:[/yellow] {name} version {v1}")
        raise typer.Exit(code=EXIT_NOT_FOUND)
    if version2 is None:
        console.print(f"[yellow]Not found:[/yellow] {name} version {v2}")
        raise typer.Exit(code=EXIT_NOT_FOUND)

    result = diff_versions(version1, version2)
    if result:
        console.print(result)
    else:
        console.print("[green]No differences found.[/green]")


@app.command()
def delete(
    name: Annotated[str, typer.Argument(help="Name of the prompt to delete")],
    output_json: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
) -> None:
    """Delete all versions of a prompt."""
    store = _get_store()
    deleted = store.delete(name)
    store.close()

    if not deleted:
        console.print(f"[yellow]Not found:[/yellow] {name}")
        raise typer.Exit(code=EXIT_NOT_FOUND)

    if output_json:
        console.print_json(json.dumps({"deleted": name}))
    else:
        console.print(f"[green]Deleted[/green] {name}")


if __name__ == "__main__":
    app()
