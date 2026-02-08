import type { SafeDate } from "./types.js";
import { assertTimezone } from "./validate.js";

/**
 * Compute the UTC offset in minutes for a given timezone at a specific instant.
 * Positive values mean ahead of UTC (e.g., +60 for UTC+1).
 */
function computeOffset(timezone: string, date: Date): number {
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone: timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });

  const parts = formatter.formatToParts(date);
  const get = (type: Intl.DateTimeFormatPartTypes): string =>
    parts.find((p) => p.type === type)?.value ?? "0";

  let year = parseInt(get("year"), 10);
  const month = parseInt(get("month"), 10) - 1;
  const day = parseInt(get("day"), 10);
  let hour = parseInt(get("hour"), 10);
  const minute = parseInt(get("minute"), 10);
  const second = parseInt(get("second"), 10);

  // Intl can return hour=24 for midnight in some locales
  if (hour === 24) hour = 0;

  // Handle BC years (era)
  const era = parts.find((p) => p.type === "era");
  if (era && era.value === "BC") {
    year = -(year - 1);
  }

  // Build a UTC timestamp from the local parts
  const localAsUtc = Date.UTC(year, month, day, hour, minute, second);
  const diff = localAsUtc - date.getTime();

  // Round to nearest minute to avoid sub-minute drift
  const result = Math.round(diff / 60000);
  // Normalize -0 to 0
  return result === 0 ? 0 : result;
}

/**
 * Create a SafeDate from a Date, ISO string, or timestamp.
 */
export function createSafeDate(date: Date | string | number, timezone: string): SafeDate {
  assertTimezone(timezone);

  const d = date instanceof Date ? date : new Date(date);
  if (isNaN(d.getTime())) {
    throw new RangeError(`Invalid date value: "${date}"`);
  }

  const offset = computeOffset(timezone, d);
  return { utc: new Date(d.getTime()), timezone, offset };
}

/**
 * Create a SafeDate representing the current instant in the given timezone.
 */
export function now(timezone: string): SafeDate {
  return createSafeDate(new Date(), timezone);
}

/**
 * Create a SafeDate from an ISO 8601 string in the given timezone.
 */
export function fromISO(iso: string, timezone: string): SafeDate {
  return createSafeDate(new Date(iso), timezone);
}

/**
 * Create a SafeDate from individual date/time components in the given timezone.
 * Month is 1-based (1 = January).
 */
export function fromComponents(
  year: number,
  month: number,
  day: number,
  hour: number = 0,
  minute: number = 0,
  second: number = 0,
  timezone: string = "UTC",
): SafeDate {
  assertTimezone(timezone);

  // Build a UTC guess, then adjust for timezone offset
  const guess = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  const offset = computeOffset(timezone, guess);

  // Subtract offset to get the true UTC instant
  const utc = new Date(guess.getTime() - offset * 60000);

  // Recompute offset at the corrected instant (DST edge cases)
  const finalOffset = computeOffset(timezone, utc);
  return { utc, timezone, offset: finalOffset };
}
