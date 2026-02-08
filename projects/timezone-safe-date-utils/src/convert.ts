/**
 * Timezone conversion utilities.
 */

import { isValidTimezone, getTimezoneOffset } from "./zones.js";

function assertValidTz(tz: string): void {
  if (!isValidTimezone(tz)) {
    throw new Error(`Invalid timezone: ${tz}`);
  }
}

/**
 * Convert a date between timezones.
 *
 * Interprets the given Date as a wall-clock time in `fromTz` and returns
 * a new Date whose UTC value represents the same wall-clock time in `toTz`.
 */
export function convertTimezone(
  date: Date,
  fromTz: string,
  toTz: string,
): Date {
  assertValidTz(fromTz);
  assertValidTz(toTz);

  const fromOffset = getTimezoneOffset(fromTz, date);
  const toOffset = getTimezoneOffset(toTz, date);
  const diff = toOffset - fromOffset;

  return new Date(date.getTime() + diff * 60000);
}

/**
 * Convert a date to UTC from a given source timezone.
 *
 * Interprets the Date's UTC components as a wall-clock time in `sourceTz`
 * and returns a Date representing that moment in UTC.
 */
export function toUTC(date: Date, sourceTz: string): Date {
  assertValidTz(sourceTz);

  const offset = getTimezoneOffset(sourceTz, date);
  return new Date(date.getTime() - offset * 60000);
}

/**
 * Convert a UTC date to a target timezone.
 *
 * Returns a Date whose UTC components represent the wall-clock time
 * in `targetTz` at the given UTC moment.
 */
export function fromUTC(date: Date, targetTz: string): Date {
  assertValidTz(targetTz);

  const offset = getTimezoneOffset(targetTz, date);
  return new Date(date.getTime() + offset * 60000);
}

/**
 * Get the current time represented in a specific timezone.
 *
 * Returns a Date whose UTC components equal the current wall-clock
 * time in the given timezone.
 */
export function nowIn(tz: string): Date {
  assertValidTz(tz);
  return fromUTC(new Date(), tz);
}
