/**
 * Date formatting utilities with timezone support.
 */

import { isValidTimezone, getTimezoneOffset } from "./zones.js";

/**
 * Format a date in a specific timezone using Intl.DateTimeFormat.
 */
export function formatInTimezone(
  date: Date,
  tz: string,
  options: Intl.DateTimeFormatOptions = {},
): string {
  if (!isValidTimezone(tz)) {
    throw new Error(`Invalid timezone: ${tz}`);
  }

  const formatter = new Intl.DateTimeFormat("en-US", {
    ...options,
    timeZone: tz,
  });

  return formatter.format(date);
}

/**
 * Format a date as an ISO 8601 string with the timezone offset.
 *
 * Example output: "2024-06-15T14:30:00+05:30"
 */
export function formatISO(date: Date, tz: string): string {
  if (!isValidTimezone(tz)) {
    throw new Error(`Invalid timezone: ${tz}`);
  }

  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: tz,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);

  const get = (type: Intl.DateTimeFormatPartTypes): string =>
    parts.find((p) => p.type === type)?.value ?? "";

  const year = get("year");
  const month = get("month");
  const day = get("day");
  let hour = get("hour");
  const minute = get("minute");
  const second = get("second");

  // Handle midnight being reported as "24"
  if (hour === "24") {
    hour = "00";
  }

  const offsetMinutes = getTimezoneOffset(tz, date);
  const offsetSign = offsetMinutes >= 0 ? "+" : "-";
  const absOffset = Math.abs(offsetMinutes);
  const offsetHours = String(Math.floor(absOffset / 60)).padStart(2, "0");
  const offsetMins = String(absOffset % 60).padStart(2, "0");
  const offsetStr =
    offsetMinutes === 0 ? "Z" : `${offsetSign}${offsetHours}:${offsetMins}`;

  return `${year}-${month}-${day}T${hour}:${minute}:${second}${offsetStr}`;
}

/**
 * Format a date as a human-readable relative time string.
 *
 * Examples: "just now", "2 hours ago", "in 3 days", "5 minutes ago"
 */
export function formatRelative(date: Date, baseDate: Date = new Date()): string {
  const diffMs = date.getTime() - baseDate.getTime();
  const absDiffMs = Math.abs(diffMs);
  const isFuture = diffMs > 0;

  const seconds = Math.floor(absDiffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const weeks = Math.floor(days / 7);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);

  let label: string;

  if (seconds < 30) {
    return "just now";
  } else if (seconds < 60) {
    label = `${seconds} seconds`;
  } else if (minutes === 1) {
    label = "1 minute";
  } else if (minutes < 60) {
    label = `${minutes} minutes`;
  } else if (hours === 1) {
    label = "1 hour";
  } else if (hours < 24) {
    label = `${hours} hours`;
  } else if (days === 1) {
    label = "1 day";
  } else if (days < 7) {
    label = `${days} days`;
  } else if (weeks === 1) {
    label = "1 week";
  } else if (weeks < 4) {
    label = `${weeks} weeks`;
  } else if (months === 1) {
    label = "1 month";
  } else if (months < 12) {
    label = `${months} months`;
  } else if (years === 1) {
    label = "1 year";
  } else {
    label = `${years} years`;
  }

  return isFuture ? `in ${label}` : `${label} ago`;
}
