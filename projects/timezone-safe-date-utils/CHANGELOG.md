# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-06-15

### Added

- `isValidTimezone` - Validate IANA timezone identifiers.
- `getTimezoneOffset` - Get UTC offset in minutes for a timezone at a specific date.
- `listCommonTimezones` - Curated list of common IANA timezone names.
- `convertTimezone` - Convert a date between two timezones.
- `toUTC` - Convert a wall-clock time from a timezone to UTC.
- `fromUTC` - Convert a UTC time to a wall-clock time in a timezone.
- `nowIn` - Get the current time in a specific timezone.
- `formatInTimezone` - Format a date for display in a given timezone.
- `formatISO` - Format a date as ISO 8601 with timezone offset.
- `formatRelative` - Human-readable relative time formatting.
- `parseISO` - Parse ISO 8601 strings to Date objects.
- `parseInTimezone` - Parse date strings as wall-clock times in a given timezone.
