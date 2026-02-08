# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the Good First Issue Generator, please report it
responsibly by opening a private security advisory on the repository.

Do not open a public issue for security vulnerabilities.

## Scope

The Good First Issue Generator is a local CLI tool that reads files from the filesystem. It does
not make network connections, store credentials, or execute arbitrary code from scanned files.

Security considerations include:

- **Path traversal**: The scanner follows symbolic links according to `os.walk` defaults.
  Ensure you scan trusted directories only.
- **File encoding**: The scanner uses `errors="replace"` when reading files, which prevents
  crashes from unexpected encodings but may produce garbled output for non-UTF-8 files.
- **Large directories**: Scanning very large codebases may consume significant memory. Use the
  `--extensions` flag to limit the scan scope if needed.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
