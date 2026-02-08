# Contributing to the Open Source Monorepo

Thank you for your interest in contributing! This document provides guidelines and conventions for contributing to any project in this monorepo.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- **Python 3.12+** for Python projects
- **Node.js 20+** and **pnpm** for TypeScript projects
- **uv** for Python package management
- **Git** with pre-commit hooks

### Bootstrap

```bash
make bootstrap
```

This installs all dependencies for all projects and sets up pre-commit hooks.

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or tooling changes
- `ci`: CI/CD changes

### Scope

Use the project folder name as scope:

```
feat(config-drift-detector): add TOML support
fix(feature-flag-service): handle missing API key
docs(retry-with-backoff): update examples
```

## Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Run lint and tests: `make lint && make test`
5. Commit using conventional commits
6. Push and create a Pull Request

## Code Style

### Python

- **Formatter**: black (line length 99)
- **Linter**: ruff
- **Type hints**: Required for all public APIs
- All code must pass `ruff check` and `black --check`

### TypeScript

- **Formatter**: prettier
- **Linter**: eslint
- **Strict mode**: enabled

## Testing

### Python

```bash
cd projects/<project-name>
uv run pytest tests/ -v --cov
```

### TypeScript

```bash
cd projects/<project-name>
pnpm test
```

## Adding a New Project

1. Create a directory under `projects/`
2. Follow the standard project contract (see README.md)
3. Add the project to the CI matrix in `.github/workflows/ci.yml`
4. Add documentation in `docs/`
5. Update the root README.md

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add changelog entries
4. Request review from at least one maintainer
5. Squash-merge after approval

## Questions?

See [SUPPORT.md](SUPPORT.md) for how to get help.
