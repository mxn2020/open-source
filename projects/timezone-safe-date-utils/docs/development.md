# Development Guide

## Prerequisites

- Node.js 18+
- pnpm

## Setup

```bash
cd projects/timezone-safe-date-utils
pnpm install
```

## Scripts

| Command         | Description                          |
|-----------------|--------------------------------------|
| `pnpm build`    | Compile TypeScript to `dist/`        |
| `pnpm test`     | Run tests with vitest                |
| `pnpm lint`     | Lint source and test files           |
| `pnpm format`   | Check formatting with prettier       |

## Project Structure

```
src/
  index.ts        — Public API exports
  types.ts        — Type definitions (SafeDate, DateRange, etc.)
  create.ts       — SafeDate creation functions
  convert.ts      — Timezone conversion functions
  format.ts       — Formatting utilities
  compare.ts      — Comparison and diff functions
  validate.ts     — Validation helpers
  arithmetic.ts   — Date arithmetic (add, startOfDay, etc.)
tests/
  create.test.ts
  convert.test.ts
  format.test.ts
  compare.test.ts
  validate.test.ts
  arithmetic.test.ts
examples/
  basic-usage.ts
  timezone-conversion.ts
docs/
  design.md       — Architecture and design decisions
  api.md          — Full API reference
  development.md  — This file
```

## Testing

Tests use [vitest](https://vitest.dev/) and cover all public API functions. Run:

```bash
pnpm test
```

To run a specific test file:

```bash
pnpm test -- tests/create.test.ts
```

## Adding a New Function

1. Add the implementation in the appropriate `src/` module.
2. Export it from `src/index.ts`.
3. Add tests in the corresponding `tests/` file.
4. Update `docs/api.md` with the new function signature and description.
5. Run `pnpm lint && pnpm test && pnpm build` to verify.

## Code Style

- Strict TypeScript with `strict: true`.
- Formatting managed by Prettier (see `.prettierrc`).
- Linting with ESLint and `@typescript-eslint`.
- No external runtime dependencies — only the built-in `Intl` API.
