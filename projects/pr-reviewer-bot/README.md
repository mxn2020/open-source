# pr-reviewer-bot

A command-line tool that provides automated PR review suggestions by analyzing unified diffs. It detects common issues like debug statements, hardcoded secrets, TODO comments, and more using pattern-based rules — no AI or network access required.

## Features

- **Diff parsing**: Parses unified diff format (`git diff` output) into structured data.
- **Pattern-based analysis**: Detects six categories of issues:
  - Large file changes (>300 lines added)
  - TODO/FIXME/HACK comments in added lines
  - Debug/print statements (`console.log`, `print()`, `debugger`)
  - Hardcoded secrets (`API_KEY=`, `password=`, `token=` with literal values)
  - Long lines (>120 characters)
  - Trailing whitespace in added lines
- **Rich terminal output**: Colour-coded severity table with summary counts.
- **JSON output**: Structured output for CI pipeline integration.
- **Severity filtering**: Report only issues at or above a chosen severity level.
- **Stdin support**: Pipe `git diff` directly into the tool.

## Installation

```bash
cd projects/pr-reviewer-bot
pip install -e ".[dev]"
```

## Quick Start

Review a diff file:

```bash
pr-reviewer review changes.diff
```

Pipe from git:

```bash
git diff | pr-reviewer review -
```

JSON output for CI:

```bash
pr-reviewer review changes.diff --json
```

Filter by severity:

```bash
pr-reviewer review changes.diff --severity warning
```

## Exit Codes

| Code | Meaning          |
|------|------------------|
| 0    | No issues found  |
| 1    | Issues found     |
| 2    | Input error      |

## Analysis Rules

| Rule                  | Severity | Trigger                                        |
|-----------------------|----------|------------------------------------------------|
| `large-change`        | warning  | File has more than 300 added lines             |
| `todo-comment`        | info     | Added line contains TODO, FIXME, or HACK       |
| `debug-statement`     | warning  | Added line contains print(), console.log, etc. |
| `hardcoded-secret`    | error    | Added line matches secret-like patterns        |
| `long-line`           | info     | Added line exceeds 120 characters              |
| `trailing-whitespace` | info     | Added line has trailing whitespace              |

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

See [docs/development.md](docs/development.md) for the full development guide, [docs/cli.md](docs/cli.md) for CLI reference, and [docs/design.md](docs/design.md) for architecture details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
