# Developer Guide

## Prerequisites

- Python 3.12+
- Node.js 20+ (for TypeScript projects)
- pnpm (for TypeScript projects)
- uv (recommended) or pip (for Python projects)
- Git

## Initial Setup

```bash
# Clone the repository
git clone https://github.com/mxn2020/open-source.git
cd open-source

# Bootstrap all projects
make bootstrap
```

## Working on a Python Project

```bash
cd projects/<project-name>

# Install in development mode
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Run linting
python -m ruff check src/ tests/
python -m black --check src/ tests/

# Format code
python -m black src/ tests/
python -m ruff check --fix src/ tests/
```

## Working on a TypeScript Project

```bash
cd projects/<project-name>

# Install dependencies
pnpm install

# Run development server (for web apps)
pnpm dev

# Run tests
pnpm test

# Run linting
pnpm lint
```

## Running All Tests

```bash
make test
```

## Running All Linters

```bash
make lint
```

## Building Documentation

```bash
make docs
# Then open site/index.html
```

## Conventions

- **Commit messages**: Follow [Conventional Commits](https://www.conventionalcommits.org/)
- **Branch naming**: `feat/<description>`, `fix/<description>`, `docs/<description>`
- **Python style**: black (line-length 99) + ruff
- **TypeScript style**: prettier + eslint (strict)
