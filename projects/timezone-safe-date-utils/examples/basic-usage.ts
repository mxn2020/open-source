/**
 * Basic usage examples for timezone-safe-date-utils.
 *
 * Run with: npx tsx examples/basic-usage.ts
 */
import {
  createSafeDate,
  now,
  fromISO,
  fromComponents,
  formatSafe,
  toISOString,
  isValidTimezone,
  addDays,
  isBefore,
  diffInHours,
} from "../src/index.js";

// Create a SafeDate from an ISO string
const meeting = fromISO("2024-06-15T14:00:00Z", "America/New_York");
console.log("Meeting (UTC):", toISOString(meeting));
console.log("Meeting (NYC):", formatSafe(meeting, "YYYY-MM-DD HH:mm Z"));

// Get the current time in Tokyo
const tokyoNow = now("Asia/Tokyo");
console.log("Tokyo now:", formatSafe(tokyoNow, "YYYY-MM-DD HH:mm:ss Z"));

// Create from components
const birthday = fromComponents(1990, 12, 25, 10, 0, 0, "Europe/London");
console.log("Birthday:", formatSafe(birthday, "YYYY-MM-DD HH:mm"));

// Date arithmetic
const tomorrow = addDays(createSafeDate(new Date(), "UTC"), 1);
console.log("Tomorrow UTC:", formatSafe(tomorrow, "YYYY-MM-DD"));

// Comparison
const a = fromISO("2024-01-01T00:00:00Z", "UTC");
const b = fromISO("2024-06-01T00:00:00Z", "UTC");
console.log("Jan before Jun?", isBefore(a, b)); // true
console.log("Hours between:", diffInHours(b, a));

// Validation
console.log("Valid timezone 'UTC':", isValidTimezone("UTC"));
console.log("Valid timezone 'Fake/Zone':", isValidTimezone("Fake/Zone"));
