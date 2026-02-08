import type { SafeDate } from "./types.js";
import { createSafeDate, fromComponents } from "./create.js";
import { formatSafe } from "./format.js";

/**
 * Add a number of days to a SafeDate, preserving timezone context.
 */
export function addDays(safeDate: SafeDate, days: number): SafeDate {
  const ms = safeDate.utc.getTime() + days * 86400000;
  return createSafeDate(new Date(ms), safeDate.timezone);
}

/**
 * Add a number of hours to a SafeDate, preserving timezone context.
 */
export function addHours(safeDate: SafeDate, hours: number): SafeDate {
  const ms = safeDate.utc.getTime() + hours * 3600000;
  return createSafeDate(new Date(ms), safeDate.timezone);
}

/**
 * Add a number of minutes to a SafeDate, preserving timezone context.
 */
export function addMinutes(safeDate: SafeDate, minutes: number): SafeDate {
  const ms = safeDate.utc.getTime() + minutes * 60000;
  return createSafeDate(new Date(ms), safeDate.timezone);
}

/**
 * Get the start of the day (00:00:00) in the SafeDate's timezone.
 */
export function startOfDay(safeDate: SafeDate): SafeDate {
  const formatted = formatSafe(safeDate, "YYYY-MM-DD");
  const [yearStr, monthStr, dayStr] = formatted.split("-");
  return fromComponents(
    parseInt(yearStr, 10),
    parseInt(monthStr, 10),
    parseInt(dayStr, 10),
    0,
    0,
    0,
    safeDate.timezone,
  );
}

/**
 * Get the end of the day (23:59:59) in the SafeDate's timezone.
 */
export function endOfDay(safeDate: SafeDate): SafeDate {
  const formatted = formatSafe(safeDate, "YYYY-MM-DD");
  const [yearStr, monthStr, dayStr] = formatted.split("-");
  return fromComponents(
    parseInt(yearStr, 10),
    parseInt(monthStr, 10),
    parseInt(dayStr, 10),
    23,
    59,
    59,
    safeDate.timezone,
  );
}
