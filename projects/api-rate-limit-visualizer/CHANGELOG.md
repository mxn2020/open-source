# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Dashboard layout with summary cards, charts, and endpoint table.
- Line chart visualization of rate limit usage over time using Recharts.
- Time range selector supporting 1h, 6h, 24h, and 7d views.
- Mock data generation for five API endpoints with realistic usage patterns.
- Per-endpoint statistics: total requests, average usage, peak usage, remaining quota.
- Color-coded status badges (Healthy/Warning/Critical) based on usage levels.
- Full TypeScript type definitions with strict mode.
- Vitest test suite with React Testing Library.
- ESLint + Prettier configuration for consistent code style.
