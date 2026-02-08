# Architecture

## Monorepo Design

This monorepo contains 11 independent projects organized under `projects/`. Each project:

- Has its own packaging (pyproject.toml or package.json)
- Is independently testable and publishable
- Follows the standard project contract
- Can be extracted into a standalone repository

## Directory Structure

```
/
├── projects/
│   ├── config-drift-detector/     # Python CLI
│   ├── pr-reviewer-bot/           # Python CLI
│   ├── dotenv-doctor/             # Python CLI
│   ├── feature-flag-service/      # FastAPI service
│   ├── api-rate-limit-visualizer/ # React + TypeScript
│   ├── prompt-version-control/    # Python CLI
│   ├── model-output-evaluator/    # Python CLI
│   ├── timezone-safe-date-utils/  # TypeScript library
│   ├── retry-with-backoff/        # Python library
│   ├── error-log-summarizer/      # Python CLI
│   └── good-first-issue-generator/# Python CLI
├── docs/                          # mkdocs site
├── .github/workflows/             # CI/CD
└── tools/                         # Shared tooling
```

## Technology Choices

| Category | Choice | Rationale |
|----------|--------|-----------|
| Python CLIs | Typer + Rich | Modern CLI framework with great UX |
| APIs | FastAPI | Fast, typed, auto-OpenAPI docs |
| Web | React + Vite + Recharts | Standard, fast build tooling |
| Python packaging | uv | Fast, reliable package management |
| TS packaging | pnpm | Efficient, strict node_modules |
| Python testing | pytest | De facto standard |
| TS testing | vitest | Fast, Vite-native |
| Python lint | ruff + black | Fast, consistent |
| TS lint | eslint + prettier | Standard toolchain |
| Docs | mkdocs-material | Beautiful, Markdown-based |
| Data | SQLite | Zero-config, embedded |

## CI/CD Strategy

- **CI**: Matrix build across all projects (lint + test)
- **Release**: Tag-based per-project releases via manual dispatch
- **Caching**: Python (pip/uv) and Node (pnpm) caches
