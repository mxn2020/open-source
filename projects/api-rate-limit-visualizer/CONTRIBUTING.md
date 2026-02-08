# Contributing to api-rate-limit-visualizer

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
- Write JSDoc comments for public functions and components.
- React components use function declarations.

## Testing

- All new features must include tests.
- Tests are in `src/__tests__/` using `vitest` and `@testing-library/react`.
- Mock Recharts components in tests to avoid jsdom rendering issues.
- Test component rendering, user interactions, and data logic.

## Design Principles

- **Mocked data only**: No external API calls in the core application.
- **Type safety**: All data flows through typed interfaces.
- **Component isolation**: Each component has a single responsibility.

## Reporting Issues

- Use the GitHub issue tracker.
- Include a minimal reproducible example when reporting bugs.
- Describe expected vs actual behavior.
