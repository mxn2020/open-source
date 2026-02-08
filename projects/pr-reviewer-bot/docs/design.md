# Design

This document describes the architecture and design decisions behind pr-reviewer-bot.

## Overview

pr-reviewer-bot is a command-line tool that analyzes unified diffs (e.g., from `git diff`) and produces review comments based on pattern-matching rules. It is designed to run locally or in CI pipelines without requiring network access or AI services.

## Architecture

The tool follows a three-stage pipeline:

```
Diff Text → Parser → Analyzer → Reporter
```

### Stage 1: Parsing (`diff_parser.py`)

The parser converts raw unified diff text into structured `DiffFile` and `DiffHunk` dataclasses. It handles:

- `diff --git` file headers
- `---`/`+++` file path lines
- `@@ ... @@` hunk headers with line number tracking
- Added (`+`), removed (`-`), and context (` `) lines

Line numbers are tracked accurately across multiple hunks within a single file.

### Stage 2: Analysis (`analyzer.py`)

The analyzer iterates over parsed files and their added lines, applying pattern-based rules:

| Rule                | Severity | Description                                   |
|---------------------|----------|-----------------------------------------------|
| `large-change`      | warning  | File has more than 300 added lines            |
| `todo-comment`      | info     | Added line contains TODO, FIXME, or HACK      |
| `debug-statement`   | warning  | Added line contains print(), console.log, etc |
| `hardcoded-secret`  | error    | Added line matches secret patterns             |
| `long-line`         | info     | Added line exceeds 120 characters              |
| `trailing-whitespace` | info   | Added line has trailing whitespace             |

Rules are intentionally simple and deterministic. They use compiled regular expressions for performance.

### Stage 3: Reporting (`reporter.py`)

Two output formats are supported:

- **Text**: A Rich-formatted table with colour-coded severity and an issue summary.
- **JSON**: Structured output for CI integration, containing a `comments` array and a `summary` object.

## CLI Design

The CLI uses Typer for argument parsing and Rich for terminal formatting. Exit codes follow standard conventions:

- `0`: No issues found (or only info-level issues when filtering).
- `1`: Issues found at or above the requested severity.
- `2`: Input error (missing file, invalid arguments).

## Extensibility

New rules can be added to `analyzer.py` by appending logic inside the `analyze_diff` function. Each rule produces `ReviewComment` instances with a unique `rule` identifier.
