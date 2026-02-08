"""Validate parsed .env entries and produce diagnostic issues."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from dotenv_doctor.parser import EnvEntry


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    """A single validation issue."""

    key: str
    line_number: int
    severity: Severity
    message: str


_VALID_KEY = re.compile(r"^[A-Z_][A-Z0-9_]*$")


def validate_env(
    entries: list[EnvEntry],
    template: list[EnvEntry] | None = None,
) -> list[Issue]:
    """Run all validation checks on the given entries.

    If *template* is provided, entries are also compared against the template
    for missing and extra keys.
    """
    issues: list[Issue] = []
    issues.extend(_check_duplicate_keys(entries))
    issues.extend(_check_empty_values(entries))
    issues.extend(_check_invalid_key_names(entries))

    if template is not None:
        issues.extend(_check_template(entries, template))

    return issues


def _check_duplicate_keys(entries: list[EnvEntry]) -> list[Issue]:
    seen: dict[str, int] = {}
    issues: list[Issue] = []
    for entry in entries:
        if entry.key in seen:
            issues.append(
                Issue(
                    key=entry.key,
                    line_number=entry.line_number,
                    severity=Severity.WARNING,
                    message=f"Duplicate key '{entry.key}' (first seen on line {seen[entry.key]})",
                )
            )
        else:
            seen[entry.key] = entry.line_number
    return issues


def _check_empty_values(entries: list[EnvEntry]) -> list[Issue]:
    return [
        Issue(
            key=entry.key,
            line_number=entry.line_number,
            severity=Severity.WARNING,
            message=f"Empty value for key '{entry.key}'",
        )
        for entry in entries
        if entry.value == ""
    ]


def _check_invalid_key_names(entries: list[EnvEntry]) -> list[Issue]:
    return [
        Issue(
            key=entry.key,
            line_number=entry.line_number,
            severity=Severity.WARNING,
            message=(
                f"Key '{entry.key}' does not match [A-Z_][A-Z0-9_]* pattern"
            ),
        )
        for entry in entries
        if not _VALID_KEY.match(entry.key)
    ]


def _check_template(
    entries: list[EnvEntry], template: list[EnvEntry]
) -> list[Issue]:
    env_keys = {e.key for e in entries}
    template_keys = {t.key for t in template}

    issues: list[Issue] = []

    # Keys in env but not in template
    for entry in entries:
        if entry.key not in template_keys:
            issues.append(
                Issue(
                    key=entry.key,
                    line_number=entry.line_number,
                    severity=Severity.INFO,
                    message=f"Key '{entry.key}' is not defined in the template",
                )
            )

    # Keys in template but missing from env
    for tmpl in template:
        if tmpl.key not in env_keys:
            issues.append(
                Issue(
                    key=tmpl.key,
                    line_number=0,
                    severity=Severity.ERROR,
                    message=f"Key '{tmpl.key}' required by template is missing",
                )
            )

    return issues
