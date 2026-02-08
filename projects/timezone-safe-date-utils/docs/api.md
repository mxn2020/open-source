# API Reference

## Types

### `TimezoneString`

```typescript
type TimezoneString = string;
```

An IANA timezone identifier (e.g., `"America/New_York"`, `"UTC"`).

### `SafeDate`

```typescript
interface SafeDate {
  utc: Date;
  timezone: string;
  offset: number;
}
```

- `utc` — The underlying `Date` object representing the UTC instant.
- `timezone` — The IANA timezone identifier.
- `offset` — The UTC offset in minutes (positive = ahead of UTC).

### `DateRange`

```typescript
interface DateRange {
  start: SafeDate;
  end: SafeDate;
}
```

### `FormatOptions`

```typescript
interface FormatOptions {
  locale?: string;
  includeTimezone?: boolean;
}
```

---

## Creation (`src/create.ts`)

### `createSafeDate(date, timezone)`

```typescript
function createSafeDate(date: Date | string | number, timezone: string): SafeDate;
```

Create a `SafeDate` from a `Date` object, ISO string, or Unix timestamp.

**Throws**: `RangeError` if timezone is invalid or date cannot be parsed.

### `now(timezone)`

```typescript
function now(timezone: string): SafeDate;
```

Create a `SafeDate` for the current instant in the given timezone.

### `fromISO(iso, timezone)`

```typescript
function fromISO(iso: string, timezone: string): SafeDate;
```

Create a `SafeDate` from an ISO 8601 string.

### `fromComponents(year, month, day, hour?, minute?, second?, timezone?)`

```typescript
function fromComponents(
  year: number,
  month: number,  // 1-based (1 = January)
  day: number,
  hour?: number,
  minute?: number,
  second?: number,
  timezone?: string,  // defaults to "UTC"
): SafeDate;
```

Create a `SafeDate` from individual date/time components interpreted in the given timezone.

---

## Conversion (`src/convert.ts`)

### `toTimezone(safeDate, targetTimezone)`

```typescript
function toTimezone(safeDate: SafeDate, targetTimezone: string): SafeDate;
```

Convert a `SafeDate` to a different timezone. The UTC instant is preserved.

### `toUTC(safeDate)`

```typescript
function toUTC(safeDate: SafeDate): SafeDate;
```

Convert a `SafeDate` to UTC.

### `getOffset(timezone, date?)`

```typescript
function getOffset(timezone: string, date?: Date): number;
```

Get the UTC offset in minutes for a timezone. Defaults to the current time.

### `isSameInstant(a, b)`

```typescript
function isSameInstant(a: SafeDate, b: SafeDate): boolean;
```

Check whether two `SafeDate` values represent the same instant.

---

## Formatting (`src/format.ts`)

### `formatSafe(safeDate, pattern)`

```typescript
function formatSafe(safeDate: SafeDate, pattern: string): string;
```

Format a `SafeDate` using a pattern string.

**Supported tokens**: `YYYY`, `MM`, `DD`, `HH`, `mm`, `ss`, `Z`

| Token | Description       | Example  |
|-------|-------------------|----------|
| YYYY  | 4-digit year      | 2024     |
| MM    | 2-digit month     | 06       |
| DD    | 2-digit day       | 15       |
| HH    | 2-digit hour (24) | 08       |
| mm    | 2-digit minute    | 30       |
| ss    | 2-digit second    | 45       |
| Z     | UTC offset        | +05:30   |

### `toISOString(safeDate)`

```typescript
function toISOString(safeDate: SafeDate): string;
```

Return the ISO 8601 string for the UTC instant.

### `toLocaleDateString(safeDate, locale?)`

```typescript
function toLocaleDateString(safeDate: SafeDate, locale?: string): string;
```

Format the date portion using the specified locale and timezone.

### `toLocaleTimeString(safeDate, locale?)`

```typescript
function toLocaleTimeString(safeDate: SafeDate, locale?: string): string;
```

Format the time portion using the specified locale and timezone.

---

## Comparison (`src/compare.ts`)

### `isBefore(a, b)`

```typescript
function isBefore(a: SafeDate, b: SafeDate): boolean;
```

### `isAfter(a, b)`

```typescript
function isAfter(a: SafeDate, b: SafeDate): boolean;
```

### `isEqual(a, b)`

```typescript
function isEqual(a: SafeDate, b: SafeDate): boolean;
```

### `diffInMilliseconds(a, b)`

```typescript
function diffInMilliseconds(a: SafeDate, b: SafeDate): number;
```

Returns `a - b` in milliseconds.

### `diffInMinutes(a, b)`

```typescript
function diffInMinutes(a: SafeDate, b: SafeDate): number;
```

### `diffInHours(a, b)`

```typescript
function diffInHours(a: SafeDate, b: SafeDate): number;
```

### `diffInDays(a, b)`

```typescript
function diffInDays(a: SafeDate, b: SafeDate): number;
```

---

## Validation (`src/validate.ts`)

### `isValidTimezone(timezone)`

```typescript
function isValidTimezone(timezone: string): boolean;
```

### `isValidDate(value)`

```typescript
function isValidDate(value: unknown): boolean;
```

Returns `true` if the value is a valid `Date`, parseable date string, or number.

### `assertTimezone(timezone)`

```typescript
function assertTimezone(timezone: string): void;
```

**Throws**: `RangeError` if the timezone string is invalid.

---

## Arithmetic (`src/arithmetic.ts`)

### `addDays(safeDate, days)`

```typescript
function addDays(safeDate: SafeDate, days: number): SafeDate;
```

### `addHours(safeDate, hours)`

```typescript
function addHours(safeDate: SafeDate, hours: number): SafeDate;
```

### `addMinutes(safeDate, minutes)`

```typescript
function addMinutes(safeDate: SafeDate, minutes: number): SafeDate;
```

### `startOfDay(safeDate)`

```typescript
function startOfDay(safeDate: SafeDate): SafeDate;
```

Returns midnight (00:00:00) in the SafeDate's timezone.

### `endOfDay(safeDate)`

```typescript
function endOfDay(safeDate: SafeDate): SafeDate;
```

Returns 23:59:59 in the SafeDate's timezone.
