# Development Guide

## Prerequisites

- Node.js 18+
- pnpm

## Setup

```bash
pnpm install
```

## Development Server

```bash
pnpm dev
```

Opens at [http://localhost:5173](http://localhost:5173) with hot module replacement.

## Testing

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm exec vitest
```

Tests use Vitest with jsdom environment and React Testing Library. Recharts components are mocked in tests to avoid jsdom rendering issues.

### Test Structure

```
src/__tests__/
├── mock-data.test.ts           # Data generation logic
├── App.test.tsx                # App rendering
└── components/
    ├── SummaryCard.test.tsx    # Card rendering
    ├── Dashboard.test.tsx      # Dashboard integration
    ├── EndpointTable.test.tsx  # Table rendering
    └── StatusBadge.test.tsx    # Badge color logic
```

## Linting

```bash
pnpm lint
```

Uses ESLint with TypeScript and React plugins.

## Formatting

```bash
pnpm format
```

Uses Prettier with the project's `.prettierrc` configuration.

## Building

```bash
pnpm build
```

Runs TypeScript type checking followed by Vite production build. Output goes to `dist/`.

## Preview Production Build

```bash
pnpm preview
```

Serves the built `dist/` directory locally.
