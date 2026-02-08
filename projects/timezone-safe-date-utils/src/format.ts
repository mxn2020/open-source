import type { SafeDate } from "./types.js";

/**
 * Get a part value from a SafeDate using Intl.DateTimeFormat.
 */
function getPart(
  safeDate: SafeDate,
  options: Intl.DateTimeFormatOptions,
  type: Intl.DateTimeFormatPartTypes,
): string {
  const formatter = new Intl.DateTimeFormat("en-US", {
    ...options,
    timeZone: safeDate.timezone,
  });
  const parts = formatter.formatToParts(safeDate.utc);
  return parts.find((p) => p.type === type)?.value ?? "";
}

/**
 * Format a SafeDate using a simple pattern string.
 *
 * Supported tokens: YYYY, MM, DD, HH, mm, ss, Z
 */
export function formatSafe(safeDate: SafeDate, pattern: string): string {
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone: safeDate.timezone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });

  const parts = formatter.formatToParts(safeDate.utc);
  const get = (type: Intl.DateTimeFormatPartTypes): string =>
    parts.find((p) => p.type === type)?.value ?? "";

  let year = get("year");
  const month = get("month");
  const day = get("day");
  let hour = get("hour");
  const minute = get("minute");
  const second = get("second");

  // Intl may return "24" for midnight; normalize to "00"
  if (hour === "24") hour = "00";

  // Pad year to 4 digits
  year = year.padStart(4, "0");

  // Build offset string like +05:30 or -04:00 or +00:00
  const offset = safeDate.offset;
  const sign = offset >= 0 ? "+" : "-";
  const absOffset = Math.abs(offset);
  const offH = String(Math.floor(absOffset / 60)).padStart(2, "0");
  const offM = String(absOffset % 60).padStart(2, "0");
  const offsetStr = `${sign}${offH}:${offM}`;

  return pattern
    .replace("YYYY", year)
    .replace("MM", month)
    .replace("mm", minute)
    .replace("DD", day)
    .replace("HH", hour)
    .replace("ss", second)
    .replace("Z", offsetStr);
}

/**
 * Return the ISO 8601 string for the underlying UTC instant.
 */
export function toISOString(safeDate: SafeDate): string {
  return safeDate.utc.toISOString();
}

/**
 * Format the date portion in the SafeDate's timezone using a locale.
 */
export function toLocaleDateString(safeDate: SafeDate, locale?: string): string {
  return getPart(
    safeDate,
    {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    },
    // Return the whole formatted string instead of a single part
    "year",
  )
    ? new Intl.DateTimeFormat(locale ?? "en-US", {
        timeZone: safeDate.timezone,
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(safeDate.utc)
    : "";
}

/**
 * Format the time portion in the SafeDate's timezone using a locale.
 */
export function toLocaleTimeString(safeDate: SafeDate, locale?: string): string {
  return new Intl.DateTimeFormat(locale ?? "en-US", {
    timeZone: safeDate.timezone,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(safeDate.utc);
}
