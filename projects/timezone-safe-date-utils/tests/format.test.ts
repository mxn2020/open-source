import { describe, it, expect } from "vitest";
import {
  createSafeDate,
  formatSafe,
  toISOString,
  toLocaleDateString,
  toLocaleTimeString,
} from "../src/index.js";

describe("formatSafe", () => {
  it("formats a date with YYYY-MM-DD pattern", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    expect(formatSafe(sd, "YYYY-MM-DD")).toBe("2024-06-15");
  });

  it("formats a date with full datetime pattern", () => {
    const sd = createSafeDate("2024-06-15T08:30:45Z", "UTC");
    expect(formatSafe(sd, "YYYY-MM-DD HH:mm:ss")).toBe("2024-06-15 08:30:45");
  });

  it("includes timezone offset with Z token", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const result = formatSafe(sd, "YYYY-MM-DDTHH:mm:ssZ");
    expect(result).toBe("2024-06-15T12:00:00+00:00");
  });

  it("shows correct local time for a non-UTC timezone", () => {
    // 2024-06-15T12:00:00Z in America/New_York (EDT, UTC-4) = 08:00
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    expect(formatSafe(sd, "HH:mm")).toBe("08:00");
  });

  it("formats with negative offset", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    const result = formatSafe(sd, "Z");
    expect(result).toBe("-04:00");
  });

  it("formats with positive non-whole-hour offset", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "Asia/Kolkata");
    const result = formatSafe(sd, "Z");
    expect(result).toBe("+05:30");
  });
});

describe("toISOString", () => {
  it("returns the UTC ISO string", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "Asia/Tokyo");
    expect(toISOString(sd)).toBe("2024-06-15T12:00:00.000Z");
  });
});

describe("toLocaleDateString", () => {
  it("formats a date string", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const result = toLocaleDateString(sd, "en-US");
    expect(result).toContain("2024");
    expect(result).toContain("06");
    expect(result).toContain("15");
  });
});

describe("toLocaleTimeString", () => {
  it("formats a time string in UTC", () => {
    const sd = createSafeDate("2024-06-15T08:30:45Z", "UTC");
    const result = toLocaleTimeString(sd, "en-US");
    expect(result).toContain("08");
    expect(result).toContain("30");
    expect(result).toContain("45");
  });

  it("formats a time string in a non-UTC timezone", () => {
    // 12:00 UTC = 08:00 EDT
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    const result = toLocaleTimeString(sd, "en-US");
    expect(result).toContain("08");
    expect(result).toContain("00");
  });
});
