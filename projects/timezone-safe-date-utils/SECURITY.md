# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue.
2. Email the maintainers with a description of the vulnerability,
   steps to reproduce, and any relevant details.
3. Allow reasonable time for the issue to be addressed before any public disclosure.

We will acknowledge your report within 48 hours and work to release a fix as quickly as possible.

## Security Considerations

This library relies on the built-in `Intl.DateTimeFormat` API for timezone operations. It does not make network requests, access the filesystem, or execute dynamic code. The primary security considerations are:

- **Input validation**: All public functions validate timezone strings before use to prevent unexpected behavior from invalid inputs.
- **No dependencies**: The library has zero runtime dependencies, minimizing supply chain risk.
