import type { SafeDate } from "./types.js";
import { assertTimezone } from "./validate.js";
import { createSafeDate } from "./create.js";

/**
 * Convert a SafeDate to a different timezone.
 * The underlying UTC instant stays the same; only the timezone context changes.
 */
export function toTimezone(safeDate: SafeDate, targetTimezone: string): SafeDate {
  return createSafeDate(safeDate.utc, targetTimezone);
}

/**
 * Convert a SafeDate to UTC.
 */
export function toUTC(safeDate: SafeDate): SafeDate {
  return createSafeDate(safeDate.utc, "UTC");
}

/**
 * Get the UTC offset in minutes for a timezone at a given instant (defaults to now).
 */
export function getOffset(timezone: string, date?: Date): number {
  assertTimezone(timezone);
  const d = date ?? new Date();
  const sd = createSafeDate(d, timezone);
  return sd.offset;
}

/**
 * Check whether two SafeDate values represent the same instant in time.
 */
export function isSameInstant(a: SafeDate, b: SafeDate): boolean {
  return a.utc.getTime() === b.utc.getTime();
}
