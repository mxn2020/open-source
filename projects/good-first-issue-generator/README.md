# Good First Issue Generator

A Python CLI tool that analyzes codebases and generates well-formatted "good first issue"
suggestions for open source projects. It scans source files for common improvement opportunities
like TODO comments, missing tests, missing docstrings, and missing type hints, then produces
ready-to-use GitHub issue templates.

## Features

- **TODO/FIXME Scanner** — Finds `TODO`, `FIXME`, `HACK`, and `XXX` comments across your codebase
- **Missing Test Detection** — Identifies source files without corresponding test files
- **Docstring Checker** — Flags Python functions and classes missing docstrings
- **Type Hint Checker** — Detects Python functions missing return type annotations
- **Multiple Output Formats** — Rich terminal output, JSON, or Markdown
- **Configurable** — Filter by file extension, limit issue count

## Installation

```bash
cd projects/good-first-issue-generator
pip install -e ".[dev]"
```

## Quick Start

Scan a project directory and display suggested issues:

```bash
gfi scan /path/to/project
```

Output as JSON for automation:

```bash
gfi scan /path/to/project --json
```

Output as Markdown for GitHub:

```bash
gfi scan /path/to/project --markdown > issues.md
```

Show codebase statistics:

```bash
gfi stats /path/to/project
```

## CLI Reference

### `gfi scan <directory>`

Scan a directory and generate good first issue suggestions.

| Option | Short | Description | Default |
|---|---|---|---|
| `--max` | `-m` | Maximum number of issues to generate | 10 |
| `--extensions` | `-e` | Comma-separated file extensions (e.g., `.py,.ts`) | `.py,.ts,.js` |
| `--json` | `-j` | Output as JSON | false |
| `--markdown` | `--md` | Output as Markdown | false |

**Exit codes:**
- `0` — Issues generated successfully
- `1` — No opportunities found
- `2` — Error (invalid directory, scan failure)

### `gfi stats <directory>`

Show statistics about code improvement opportunities.

### `gfi --version`

Print the current version.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=good_first_issue_generator
```

Lint and format:

```bash
ruff check src/ tests/
black src/ tests/
```

## Project Structure

```
projects/good-first-issue-generator/
├── src/good_first_issue_generator/
│   ├── __init__.py         # Package version
│   ├── cli.py              # Typer CLI commands
│   ├── scanner.py          # Codebase scanning logic
│   ├── generator.py        # Issue template generation
│   └── reporter.py         # Output formatting (text, JSON, Markdown)
├── tests/
│   ├── test_scanner.py     # Scanner unit tests
│   ├── test_generator.py   # Generator unit tests
│   └── test_cli.py         # CLI integration tests
├── docs/                   # Documentation
└── examples/               # Example output
```

## How It Works

1. **Scan** — The scanner walks the project directory, skipping common non-source directories
   (`node_modules`, `__pycache__`, `.git`, etc.). For each source file, it searches for TODO
   comments, checks for missing docstrings and type hints in Python files, and identifies
   source files without corresponding test files.

2. **Generate** — Opportunities are deduplicated, sorted by difficulty (easy first), and
   converted into structured issue templates with titles, bodies, labels, and difficulty ratings.

3. **Report** — Issues are formatted for the chosen output: Rich-formatted terminal output,
   JSON for programmatic use, or Markdown suitable for pasting into GitHub issues.

## License

MIT License. See [LICENSE](LICENSE) for details.
