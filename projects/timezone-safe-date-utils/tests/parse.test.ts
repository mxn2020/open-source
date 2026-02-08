import { describe, it, expect } from "vitest";
import { parseISO, parseInTimezone } from "../src/parse.js";

describe("parseISO", () => {
  it("parses a UTC ISO string", () => {
    const date = parseISO("2024-06-15T14:30:00Z");
    expect(date.getUTCFullYear()).toBe(2024);
    expect(date.getUTCMonth()).toBe(5); // June = 5
    expect(date.getUTCDate()).toBe(15);
    expect(date.getUTCHours()).toBe(14);
    expect(date.getUTCMinutes()).toBe(30);
  });

  it("parses an ISO string with positive offset", () => {
    const date = parseISO("2024-06-15T14:30:00+05:30");
    // 14:30 + 05:30 offset → 09:00 UTC
    expect(date.getUTCHours()).toBe(9);
    expect(date.getUTCMinutes()).toBe(0);
  });

  it("parses an ISO string with negative offset", () => {
    const date = parseISO("2024-06-15T14:30:00-04:00");
    // 14:30 - (-04:00) → 18:30 UTC
    expect(date.getUTCHours()).toBe(18);
    expect(date.getUTCMinutes()).toBe(30);
  });

  it("parses a date-only ISO string", () => {
    const date = parseISO("2024-06-15");
    expect(date.getUTCFullYear()).toBe(2024);
    expect(date.getUTCMonth()).toBe(5);
    expect(date.getUTCDate()).toBe(15);
  });

  it("throws for invalid ISO strings", () => {
    expect(() => parseISO("not-a-date")).toThrow("Invalid ISO 8601 string");
    expect(() => parseISO("")).toThrow("Invalid ISO 8601 string");
  });
});

describe("parseInTimezone", () => {
  it("parses a datetime string in New York timezone", () => {
    const date = parseInTimezone(
      "2024-06-15 12:00:00",
      "America/New_York",
    );
    // Noon in NY (EDT, UTC-4) should be 16:00 UTC
    expect(date.getUTCHours()).toBe(16);
    expect(date.getUTCDate()).toBe(15);
  });

  it("parses a datetime string in Tokyo timezone", () => {
    const date = parseInTimezone("2024-06-15 12:00:00", "Asia/Tokyo");
    // Noon in Tokyo (UTC+9) should be 03:00 UTC
    expect(date.getUTCHours()).toBe(3);
    expect(date.getUTCDate()).toBe(15);
  });

  it("parses a date-only string", () => {
    const date = parseInTimezone("2024-06-15", "America/New_York");
    // Midnight in NY (EDT, UTC-4) should be 04:00 UTC
    expect(date.getUTCHours()).toBe(4);
    expect(date.getUTCDate()).toBe(15);
  });

  it("parses midnight in a positive-offset timezone", () => {
    const date = parseInTimezone("2024-06-15", "Asia/Tokyo");
    // Midnight Tokyo (UTC+9) → 15:00 UTC on June 14
    expect(date.getUTCHours()).toBe(15);
    expect(date.getUTCDate()).toBe(14);
  });

  it("throws for invalid timezone", () => {
    expect(() =>
      parseInTimezone("2024-06-15 12:00:00", "Bad/Zone"),
    ).toThrow("Invalid timezone");
  });

  it("throws for unsupported format", () => {
    expect(() =>
      parseInTimezone("06/15/2024", "UTC", "MM/DD/YYYY"),
    ).toThrow("Unsupported format");
  });

  it("throws for non-matching date string", () => {
    expect(() =>
      parseInTimezone("not-a-date", "UTC"),
    ).toThrow("does not match format");
  });
});
