# Development Guide

## Prerequisites

- **Node.js** 18 or later
- **pnpm** (recommended) or npm

## Setup

```bash
git clone <repository-url>
cd timezone-safe-date-utils
pnpm install
```

## Project Structure

```
src/
├── index.ts      # Public API re-exports
├── zones.ts      # Timezone validation and information
├── convert.ts    # Timezone conversion functions
├── format.ts     # Date formatting with timezone support
└── parse.ts      # Date parsing with timezone support

tests/
├── zones.test.ts
├── convert.test.ts
├── format.test.ts
└── parse.test.ts

examples/
└── usage.ts      # Runnable usage examples

docs/
├── design.md     # Architecture and design decisions
├── api.md        # Complete API reference
└── development.md  # This file
```

## Commands

| Command              | Description                        |
| -------------------- | ---------------------------------- |
| `pnpm build`         | Compile TypeScript to `dist/`      |
| `pnpm test`          | Run all tests once                 |
| `pnpm test:watch`    | Run tests in watch mode            |
| `pnpm lint`          | Run ESLint on source and tests     |
| `pnpm format`        | Format code with Prettier          |
| `pnpm format:check`  | Check formatting without writing   |

## Building

The TypeScript compiler emits JavaScript and declaration files to `dist/`:

```bash
pnpm build
```

The `tsconfig.json` is configured with:
- `target: "ES2022"` – modern JavaScript output.
- `module: "ES2022"` – ES module output matching `"type": "module"` in `package.json`.
- `strict: true` – full strict mode.
- `declaration: true` – generates `.d.ts` files for consumers.

## Testing

Tests use [Vitest](https://vitest.dev/) and are located in `tests/`. Each source module has a corresponding test file.

```bash
pnpm test           # Single run
pnpm test:watch     # Watch mode with interactive UI
```

Tests use fixed dates (e.g., `2024-06-15T12:00:00Z`) to ensure deterministic results regardless of the machine's local timezone.

## Linting

ESLint is configured with the flat config format (ESLint 9+) using `typescript-eslint`:

```bash
pnpm lint
```

The configuration lives in `eslint.config.js` and applies recommended rules from both `@eslint/js` and `typescript-eslint`.

## Formatting

Prettier is configured via `.prettierrc`:

```bash
pnpm format         # Auto-fix formatting
pnpm format:check   # Check without writing
```

Settings: double quotes, semicolons, 2-space indentation, trailing commas.

## Adding a New Function

1. Add the function to the appropriate source module (`zones.ts`, `convert.ts`, `format.ts`, or `parse.ts`).
2. Export it from `src/index.ts`.
3. Add tests in the corresponding test file.
4. Update `docs/api.md` with the function's documentation.
5. Add a changelog entry under `## [Unreleased]` in `CHANGELOG.md`.

## How Timezone Operations Work

The library uses `Intl.DateTimeFormat` as its timezone engine. Key patterns:

- **Offset calculation**: Format the same `Date` in both UTC and the target timezone using `toLocaleString("en-US", { timeZone })`, parse the results, and measure the difference in milliseconds.
- **Timezone-aware formatting**: Use `Intl.DateTimeFormat` with `formatToParts` to extract individual date components (year, month, day, hour, etc.) in a specific timezone.
- **Timezone-aware parsing**: Construct a `Date` in UTC from parsed components, then subtract the timezone offset to get the true UTC moment.

This approach is reliable across environments because it delegates timezone data to the JavaScript runtime's ICU implementation.
