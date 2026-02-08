# CLI Reference

## Commands

### `gfi scan`

Scan a project directory and generate good first issue suggestions.

```bash
gfi scan <directory> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `directory` | Path to the project directory to scan (required) |

**Options:**

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--max` | `-m` | int | 10 | Maximum number of issues to generate |
| `--extensions` | `-e` | str | None | Comma-separated file extensions (e.g., `.py,.ts,.js`) |
| `--json` | `-j` | flag | false | Output results as JSON |
| `--markdown` | `--md` | flag | false | Output results as Markdown |

**Examples:**

```bash
# Basic scan with Rich terminal output
gfi scan ./my-project

# Generate at most 5 issues as JSON
gfi scan ./my-project --max 5 --json

# Scan only Python files, output as Markdown
gfi scan ./my-project --extensions .py --markdown

# Save Markdown output to a file
gfi scan ./my-project --markdown > good-first-issues.md
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Issues generated successfully |
| 1 | No improvement opportunities found |
| 2 | Error (invalid directory, scan failure) |

### `gfi stats`

Show statistics about code improvement opportunities in a directory.

```bash
gfi stats <directory>
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `directory` | Path to the project directory to analyze (required) |

**Example output:**

```
Codebase Statistics

  Files with opportunities: 12
  Total opportunities:      27

  TODO/FIXME comments:      8
  Files without tests:      5
  Missing docstrings:       9
  Missing type hints:       5

  Easy issues:   17
  Medium issues: 10
```

### `gfi --version`

Print the current version of the tool and exit.

```bash
gfi --version
```
