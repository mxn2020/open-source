# timezone-safe-date-utils

Timezone-safe date utilities for TypeScript. A zero-dependency library built on the native `Intl.DateTimeFormat` API for reliable timezone conversions, formatting, and parsing.

## Features

- **Timezone validation** – Check if a string is a valid IANA timezone identifier.
- **Timezone conversion** – Convert dates between any two IANA timezones.
- **UTC conversion** – Convert to and from UTC with explicit timezone context.
- **Timezone-aware formatting** – Format dates for display in any timezone, including ISO 8601 output with correct offsets.
- **Relative time formatting** – Human-readable strings like "2 hours ago" or "in 3 days".
- **Timezone-aware parsing** – Parse date strings with explicit timezone context.
- **Zero runtime dependencies** – Uses only built-in `Intl` APIs.
- **Full TypeScript support** – Written in TypeScript with complete type declarations.

## Installation

```bash
npm install timezone-safe-date-utils
```

## Quick Start

```typescript
import {
  isValidTimezone,
  convertTimezone,
  formatISO,
  parseInTimezone,
  nowIn,
} from "timezone-safe-date-utils";

// Validate a timezone
isValidTimezone("America/New_York"); // true
isValidTimezone("Fake/Zone");        // false

// Get current time in a timezone
const tokyoNow = nowIn("Asia/Tokyo");

// Convert between timezones
const date = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
const result = convertTimezone(date, "America/New_York", "Asia/Tokyo");

// Format with timezone offset
formatISO(new Date("2024-06-15T16:00:00Z"), "America/New_York");
// → "2024-06-15T12:00:00-04:00"

// Parse a date string in a specific timezone
const parsed = parseInTimezone("2024-06-15 12:00:00", "America/New_York");
// → Date representing 2024-06-15T16:00:00Z
```

## API Reference

### Timezone Utilities (`zones`)

#### `isValidTimezone(tz: string): boolean`

Check if a string is a valid IANA timezone identifier.

```typescript
isValidTimezone("Europe/London"); // true
isValidTimezone("Invalid");       // false
```

#### `getTimezoneOffset(tz: string, date?: Date): number`

Get the UTC offset in minutes for a timezone at a given date. Positive values mean the timezone is ahead of UTC. Defaults to the current time if no date is provided.

```typescript
getTimezoneOffset("Asia/Tokyo"); // 540 (UTC+9)
getTimezoneOffset("America/New_York", new Date("2024-06-15")); // -240 (EDT)
```

#### `listCommonTimezones(): string[]`

Return a curated list of common IANA timezone names.

```typescript
const zones = listCommonTimezones();
// ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo", ...]
```

### Conversion (`convert`)

#### `convertTimezone(date: Date, fromTz: string, toTz: string): Date`

Convert a date between timezones. Interprets the date as wall-clock time in `fromTz` and returns a Date representing the equivalent wall-clock time in `toTz`.

```typescript
const nyNoon = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
const tokyoTime = convertTimezone(nyNoon, "America/New_York", "Asia/Tokyo");
```

#### `toUTC(date: Date, sourceTz: string): Date`

Convert a wall-clock time in a source timezone to UTC.

```typescript
const utc = toUTC(new Date(Date.UTC(2024, 5, 15, 12, 0, 0)), "America/New_York");
// → 2024-06-15T16:00:00Z
```

#### `fromUTC(date: Date, targetTz: string): Date`

Convert a UTC date to a target timezone. Returns a Date whose UTC components represent the wall-clock time in the target timezone.

```typescript
const ny = fromUTC(new Date("2024-06-15T16:00:00Z"), "America/New_York");
```

#### `nowIn(tz: string): Date`

Get the current time in a specific timezone.

```typescript
const tokyoNow = nowIn("Asia/Tokyo");
```

### Formatting (`format`)

#### `formatInTimezone(date: Date, tz: string, options?: Intl.DateTimeFormatOptions): string`

Format a date for display in a specific timezone using `Intl.DateTimeFormat`.

```typescript
formatInTimezone(new Date(), "Europe/London", {
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "2-digit",
  minute: "2-digit",
});
```

#### `formatISO(date: Date, tz: string): string`

Format a date as an ISO 8601 string with the correct timezone offset.

```typescript
formatISO(new Date("2024-06-15T16:00:00Z"), "UTC");
// → "2024-06-15T16:00:00Z"

formatISO(new Date("2024-06-15T16:00:00Z"), "Asia/Tokyo");
// → "2024-06-16T01:00:00+09:00"
```

#### `formatRelative(date: Date, baseDate?: Date): string`

Format a date as a human-readable relative time string. Defaults to comparing against the current time.

```typescript
const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000);
formatRelative(twoHoursAgo); // "2 hours ago"

const inThreeDays = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);
formatRelative(inThreeDays); // "in 3 days"
```

### Parsing (`parse`)

#### `parseISO(isoString: string): Date`

Parse an ISO 8601 string into a Date object. Supports UTC (`Z`), positive, and negative offsets.

```typescript
parseISO("2024-06-15T14:30:00Z");       // Date at 14:30 UTC
parseISO("2024-06-15T14:30:00+05:30");  // Date at 09:00 UTC
parseISO("2024-06-15");                  // Date-only
```

#### `parseInTimezone(dateStr: string, tz: string, format?: string): Date`

Parse a date string assuming it represents a wall-clock time in the given timezone. Returns the corresponding UTC Date.

Supported formats:
- `"YYYY-MM-DD"` – date only (time defaults to 00:00:00)
- `"YYYY-MM-DD HH:mm:ss"` – date and time (default)

```typescript
parseInTimezone("2024-06-15 12:00:00", "America/New_York");
// → Date representing 2024-06-15T16:00:00Z

parseInTimezone("2024-06-15", "Asia/Tokyo");
// → Date representing 2024-06-14T15:00:00Z
```

## Development

```bash
pnpm install        # Install dependencies
pnpm build          # Compile TypeScript
pnpm test           # Run tests
pnpm lint           # Lint source code
pnpm format         # Format source code
```

See [docs/development.md](docs/development.md) for detailed development instructions.

## License

[MIT](LICENSE)
