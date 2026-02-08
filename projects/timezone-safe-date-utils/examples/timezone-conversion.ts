/**
 * Timezone conversion examples for timezone-safe-date-utils.
 *
 * Run with: npx tsx examples/timezone-conversion.ts
 */
import {
  fromComponents,
  toTimezone,
  toUTC,
  getOffset,
  isSameInstant,
  formatSafe,
  toISOString,
} from "../src/index.js";

// Schedule a meeting at 9 AM in New York
const nycMeeting = fromComponents(2024, 7, 15, 9, 0, 0, "America/New_York");
console.log("NYC meeting:", formatSafe(nycMeeting, "YYYY-MM-DD HH:mm Z"));

// What time is that in London?
const londonTime = toTimezone(nycMeeting, "Europe/London");
console.log("London time:", formatSafe(londonTime, "YYYY-MM-DD HH:mm Z"));

// What time is that in Tokyo?
const tokyoTime = toTimezone(nycMeeting, "Asia/Tokyo");
console.log("Tokyo time:", formatSafe(tokyoTime, "YYYY-MM-DD HH:mm Z"));

// Convert to UTC
const utcTime = toUTC(nycMeeting);
console.log("UTC time:", formatSafe(utcTime, "YYYY-MM-DD HH:mm Z"));

// All represent the same instant
console.log("\nAll same instant?");
console.log("  NYC vs London:", isSameInstant(nycMeeting, londonTime));
console.log("  NYC vs Tokyo:", isSameInstant(nycMeeting, tokyoTime));
console.log("  NYC vs UTC:", isSameInstant(nycMeeting, utcTime));

// ISO strings are all identical (they're all the same UTC instant)
console.log("\nISO strings:");
console.log("  NYC:", toISOString(nycMeeting));
console.log("  London:", toISOString(londonTime));
console.log("  Tokyo:", toISOString(tokyoTime));

// Check offsets for different timezones
console.log("\nOffsets (in minutes):");
const date = new Date("2024-07-15T13:00:00Z");
console.log("  New York:", getOffset("America/New_York", date));
console.log("  London:", getOffset("Europe/London", date));
console.log("  Tokyo:", getOffset("Asia/Tokyo", date));
console.log("  Kolkata:", getOffset("Asia/Kolkata", date));

// Compare winter vs summer offsets (DST)
console.log("\nDST difference for New York:");
console.log("  January offset:", getOffset("America/New_York", new Date("2024-01-15T12:00:00Z")));
console.log("  July offset:", getOffset("America/New_York", new Date("2024-07-15T12:00:00Z")));
