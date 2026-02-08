# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- `SafeDate` type pairing UTC instants with explicit timezone metadata.
- `createSafeDate`, `now`, `fromISO`, `fromComponents` creation functions.
- `toTimezone`, `toUTC`, `getOffset`, `isSameInstant` conversion functions.
- `formatSafe` with support for `YYYY`, `MM`, `DD`, `HH`, `mm`, `ss`, `Z` tokens.
- `toISOString`, `toLocaleDateString`, `toLocaleTimeString` formatting helpers.
- `isBefore`, `isAfter`, `isEqual` comparison functions.
- `diffInMilliseconds`, `diffInMinutes`, `diffInHours`, `diffInDays` diff functions.
- `isValidTimezone`, `isValidDate`, `assertTimezone` validation functions.
- `addDays`, `addHours`, `addMinutes` arithmetic functions.
- `startOfDay`, `endOfDay` timezone-aware day boundary functions.
- Full TypeScript type definitions and strict mode support.
- Zero runtime dependencies — uses only built-in `Intl.DateTimeFormat` API.
