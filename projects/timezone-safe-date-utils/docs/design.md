# Design Decisions

## Overview

`timezone-safe-date-utils` is a TypeScript library that wraps JavaScript's built-in
`Date` and `Intl.DateTimeFormat` APIs to provide timezone-safe date/time operations.

## Why This Library?

JavaScript's `Date` object stores instants as UTC milliseconds but implicitly converts
to the host machine's local timezone for most operations (`getHours()`, `toString()`,
etc.). This leads to subtle bugs in server-side and cross-timezone applications.

Common pitfalls:

1. `new Date("2024-06-15")` is interpreted as midnight UTC, but `.getDate()` may
   return 14 in western timezones.
2. There is no built-in way to format a date in a specific timezone without
   `Intl.DateTimeFormat`.
3. Date arithmetic that should be timezone-aware (e.g., "start of day in NYC")
   requires manual offset calculations.

## Core Design: SafeDate

The `SafeDate` interface pairs a UTC `Date` with explicit timezone metadata:

```typescript
interface SafeDate {
  utc: Date;        // The underlying UTC instant
  timezone: string; // IANA timezone identifier
  offset: number;   // UTC offset in minutes at this instant
}
```

This makes the timezone context explicit and prevents accidental local-timezone
conversions.

## Why Intl.DateTimeFormat?

We chose the built-in `Intl.DateTimeFormat` API because:

1. **Zero dependencies**: No external libraries needed. Keeps the bundle size minimal.
2. **IANA timezone database**: The runtime's ICU data provides authoritative timezone
   rules, including historical DST changes.
3. **Wide support**: Available in all modern browsers and Node.js 12+.
4. **Maintained automatically**: Timezone rules update with the runtime, not with
   library releases.

Trade-offs:

- `Intl.DateTimeFormat` is designed for formatting, not computation. We use
  `formatToParts()` to extract numeric components for offset calculations, which
  is a well-known technique but slightly indirect.
- Performance: Creating `Intl.DateTimeFormat` instances has some overhead. For
  hot paths, consider caching SafeDate objects.

## Offset Computation

To compute the UTC offset for a timezone at a specific instant:

1. Use `Intl.DateTimeFormat` with `formatToParts()` to get the local date/time
   components in the target timezone.
2. Build a UTC timestamp from those local components using `Date.UTC()`.
3. Subtract the original UTC timestamp to get the offset.

This avoids any dependency on non-standard APIs or hardcoded timezone rules.

## Immutability

All functions return new `SafeDate` objects rather than mutating existing ones.
This follows functional programming principles and prevents shared-state bugs.

## Error Handling

- Invalid timezone strings throw `RangeError` with descriptive messages.
- Invalid date values throw `RangeError`.
- Validation functions (`isValidTimezone`, `isValidDate`) return booleans for
  non-throwing checks.
