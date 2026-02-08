import { describe, it, expect } from "vitest";
import { createSafeDate, now, fromISO, fromComponents } from "../src/index.js";

describe("createSafeDate", () => {
  it("creates a SafeDate from a Date object", () => {
    const date = new Date("2024-06-15T12:00:00Z");
    const sd = createSafeDate(date, "America/New_York");
    expect(sd.utc.getTime()).toBe(date.getTime());
    expect(sd.timezone).toBe("America/New_York");
    expect(typeof sd.offset).toBe("number");
  });

  it("creates a SafeDate from an ISO string", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "Europe/London");
    expect(sd.utc.toISOString()).toBe("2024-06-15T12:00:00.000Z");
    expect(sd.timezone).toBe("Europe/London");
  });

  it("creates a SafeDate from a timestamp number", () => {
    const ts = Date.UTC(2024, 0, 1);
    const sd = createSafeDate(ts, "UTC");
    expect(sd.utc.getTime()).toBe(ts);
    expect(sd.offset).toBe(0);
  });

  it("throws on invalid timezone", () => {
    expect(() => createSafeDate(new Date(), "Not/Real")).toThrow("Invalid timezone");
  });

  it("throws on invalid date value", () => {
    expect(() => createSafeDate("not-a-date", "UTC")).toThrow("Invalid date");
  });

  it("computes correct offset for UTC", () => {
    const sd = createSafeDate("2024-01-01T00:00:00Z", "UTC");
    expect(sd.offset).toBe(0);
  });

  it("computes a non-zero offset for non-UTC timezones", () => {
    // In summer, America/New_York is UTC-4
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    expect(sd.offset).toBe(-240);
  });

  it("computes correct offset for positive-offset timezone", () => {
    // Asia/Kolkata is always UTC+5:30
    const sd = createSafeDate("2024-06-15T12:00:00Z", "Asia/Kolkata");
    expect(sd.offset).toBe(330);
  });
});

describe("now", () => {
  it("returns a SafeDate close to current time", () => {
    const before = Date.now();
    const sd = now("UTC");
    const after = Date.now();
    expect(sd.utc.getTime()).toBeGreaterThanOrEqual(before);
    expect(sd.utc.getTime()).toBeLessThanOrEqual(after);
    expect(sd.timezone).toBe("UTC");
  });
});

describe("fromISO", () => {
  it("parses an ISO string correctly", () => {
    const sd = fromISO("2024-03-10T07:00:00Z", "America/Los_Angeles");
    expect(sd.utc.toISOString()).toBe("2024-03-10T07:00:00.000Z");
    expect(sd.timezone).toBe("America/Los_Angeles");
  });

  it("throws on invalid ISO string", () => {
    expect(() => fromISO("garbage", "UTC")).toThrow("Invalid date");
  });
});

describe("fromComponents", () => {
  it("creates a SafeDate from components in UTC", () => {
    const sd = fromComponents(2024, 6, 15, 12, 30, 0, "UTC");
    expect(sd.utc.toISOString()).toBe("2024-06-15T12:30:00.000Z");
  });

  it("creates a SafeDate from components in a non-UTC timezone", () => {
    // 2024-06-15 12:00 in America/New_York (EDT, UTC-4) = 16:00 UTC
    const sd = fromComponents(2024, 6, 15, 12, 0, 0, "America/New_York");
    expect(sd.utc.toISOString()).toBe("2024-06-15T16:00:00.000Z");
  });

  it("defaults to UTC when timezone is omitted", () => {
    const sd = fromComponents(2024, 1, 1);
    expect(sd.timezone).toBe("UTC");
    expect(sd.utc.toISOString()).toBe("2024-01-01T00:00:00.000Z");
  });

  it("handles timezone with non-whole-hour offset", () => {
    // Asia/Kolkata is UTC+5:30
    const sd = fromComponents(2024, 6, 15, 12, 0, 0, "Asia/Kolkata");
    expect(sd.utc.toISOString()).toBe("2024-06-15T06:30:00.000Z");
  });

  it("throws on invalid timezone", () => {
    expect(() => fromComponents(2024, 1, 1, 0, 0, 0, "Invalid/Zone")).toThrow("Invalid timezone");
  });
});
