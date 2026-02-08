# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in prompt-version-control, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please send an email to the project maintainers with:

1. A description of the vulnerability.
2. Steps to reproduce the issue.
3. The potential impact.

We will acknowledge receipt within 48 hours and provide a timeline for a fix.

## Security Considerations

- **Local storage**: prompt-version-control stores data in a local SQLite database file
  (`.prompts.db` by default). Ensure appropriate file permissions are set on this file.
- **No network access**: This tool operates entirely locally and does not transmit data
  over the network.
- **Input validation**: All CLI inputs are validated before processing. SQL parameters are
  always passed via parameterized queries to prevent SQL injection.
