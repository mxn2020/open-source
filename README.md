# Open Source Monorepo

[![CI](https://github.com/mxn2020/open-source/actions/workflows/ci.yml/badge.svg)](https://github.com/mxn2020/open-source/actions/workflows/ci.yml)

A collection of production-quality, independently publishable open-source projects.

## Projects

| Project | Type | Description | Version |
|---------|------|-------------|---------|
| [config-drift-detector](projects/config-drift-detector/) | Python CLI | Detect drift between configuration sources | 0.1.0 |
| [pr-reviewer-bot](projects/pr-reviewer-bot/) | Python CLI | Automated PR review suggestions | 0.1.0 |
| [dotenv-doctor](projects/dotenv-doctor/) | Python CLI | Validate and diagnose .env files | 0.1.0 |
| [feature-flag-service](projects/feature-flag-service/) | FastAPI | Feature flag management API | 0.1.0 |
| [api-rate-limit-visualizer](projects/api-rate-limit-visualizer/) | React + TS | Visualize API rate limit usage | 0.1.0 |
| [prompt-version-control](projects/prompt-version-control/) | Python CLI | Version control for LLM prompts | 0.1.0 |
| [model-output-evaluator](projects/model-output-evaluator/) | Python CLI | Evaluate and score model outputs | 0.1.0 |
| [timezone-safe-date-utils](projects/timezone-safe-date-utils/) | TypeScript | Timezone-safe date utilities | 0.1.0 |
| [retry-with-backoff](projects/retry-with-backoff/) | Python lib | Retry with configurable backoff strategies | 0.1.0 |
| [error-log-summarizer](projects/error-log-summarizer/) | Python CLI | Summarize and categorize error logs | 0.1.0 |
| [good-first-issue-generator](projects/good-first-issue-generator/) | Python CLI | Generate good first issues for projects | 0.1.0 |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mxn2020/open-source.git
cd open-source

# Bootstrap all projects
make bootstrap

# Run all tests
make test

# Run all linters
make lint
```

## Documentation

- [Architecture](docs/architecture.md)
- [Developer Guide](docs/dev-guide.md)
- [Splitting Projects](docs/splitting.md)
- [Contributing](CONTRIBUTING.md)

## License

[MIT](LICENSE)
