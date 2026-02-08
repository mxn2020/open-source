import { describe, it, expect } from "vitest";
import { convertTimezone, toUTC, fromUTC, nowIn } from "../src/convert.js";

describe("toUTC", () => {
  it("converts a New York time to UTC in summer (EDT = UTC-4)", () => {
    // 2024-06-15 12:00:00 UTC interpreted as New York wall-clock
    const nyNoon = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
    const utc = toUTC(nyNoon, "America/New_York");
    // New York is UTC-4 in June, so noon NY = 16:00 UTC
    expect(utc.getUTCHours()).toBe(16);
  });

  it("converts a Tokyo time to UTC (JST = UTC+9)", () => {
    const tokyoNoon = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
    const utc = toUTC(tokyoNoon, "Asia/Tokyo");
    // Tokyo is UTC+9, so noon Tokyo = 03:00 UTC
    expect(utc.getUTCHours()).toBe(3);
  });

  it("throws for invalid timezone", () => {
    expect(() => toUTC(new Date(), "Bad/Zone")).toThrow("Invalid timezone");
  });
});

describe("fromUTC", () => {
  it("converts UTC to New York time in summer", () => {
    const utcNoon = new Date(Date.UTC(2024, 5, 15, 16, 0, 0));
    const ny = fromUTC(utcNoon, "America/New_York");
    // UTC 16:00 in June → NY 12:00 (UTC-4)
    expect(ny.getUTCHours()).toBe(12);
  });

  it("converts UTC to Tokyo time", () => {
    const utcDate = new Date(Date.UTC(2024, 5, 15, 3, 0, 0));
    const tokyo = fromUTC(utcDate, "Asia/Tokyo");
    // UTC 03:00 → Tokyo 12:00 (UTC+9)
    expect(tokyo.getUTCHours()).toBe(12);
  });
});

describe("convertTimezone", () => {
  it("converts from New York to Tokyo", () => {
    const date = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
    const result = convertTimezone(date, "America/New_York", "Asia/Tokyo");
    // Tokyo is 13 hours ahead of New York in summer
    expect(result.getUTCHours()).toBe(1);
    expect(result.getUTCDate()).toBe(16);
  });

  it("returns the same time when from and to are the same", () => {
    const date = new Date(Date.UTC(2024, 5, 15, 12, 0, 0));
    const result = convertTimezone(date, "Europe/London", "Europe/London");
    expect(result.getTime()).toBe(date.getTime());
  });

  it("throws for invalid source timezone", () => {
    expect(() =>
      convertTimezone(new Date(), "Bad/Zone", "UTC"),
    ).toThrow("Invalid timezone");
  });

  it("throws for invalid target timezone", () => {
    expect(() =>
      convertTimezone(new Date(), "UTC", "Bad/Zone"),
    ).toThrow("Invalid timezone");
  });
});

describe("nowIn", () => {
  it("returns a Date object", () => {
    const result = nowIn("America/New_York");
    expect(result).toBeInstanceOf(Date);
  });

  it("returns a time close to now", () => {
    const result = nowIn("UTC");
    const now = new Date();
    const diffMs = Math.abs(result.getTime() - now.getTime());
    expect(diffMs).toBeLessThan(2000);
  });

  it("throws for invalid timezone", () => {
    expect(() => nowIn("Bad/Zone")).toThrow("Invalid timezone");
  });
});
