# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please email the maintainers or use GitHub's private vulnerability reporting feature.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Considerations

- **API Key Authentication**: Admin endpoints (create, update, delete) require an API key
  passed via the `X-API-Key` header. The key is read from the `FF_API_KEY` environment variable.
- **Default Key**: The default API key (`dev-api-key`) is intended for development only.
  Always set a strong, unique key in production via the `FF_API_KEY` environment variable.
- **No Encryption at Rest**: The SQLite database stores data unencrypted on disk.
  Protect access to the database file in production environments.
- **CORS**: CORS is configured to allow all origins by default. Restrict allowed origins
  in production deployments.
