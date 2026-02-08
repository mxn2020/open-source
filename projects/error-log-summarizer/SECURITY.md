# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue.
2. Email the maintainers with a detailed description of the vulnerability.
3. Include steps to reproduce the issue and any relevant log samples (redacted of sensitive data).

We will acknowledge receipt within 48 hours and aim to provide a fix or mitigation plan within 7 days.

## Security Considerations

- **Log file handling**: The tool reads log files as plain text. It does not execute any content from log files.
- **JSON parsing**: JSON log lines are parsed using Python's standard `json` module. Malformed JSON is silently skipped.
- **File access**: The tool only reads files specified by the user. It does not write to any files unless output is redirected by the user's shell.
- **No network access**: The tool operates entirely offline and makes no network requests.
