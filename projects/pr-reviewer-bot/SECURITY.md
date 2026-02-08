# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in pr-reviewer-bot, please report it responsibly.

**Do not open a public issue.** Instead, send an email to the repository maintainers with the following information:

- Description of the vulnerability.
- Steps to reproduce.
- Potential impact.

We will acknowledge receipt within 48 hours and provide an estimated timeline for a fix.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |

## Security Considerations

pr-reviewer-bot analyzes diff text locally. It does not transmit data to external services. The hardcoded-secret rule is a best-effort pattern match and should not be relied upon as the sole mechanism for secret detection. Use dedicated secret scanning tools for comprehensive coverage.
