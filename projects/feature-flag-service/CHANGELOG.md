# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of the Feature Flag Service.
- CRUD endpoints for managing feature flags (`POST`, `GET`, `PUT`, `DELETE`).
- Flag evaluation endpoint with percentage-based rollout support.
- Consistent user bucketing using SHA-256 hashing for percentage rollouts.
- SQLite-based persistent storage.
- API key authentication for admin (write) endpoints.
- CORS middleware enabled by default.
- Health check endpoint at `/health`.
- Tag-based filtering for listing flags.
