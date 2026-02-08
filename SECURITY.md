# Security Policy

## Supported Versions

| Project | Version | Supported |
| ------- | ------- | --------- |
| All projects | 0.1.x | ✅ |

## Reporting a Vulnerability

If you discover a security vulnerability in any project in this monorepo, please report it responsibly.

### How to Report

1. **DO NOT** open a public GitHub issue for security vulnerabilities.
2. Email **security@example.com** with:
   - The affected project name
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
3. You will receive an acknowledgment within 48 hours.
4. We will work with you to understand and address the issue.

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Fix Timeline**: Depends on severity, typically:
  - Critical: 24-48 hours
  - High: 1 week
  - Medium: 2 weeks
  - Low: Next release

### Disclosure Policy

- We follow [responsible disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).
- We will credit reporters in the security advisory (unless they prefer anonymity).
- We will publish advisories on GitHub Security Advisories.

## Security Best Practices

All projects in this monorepo follow these practices:

- Dependencies are regularly audited
- Secrets are never committed to the repository
- Input validation is enforced on all user-facing interfaces
- SQL injection prevention (parameterized queries)
- No eval() or equivalent dangerous functions
