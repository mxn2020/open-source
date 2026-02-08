# Splitting Projects into Separate Repositories

Each project in this monorepo is designed to be extracted into its own standalone repository. This guide explains how to do that.

## Using git filter-repo

[git filter-repo](https://github.com/newren/git-filter-repo) is the recommended tool for extracting a project with its full history.

### Prerequisites

```bash
pip install git-filter-repo
```

### Extraction Steps

1. **Clone the monorepo** (fresh clone recommended):

```bash
git clone https://github.com/mxn2020/open-source.git my-project-extract
cd my-project-extract
```

2. **Extract the project directory**:

```bash
git filter-repo --subdirectory-filter projects/<project-name>
```

3. **Verify the result**:

```bash
git log --oneline  # Should show only commits touching that project
ls                  # Should show the project files at root level
```

4. **Set up new remote**:

```bash
git remote add origin https://github.com/<org>/<project-name>.git
git push -u origin main
```

## Post-Extraction Setup

### Standalone CI

Create `.github/workflows/ci.yml` in the new repo:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: python -m pytest tests/ -v --cov
      - run: python -m ruff check src/ tests/
```

### Publishing to PyPI

For Python projects:

```bash
# Build
uv build
# or: python -m build

# Upload to PyPI
twine upload dist/*
```

For TypeScript projects:

```bash
pnpm build
npm publish
```

### Creating a Demo/Marketing Site

1. Set up GitHub Pages from the `docs/` directory or a `gh-pages` branch
2. Use mkdocs-material for documentation
3. Add a landing page with:
   - Project description and value proposition
   - Quick start guide
   - Screenshots/GIFs
   - Link to PyPI/npm package
   - Link to GitHub repository
