/**
 * Date parsing utilities with timezone support.
 */

import { isValidTimezone, getTimezoneOffset } from "./zones.js";

/**
 * Parse an ISO 8601 string into a Date object.
 *
 * Supports formats like:
 *   "2024-06-15T14:30:00Z"
 *   "2024-06-15T14:30:00+05:30"
 *   "2024-06-15T14:30:00-04:00"
 *   "2024-06-15"
 */
export function parseISO(isoString: string): Date {
  const date = new Date(isoString);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid ISO 8601 string: ${isoString}`);
  }
  return date;
}

const FORMAT_PATTERNS: Record<string, RegExp> = {
  "YYYY-MM-DD": /^(\d{4})-(\d{2})-(\d{2})$/,
  "YYYY-MM-DD HH:mm:ss": /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/,
};

/**
 * Parse a date string assuming it represents a wall-clock time in the
 * given timezone, and return the corresponding UTC Date.
 *
 * Supported formats:
 *   - "YYYY-MM-DD" (time defaults to 00:00:00)
 *   - "YYYY-MM-DD HH:mm:ss"
 */
export function parseInTimezone(
  dateStr: string,
  tz: string,
  format: string = "YYYY-MM-DD HH:mm:ss",
): Date {
  if (!isValidTimezone(tz)) {
    throw new Error(`Invalid timezone: ${tz}`);
  }

  // Try date-only format first if the string matches
  const dateOnlyMatch = FORMAT_PATTERNS["YYYY-MM-DD"].exec(dateStr);
  if (dateOnlyMatch) {
    const [, year, month, day] = dateOnlyMatch;
    const utcDate = new Date(
      Date.UTC(Number(year), Number(month) - 1, Number(day), 0, 0, 0),
    );
    const offset = getTimezoneOffset(tz, utcDate);
    return new Date(utcDate.getTime() - offset * 60000);
  }

  // Try datetime format
  const pattern = FORMAT_PATTERNS[format];
  if (!pattern) {
    throw new Error(`Unsupported format: ${format}`);
  }

  const match = pattern.exec(dateStr);
  if (!match) {
    throw new Error(
      `Date string "${dateStr}" does not match format "${format}"`,
    );
  }

  const [, year, month, day, hour, minute, second] = match;
  const utcDate = new Date(
    Date.UTC(
      Number(year),
      Number(month) - 1,
      Number(day),
      Number(hour),
      Number(minute),
      Number(second),
    ),
  );

  const offset = getTimezoneOffset(tz, utcDate);
  return new Date(utcDate.getTime() - offset * 60000);
}
