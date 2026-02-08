import { describe, it, expect } from "vitest";
import {
  formatInTimezone,
  formatISO,
  formatRelative,
} from "../src/format.js";

describe("formatInTimezone", () => {
  it("formats a date in a given timezone", () => {
    const date = new Date("2024-06-15T16:00:00Z");
    const result = formatInTimezone(date, "America/New_York", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
    // UTC 16:00 → NY 12:00 in June (EDT)
    expect(result).toContain("12:00");
  });

  it("uses default options when none are provided", () => {
    const date = new Date("2024-06-15T12:00:00Z");
    const result = formatInTimezone(date, "UTC");
    expect(typeof result).toBe("string");
    expect(result.length).toBeGreaterThan(0);
  });

  it("throws for invalid timezone", () => {
    expect(() => formatInTimezone(new Date(), "Bad/Zone")).toThrow(
      "Invalid timezone",
    );
  });
});

describe("formatISO", () => {
  it("formats a UTC date with Z suffix", () => {
    const date = new Date("2024-06-15T14:30:00Z");
    const result = formatISO(date, "UTC");
    expect(result).toBe("2024-06-15T14:30:00Z");
  });

  it("formats with a positive timezone offset", () => {
    const date = new Date("2024-06-15T03:00:00Z");
    const result = formatISO(date, "Asia/Tokyo");
    // UTC 03:00 → Tokyo 12:00 (UTC+9)
    expect(result).toBe("2024-06-15T12:00:00+09:00");
  });

  it("formats with a negative timezone offset", () => {
    const date = new Date("2024-06-15T16:30:00Z");
    const result = formatISO(date, "America/New_York");
    // UTC 16:30 → NY 12:30 (EDT, UTC-4)
    expect(result).toBe("2024-06-15T12:30:00-04:00");
  });

  it("throws for invalid timezone", () => {
    expect(() => formatISO(new Date(), "Bad/Zone")).toThrow(
      "Invalid timezone",
    );
  });
});

describe("formatRelative", () => {
  const base = new Date("2024-06-15T12:00:00Z");

  it('returns "just now" for very recent times', () => {
    const date = new Date("2024-06-15T12:00:10Z");
    expect(formatRelative(date, base)).toBe("just now");
  });

  it("formats seconds ago", () => {
    const date = new Date("2024-06-15T11:59:15Z");
    expect(formatRelative(date, base)).toBe("45 seconds ago");
  });

  it("formats minutes ago", () => {
    const date = new Date("2024-06-15T11:45:00Z");
    expect(formatRelative(date, base)).toBe("15 minutes ago");
  });

  it("formats hours ago", () => {
    const date = new Date("2024-06-15T09:00:00Z");
    expect(formatRelative(date, base)).toBe("3 hours ago");
  });

  it("formats days ago", () => {
    const date = new Date("2024-06-12T12:00:00Z");
    expect(formatRelative(date, base)).toBe("3 days ago");
  });

  it("formats future times", () => {
    const date = new Date("2024-06-18T12:00:00Z");
    expect(formatRelative(date, base)).toBe("in 3 days");
  });

  it("formats 1 minute ago", () => {
    const date = new Date("2024-06-15T11:59:00Z");
    expect(formatRelative(date, base)).toBe("1 minute ago");
  });

  it("formats 1 hour ago", () => {
    const date = new Date("2024-06-15T11:00:00Z");
    expect(formatRelative(date, base)).toBe("1 hour ago");
  });

  it("formats weeks", () => {
    const date = new Date("2024-06-01T12:00:00Z");
    expect(formatRelative(date, base)).toBe("2 weeks ago");
  });

  it("formats months", () => {
    const date = new Date("2024-03-15T12:00:00Z");
    expect(formatRelative(date, base)).toBe("3 months ago");
  });

  it("formats years", () => {
    const date = new Date("2022-06-15T12:00:00Z");
    expect(formatRelative(date, base)).toBe("2 years ago");
  });
});
