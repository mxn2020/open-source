# Design Decisions

This document captures the key design decisions behind dotenv-doctor.

## Pipeline Architecture

The tool follows a three-stage pipeline: **parse → validate → report**.

Each stage is a pure function operating on simple data classes (`EnvEntry`, `Issue`). This makes every stage independently testable and composable.

## Data Classes Over Dictionaries

`EnvEntry` and `Issue` are Python `dataclass` types rather than plain dictionaries. This provides:

- Type safety and IDE autocompletion.
- Clear field documentation.
- Immutability by convention.

## Severity Levels

Three severity levels were chosen to match common linting conventions:

| Level | Meaning | Example |
|-------|---------|---------|
| `error` | Must be fixed; likely to cause failures | Missing required key |
| `warning` | Suspicious but may be intentional | Duplicate key, empty value |
| `info` | Informational; no action required | Extra key not in template |

## Template Comparison

Rather than inventing a schema language, dotenv-doctor uses an existing `.env` file (typically `.env.example`) as the template. The template's *keys* define the contract; the template's *values* are ignored during validation.

## No Multiline Support

Multiline values (using `\n` escapes or heredoc-style syntax) are deliberately not supported in v0.1. The `.env` format has no formal specification, and multiline handling varies across implementations. This avoids surprising behavior and keeps the parser simple.

## CLI Framework

[Typer](https://typer.tiangolo.com/) was chosen for the CLI because:

- It generates help text and argument parsing from type annotations.
- It integrates naturally with [Rich](https://rich.readthedocs.io/) for colored output.
- It has minimal boilerplate compared to argparse or click.

## Exit Codes

Exit codes follow Unix conventions:

- `0` — success (no errors).
- `1` — validation errors found.
- `2` — runtime error (e.g., file not found).

This allows dotenv-doctor to be used in CI pipelines with standard shell conditionals.
