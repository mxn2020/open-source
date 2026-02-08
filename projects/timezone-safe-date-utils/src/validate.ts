/**
 * Check whether a timezone string is a valid IANA timezone identifier.
 */
export function isValidTimezone(timezone: string): boolean {
  try {
    Intl.DateTimeFormat(undefined, { timeZone: timezone });
    return true;
  } catch {
    return false;
  }
}

/**
 * Check whether a value is a valid Date (not NaN).
 */
export function isValidDate(value: unknown): boolean {
  if (value instanceof Date) {
    return !isNaN(value.getTime());
  }
  if (typeof value === "string" || typeof value === "number") {
    const d = new Date(value);
    return !isNaN(d.getTime());
  }
  return false;
}

/**
 * Assert that a timezone string is valid. Throws a RangeError if not.
 */
export function assertTimezone(timezone: string): void {
  if (!isValidTimezone(timezone)) {
    throw new RangeError(`Invalid timezone: "${timezone}"`);
  }
}
