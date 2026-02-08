# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in dotenv-doctor, please report it responsibly.

**Do not open a public issue.** Instead, send an email to the maintainers with:

1. A description of the vulnerability.
2. Steps to reproduce.
3. The potential impact.

We will acknowledge receipt within 48 hours and aim to release a fix within 7 days for critical issues.

## Scope

dotenv-doctor is a local development tool that reads `.env` files from disk. It does not make network requests, store credentials, or run in production environments. The primary risk surface is malicious `.env` file content leading to unexpected behavior during parsing.
