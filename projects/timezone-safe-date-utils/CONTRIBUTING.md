# Contributing to timezone-safe-date-utils

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork and clone the repository.
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Run the tests to verify your setup:
   ```bash
   pnpm test
   ```

## Development Workflow

### Building

```bash
pnpm build
```

### Running Tests

```bash
pnpm test           # Run all tests once
pnpm test:watch     # Run tests in watch mode
```

### Linting and Formatting

```bash
pnpm lint           # Run ESLint
pnpm format         # Format code with Prettier
pnpm format:check   # Check formatting without writing
```

## Making Changes

1. Create a feature branch from `main`.
2. Write your code with full TypeScript types.
3. Add or update tests for any new or changed functionality.
4. Ensure all tests pass and linting is clean.
5. Update documentation if your changes affect the public API.
6. Submit a pull request with a clear description of the changes.

## Code Style

- All code is written in TypeScript with strict mode enabled.
- Use `Intl.DateTimeFormat` for timezone operations instead of third-party libraries.
- Follow the existing code patterns for consistency.
- Formatting is enforced by Prettier; run `pnpm format` before committing.

## Commit Messages

Use clear, descriptive commit messages. Prefix with a category when helpful:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions or changes
- `chore:` for maintenance tasks

## Reporting Issues

Open a GitHub issue with:

- A clear description of the problem or feature request.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
- Your environment details (Node.js version, OS).
