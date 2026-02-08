import { describe, it, expect } from "vitest";
import { createSafeDate, toTimezone, toUTC, getOffset, isSameInstant } from "../src/index.js";

describe("toTimezone", () => {
  it("converts to a new timezone while preserving the UTC instant", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const converted = toTimezone(sd, "America/New_York");
    expect(converted.utc.getTime()).toBe(sd.utc.getTime());
    expect(converted.timezone).toBe("America/New_York");
    expect(converted.offset).toBe(-240); // EDT
  });

  it("throws on invalid target timezone", () => {
    const sd = createSafeDate("2024-01-01T00:00:00Z", "UTC");
    expect(() => toTimezone(sd, "Fake/Zone")).toThrow("Invalid timezone");
  });
});

describe("toUTC", () => {
  it("converts any SafeDate to UTC", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "Asia/Tokyo");
    const utc = toUTC(sd);
    expect(utc.timezone).toBe("UTC");
    expect(utc.offset).toBe(0);
    expect(utc.utc.getTime()).toBe(sd.utc.getTime());
  });
});

describe("getOffset", () => {
  it("returns 0 for UTC", () => {
    expect(getOffset("UTC")).toBe(0);
  });

  it("returns correct offset for Asia/Kolkata", () => {
    expect(getOffset("Asia/Kolkata", new Date("2024-06-15T00:00:00Z"))).toBe(330);
  });

  it("returns winter offset for America/New_York in January", () => {
    expect(getOffset("America/New_York", new Date("2024-01-15T12:00:00Z"))).toBe(-300);
  });

  it("returns summer offset for America/New_York in July", () => {
    expect(getOffset("America/New_York", new Date("2024-07-15T12:00:00Z"))).toBe(-240);
  });

  it("throws on invalid timezone", () => {
    expect(() => getOffset("Invalid/TZ")).toThrow("Invalid timezone");
  });
});

describe("isSameInstant", () => {
  it("returns true for the same instant in different timezones", () => {
    const a = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const b = createSafeDate("2024-06-15T12:00:00Z", "Asia/Tokyo");
    expect(isSameInstant(a, b)).toBe(true);
  });

  it("returns false for different instants", () => {
    const a = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const b = createSafeDate("2024-06-15T13:00:00Z", "UTC");
    expect(isSameInstant(a, b)).toBe(false);
  });
});
