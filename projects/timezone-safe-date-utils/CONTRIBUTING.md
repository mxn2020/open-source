# Contributing to timezone-safe-date-utils

Thank you for your interest in contributing! This document provides guidelines for
contributing to the project.

## Getting Started

1. Fork and clone the repository.
2. Install development dependencies:

   ```bash
   pnpm install
   ```

3. Run the tests to make sure everything is working:

   ```bash
   pnpm test
   ```

## Development Workflow

1. Create a feature branch from `main`.
2. Make your changes, adding tests for new functionality.
3. Ensure all tests pass: `pnpm test`
4. Ensure code passes linting: `pnpm lint`
5. Ensure code is formatted: `pnpm format`
6. Ensure the build succeeds: `pnpm build`
7. Submit a pull request.

## Code Style

- Strict TypeScript with `strict: true` in `tsconfig.json`.
- Line length limit is 99 characters (configured in `.prettierrc`).
- Use type hints for all public APIs.
- Write JSDoc comments for all public functions.

## Testing

- All new features must include tests.
- Tests are in the `tests/` directory using `vitest`.
- Aim for high test coverage.
- Test edge cases: DST transitions, invalid inputs, boundary dates.

## Design Principles

- **Zero runtime dependencies**: Do not add external dependencies for core functionality.
- **Immutability**: All functions return new objects rather than mutating inputs.
- **Explicit timezone context**: Never rely on the host's local timezone.

## Reporting Issues

- Use the GitHub issue tracker.
- Include a minimal reproducible example when reporting bugs.
- Describe expected vs actual behavior.
