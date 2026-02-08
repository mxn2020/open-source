# timezone-safe-date-utils

A TypeScript library that provides timezone-safe date/time utility functions. Zero
runtime dependencies — uses only the built-in `Intl.DateTimeFormat` API.

## Why?

JavaScript's `Date` object is notoriously timezone-unfriendly. It stores instants as
UTC but implicitly converts to the host's local timezone for most operations. This
leads to subtle bugs when:

- Formatting dates for users in different timezones
- Computing "start of day" or "end of day" in a specific timezone
- Comparing dates created in different timezone contexts
- Serializing dates that should preserve timezone intent

`timezone-safe-date-utils` solves this by pairing every date with explicit timezone
metadata via the `SafeDate` type.

## Features

- **Explicit timezone context**: Every date carries its timezone and offset.
- **Zero runtime dependencies**: Uses only the built-in `Intl.DateTimeFormat` API.
- **Timezone conversion**: Convert between any IANA timezones with a single call.
- **Safe formatting**: Format dates in any timezone without local-timezone surprises.
- **Timezone-aware arithmetic**: Add days/hours/minutes with correct DST handling.
- **Validation**: Check timezone strings and date values before use.
- **Comparison utilities**: Compare dates across timezones by their UTC instant.
- **Type-safe**: Full TypeScript types and strict mode.

## Installation

```bash
pnpm add timezone-safe-date-utils
```

## Quick Start

```typescript
import { fromComponents, toTimezone, formatSafe } from "timezone-safe-date-utils";

// Create a date: 2024-07-15 at 9:00 AM in New York
const meeting = fromComponents(2024, 7, 15, 9, 0, 0, "America/New_York");

// What time is that in Tokyo?
const inTokyo = toTimezone(meeting, "Asia/Tokyo");
console.log(formatSafe(inTokyo, "YYYY-MM-DD HH:mm Z"));
// => "2024-07-15 22:00 +09:00"
```

## Examples

### Create dates safely

```typescript
import { createSafeDate, now, fromISO, fromComponents } from "timezone-safe-date-utils";

// From a Date object
const sd1 = createSafeDate(new Date(), "Europe/London");

// Current time in a timezone
const sd2 = now("Asia/Tokyo");

// From an ISO string
const sd3 = fromISO("2024-06-15T14:00:00Z", "America/Chicago");

// From components (month is 1-based)
const sd4 = fromComponents(2024, 6, 15, 14, 0, 0, "America/Chicago");
```

### Convert between timezones

```typescript
import { toTimezone, toUTC, isSameInstant } from "timezone-safe-date-utils";

const tokyo = toTimezone(meeting, "Asia/Tokyo");
const utc = toUTC(meeting);

// They all represent the same instant
isSameInstant(meeting, tokyo); // true
isSameInstant(meeting, utc);   // true
```

### Format dates

```typescript
import { formatSafe, toISOString } from "timezone-safe-date-utils";

formatSafe(meeting, "YYYY-MM-DD HH:mm:ss Z");
// => "2024-07-15 09:00:00 -04:00"

toISOString(meeting);
// => "2024-07-15T13:00:00.000Z"
```

### Date arithmetic

```typescript
import { addDays, addHours, startOfDay, endOfDay } from "timezone-safe-date-utils";

const tomorrow = addDays(meeting, 1);
const twoHoursLater = addHours(meeting, 2);
const dayStart = startOfDay(meeting);  // 00:00:00 in NYC
const dayEnd = endOfDay(meeting);      // 23:59:59 in NYC
```

### Compare dates

```typescript
import { isBefore, isAfter, diffInHours } from "timezone-safe-date-utils";

isBefore(meeting, tomorrow);       // true
isAfter(tomorrow, meeting);        // true
diffInHours(tomorrow, meeting);    // 24
```

### Validate inputs

```typescript
import { isValidTimezone, isValidDate, assertTimezone } from "timezone-safe-date-utils";

isValidTimezone("America/New_York"); // true
isValidTimezone("Fake/Zone");        // false

isValidDate("2024-06-15");          // true
isValidDate("not-a-date");          // false

assertTimezone("UTC");              // ok
assertTimezone("Nope");             // throws RangeError
```

## API Overview

| Module       | Functions                                                        |
|--------------|------------------------------------------------------------------|
| Creation     | `createSafeDate`, `now`, `fromISO`, `fromComponents`            |
| Conversion   | `toTimezone`, `toUTC`, `getOffset`, `isSameInstant`             |
| Formatting   | `formatSafe`, `toISOString`, `toLocaleDateString`, `toLocaleTimeString` |
| Comparison   | `isBefore`, `isAfter`, `isEqual`, `diffInMilliseconds`, `diffInMinutes`, `diffInHours`, `diffInDays` |
| Validation   | `isValidTimezone`, `isValidDate`, `assertTimezone`              |
| Arithmetic   | `addDays`, `addHours`, `addMinutes`, `startOfDay`, `endOfDay`   |

See [docs/api.md](docs/api.md) for the full API reference.

## Architecture

The library is built around the `SafeDate` type:

```typescript
interface SafeDate {
  utc: Date;        // The underlying UTC instant
  timezone: string; // IANA timezone identifier
  offset: number;   // UTC offset in minutes
}
```

All timezone operations use the built-in `Intl.DateTimeFormat` API with
`formatToParts()` for offset calculations. This means:

- No bundled timezone database — the runtime provides it
- Timezone rules update automatically with Node.js/browser updates
- Zero runtime dependencies

See [docs/design.md](docs/design.md) for detailed design decisions.

## Limitations

- **Pattern formatting is basic**: `formatSafe` supports `YYYY`, `MM`, `DD`, `HH`,
  `mm`, `ss`, `Z`. For complex formatting, use `Intl.DateTimeFormat` directly.
- **No calendar systems**: Only the Gregorian calendar is supported.
- **Sub-minute precision**: Offsets are rounded to the nearest minute.
- **Performance**: Each `SafeDate` creation involves an `Intl.DateTimeFormat` call.
  For hot paths, consider caching.

## Roadmap

- [ ] `addMonths` and `addYears` with end-of-month handling
- [ ] `DateRange` utilities (overlap, contains, duration)
- [ ] Recurring event support
- [ ] Performance optimizations (formatter caching)
- [ ] Additional format tokens (day of week, AM/PM, etc.)

## Development

```bash
pnpm install
pnpm build
pnpm test
pnpm lint
pnpm format
```

See [docs/development.md](docs/development.md) for the full development guide.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.
