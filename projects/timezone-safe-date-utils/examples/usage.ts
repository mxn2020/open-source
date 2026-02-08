/**
 * Example usage of timezone-safe-date-utils.
 *
 * Run with: npx tsx examples/usage.ts
 */

import {
  isValidTimezone,
  getTimezoneOffset,
  listCommonTimezones,
  convertTimezone,
  toUTC,
  fromUTC,
  nowIn,
  formatInTimezone,
  formatISO,
  formatRelative,
  parseISO,
  parseInTimezone,
} from "../src/index.js";

// --- Timezone validation ---
console.log("=== Timezone Validation ===");
console.log("America/New_York valid:", isValidTimezone("America/New_York"));
console.log("Fake/Zone valid:", isValidTimezone("Fake/Zone"));

// --- Timezone offset ---
console.log("\n=== Timezone Offsets ===");
const summer = new Date("2024-06-15T12:00:00Z");
console.log("NYC offset (June):", getTimezoneOffset("America/New_York", summer), "minutes");
console.log("Tokyo offset:", getTimezoneOffset("Asia/Tokyo", summer), "minutes");

// --- List common timezones ---
console.log("\n=== Common Timezones ===");
console.log(listCommonTimezones().join(", "));

// --- Convert between timezones ---
console.log("\n=== Timezone Conversion ===");
const nyNoon = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
const tokyoTime = convertTimezone(nyNoon, "America/New_York", "Asia/Tokyo");
console.log("Noon in NY → Tokyo:", tokyoTime.toISOString());

// --- To/From UTC ---
console.log("\n=== UTC Conversion ===");
const utcTime = toUTC(nyNoon, "America/New_York");
console.log("NY noon → UTC:", utcTime.toISOString());
const backToNy = fromUTC(utcTime, "America/New_York");
console.log("UTC → NY:", backToNy.toISOString());

// --- Current time in timezone ---
console.log("\n=== Current Time ===");
console.log("Now in Tokyo:", nowIn("Asia/Tokyo").toISOString());

// --- Formatting ---
console.log("\n=== Formatting ===");
const date = new Date("2024-06-15T16:00:00Z");
console.log("Formatted (NY):", formatInTimezone(date, "America/New_York", {
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hour12: true,
}));
console.log("ISO (Tokyo):", formatISO(date, "Asia/Tokyo"));
console.log("ISO (UTC):", formatISO(date, "UTC"));

const past = new Date(Date.now() - 3 * 60 * 60 * 1000);
console.log("Relative:", formatRelative(past));

// --- Parsing ---
console.log("\n=== Parsing ===");
const parsed = parseISO("2024-06-15T14:30:00+05:30");
console.log("Parsed ISO:", parsed.toISOString());

const parsedNy = parseInTimezone("2024-06-15 12:00:00", "America/New_York");
console.log("Parsed NY noon:", parsedNy.toISOString());
