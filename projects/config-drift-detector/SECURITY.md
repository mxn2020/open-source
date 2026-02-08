# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Config Drift Detector, please
report it responsibly by emailing the maintainers. Do **not** open a public
GitHub issue for security vulnerabilities.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Scope

Config Drift Detector reads local configuration files. It does not make
network requests or execute arbitrary code from configuration values. The
primary security consideration is ensuring safe parsing of untrusted YAML,
JSON, and TOML files — the tool uses `yaml.safe_load`, `json.loads`, and
`tomllib.loads`, all of which are safe against code injection.
