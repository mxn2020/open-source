# Design

## Overview

The Good First Issue Generator follows a three-stage pipeline:

1. **Scan** — Walk the project directory and identify code improvement opportunities
2. **Generate** — Convert raw opportunities into structured issue templates
3. **Report** — Format templates for the desired output medium

## Architecture

```
┌─────────┐     ┌───────────┐     ┌──────────┐
│ Scanner │────▶│ Generator │────▶│ Reporter │
└─────────┘     └───────────┘     └──────────┘
     │                │                 │
     ▼                ▼                 ▼
CodeOpportunity  IssueTemplate    Text/JSON/MD
```

### Scanner (`scanner.py`)

The scanner is responsible for finding improvement opportunities in source code. Each detection
function returns a list of `CodeOpportunity` dataclass instances.

**Detection strategies:**

- **TODO comments**: Regex matching for `TODO`, `FIXME`, `HACK`, `XXX` patterns in comments
- **Missing tests**: Compare source file basenames against test file basenames
- **Missing docstrings**: Check Python `def` and `class` statements for a following docstring
- **Missing type hints**: Check Python `def` statements for `->` return type annotations

**Filtering:**

- File extensions are configurable (default: `.py`, `.ts`, `.js`)
- Common non-source directories are skipped (`node_modules`, `__pycache__`, `.git`, etc.)

### Generator (`generator.py`)

The generator converts `CodeOpportunity` instances into `IssueTemplate` instances. Each opportunity
type has a template that produces a title, body with steps, appropriate labels, and difficulty.

**Deduplication**: Issues with identical titles are deduplicated.

**Prioritization**: Issues are sorted by difficulty (easy first), then by file path and line number.

### Reporter (`reporter.py`)

The reporter handles output formatting:

- **Text**: Uses Rich library for colorful terminal output with panels
- **JSON**: Structured JSON output for programmatic consumption
- **Markdown**: GitHub-flavored Markdown with sections per issue

## Data Flow

```python
# CLI entry point
opportunities = scan_directory(path, extensions)
issues = generate_issues(opportunities, max_issues)
output = report_text(issues)  # or report_json / report_markdown
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Issues generated successfully |
| 1 | No improvement opportunities found |
| 2 | Error (invalid directory, scan failure) |
