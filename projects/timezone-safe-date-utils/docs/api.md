# API Reference

Complete API documentation for `timezone-safe-date-utils`.

## Timezone Utilities

### `isValidTimezone(tz: string): boolean`

Checks whether the given string is a valid IANA timezone identifier by attempting to construct an `Intl.DateTimeFormat` with it.

**Parameters:**
- `tz` – A timezone string to validate (e.g., `"America/New_York"`).

**Returns:** `true` if valid, `false` otherwise.

**Example:**
```typescript
isValidTimezone("Europe/London"); // true
isValidTimezone("Mars/Olympus");  // false
```

---

### `getTimezoneOffset(tz: string, date?: Date): number`

Returns the UTC offset in minutes for the given timezone at the specified moment. A positive value indicates the timezone is ahead of UTC; negative means behind.

**Parameters:**
- `tz` – A valid IANA timezone identifier.
- `date` *(optional)* – The moment at which to compute the offset. Defaults to the current time.

**Returns:** Offset in minutes (e.g., `540` for UTC+9, `-240` for UTC-4).

**Throws:** `Error` if `tz` is not a valid timezone.

**Example:**
```typescript
getTimezoneOffset("Asia/Tokyo");                          // 540
getTimezoneOffset("America/New_York", new Date("2024-01-15")); // -300 (EST)
getTimezoneOffset("America/New_York", new Date("2024-06-15")); // -240 (EDT)
```

---

### `listCommonTimezones(): string[]`

Returns a curated array of common IANA timezone names. Each call returns a new array copy.

**Returns:** An array of timezone strings.

**Example:**
```typescript
const zones = listCommonTimezones();
// ["UTC", "America/New_York", "America/Chicago", ...]
```

---

## Conversion

### `convertTimezone(date: Date, fromTz: string, toTz: string): Date`

Converts a date between two timezones. Interprets the input date's UTC components as wall-clock time in `fromTz` and returns a new Date whose UTC components represent the corresponding wall-clock time in `toTz`.

**Parameters:**
- `date` – The input date.
- `fromTz` – Source timezone.
- `toTz` – Target timezone.

**Returns:** A new `Date` object.

**Throws:** `Error` if either timezone is invalid.

**Example:**
```typescript
const nyNoon = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
const tokyoTime = convertTimezone(nyNoon, "America/New_York", "Asia/Tokyo");
// tokyoTime.getUTCHours() === 1, tokyoTime.getUTCDate() === 16
```

---

### `toUTC(date: Date, sourceTz: string): Date`

Interprets the date's UTC components as a wall-clock time in `sourceTz` and returns a Date representing that moment in true UTC.

**Parameters:**
- `date` – A date whose UTC components are treated as wall-clock time.
- `sourceTz` – The timezone the wall-clock time is in.

**Returns:** A `Date` in UTC.

**Throws:** `Error` if `sourceTz` is invalid.

**Example:**
```typescript
const local = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
const utc = toUTC(local, "America/New_York");
// utc represents 2024-06-15T16:00:00Z
```

---

### `fromUTC(date: Date, targetTz: string): Date`

Converts a true UTC date to a Date whose UTC components represent the wall-clock time in the target timezone.

**Parameters:**
- `date` – A date in UTC.
- `targetTz` – The target timezone.

**Returns:** A `Date` whose UTC components are the wall-clock time in `targetTz`.

**Throws:** `Error` if `targetTz` is invalid.

**Example:**
```typescript
const utc = new Date("2024-06-15T16:00:00Z");
const ny = fromUTC(utc, "America/New_York");
// ny.getUTCHours() === 12
```

---

### `nowIn(tz: string): Date`

Returns a Date whose UTC components represent the current wall-clock time in the given timezone.

**Parameters:**
- `tz` – A valid IANA timezone.

**Returns:** A `Date` object.

**Throws:** `Error` if `tz` is invalid.

**Example:**
```typescript
const tokyoNow = nowIn("Asia/Tokyo");
```

---

## Formatting

### `formatInTimezone(date: Date, tz: string, options?: Intl.DateTimeFormatOptions): string`

Formats a date for display in a specific timezone using `Intl.DateTimeFormat`.

**Parameters:**
- `date` – The date to format.
- `tz` – The timezone for display.
- `options` *(optional)* – `Intl.DateTimeFormatOptions` to control the output format.

**Returns:** A formatted date string.

**Throws:** `Error` if `tz` is invalid.

**Example:**
```typescript
formatInTimezone(new Date("2024-06-15T16:00:00Z"), "America/New_York", {
  year: "numeric", month: "long", day: "numeric",
  hour: "2-digit", minute: "2-digit", hour12: true,
});
// "June 15, 2024 at 12:00 PM"
```

---

### `formatISO(date: Date, tz: string): string`

Formats a date as an ISO 8601 string with the timezone's UTC offset. Uses `"Z"` for UTC.

**Parameters:**
- `date` – The date to format.
- `tz` – The timezone for the output.

**Returns:** An ISO 8601 string (e.g., `"2024-06-15T12:00:00-04:00"`).

**Throws:** `Error` if `tz` is invalid.

**Example:**
```typescript
formatISO(new Date("2024-06-15T16:00:00Z"), "UTC");
// "2024-06-15T16:00:00Z"

formatISO(new Date("2024-06-15T16:00:00Z"), "America/New_York");
// "2024-06-15T12:00:00-04:00"
```

---

### `formatRelative(date: Date, baseDate?: Date): string`

Produces a human-readable relative time string comparing the given date to a base date.

**Parameters:**
- `date` – The date to describe.
- `baseDate` *(optional)* – The reference point. Defaults to `new Date()`.

**Returns:** A string like `"just now"`, `"2 hours ago"`, or `"in 3 days"`.

**Example:**
```typescript
const base = new Date("2024-06-15T12:00:00Z");
formatRelative(new Date("2024-06-15T09:00:00Z"), base); // "3 hours ago"
formatRelative(new Date("2024-06-18T12:00:00Z"), base); // "in 3 days"
```

---

## Parsing

### `parseISO(isoString: string): Date`

Parses an ISO 8601 string into a Date object using the native `Date` constructor.

**Parameters:**
- `isoString` – An ISO 8601 date string.

**Returns:** A `Date` object.

**Throws:** `Error` if the string cannot be parsed.

**Example:**
```typescript
parseISO("2024-06-15T14:30:00Z");      // 14:30 UTC
parseISO("2024-06-15T14:30:00+05:30"); // 09:00 UTC
parseISO("2024-06-15");                 // midnight UTC
```

---

### `parseInTimezone(dateStr: string, tz: string, format?: string): Date`

Parses a date string as a wall-clock time in the given timezone and returns the corresponding UTC Date.

**Parameters:**
- `dateStr` – The date string to parse.
- `tz` – The timezone the string represents.
- `format` *(optional)* – The expected format. Supported values:
  - `"YYYY-MM-DD"` – date only (time defaults to 00:00:00)
  - `"YYYY-MM-DD HH:mm:ss"` – date and time (default)

**Returns:** A `Date` in UTC.

**Throws:**
- `Error` if `tz` is invalid.
- `Error` if the format is unsupported.
- `Error` if the string doesn't match the format.

**Example:**
```typescript
parseInTimezone("2024-06-15 12:00:00", "America/New_York");
// Date representing 2024-06-15T16:00:00Z

parseInTimezone("2024-06-15", "Asia/Tokyo");
// Date representing 2024-06-14T15:00:00Z (midnight Tokyo = 15:00 UTC prev day)
```