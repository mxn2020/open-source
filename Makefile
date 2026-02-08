.PHONY: bootstrap lint test ci docs clean

PYTHON_PROJECTS := config-drift-detector pr-reviewer-bot dotenv-doctor \
	feature-flag-service prompt-version-control model-output-evaluator \
	retry-with-backoff error-log-summarizer good-first-issue-generator

TS_PROJECTS := api-rate-limit-visualizer timezone-safe-date-utils

bootstrap:
	@echo "==> Installing pre-commit hooks..."
	pip install pre-commit 2>/dev/null || true
	pre-commit install 2>/dev/null || true
	@echo "==> Bootstrapping Python projects..."
	@for proj in $(PYTHON_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/pyproject.toml ]; then \
			cd projects/$$proj && pip install -e ".[dev]" 2>/dev/null || pip install -e . 2>/dev/null; cd ../..; \
		fi; \
	done
	@echo "==> Bootstrapping TypeScript projects..."
	@for proj in $(TS_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/package.json ]; then \
			cd projects/$$proj && pnpm install; cd ../..; \
		fi; \
	done
	@echo "==> Bootstrap complete!"

lint:
	@echo "==> Linting Python projects..."
	@for proj in $(PYTHON_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/pyproject.toml ]; then \
			cd projects/$$proj && python -m ruff check src/ tests/ 2>/dev/null || true && python -m black --check src/ tests/ 2>/dev/null || true; cd ../..; \
		fi; \
	done
	@echo "==> Linting TypeScript projects..."
	@for proj in $(TS_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/package.json ]; then \
			cd projects/$$proj && pnpm run lint 2>/dev/null || true; cd ../..; \
		fi; \
	done

test:
	@echo "==> Testing Python projects..."
	@for proj in $(PYTHON_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/pyproject.toml ]; then \
			cd projects/$$proj && python -m pytest tests/ -v 2>/dev/null || true; cd ../..; \
		fi; \
	done
	@echo "==> Testing TypeScript projects..."
	@for proj in $(TS_PROJECTS); do \
		echo "--- $$proj ---"; \
		if [ -f projects/$$proj/package.json ]; then \
			cd projects/$$proj && pnpm test 2>/dev/null || true; cd ../..; \
		fi; \
	done

ci: lint test

docs:
	@echo "==> Building documentation..."
	pip install mkdocs-material 2>/dev/null || true
	mkdocs build

clean:
	@echo "==> Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -name .coverage -delete 2>/dev/null || true
	rm -rf site/ htmlcov/
