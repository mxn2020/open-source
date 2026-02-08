import { describe, it, expect } from "vitest";
import {
  isValidTimezone,
  getTimezoneOffset,
  listCommonTimezones,
} from "../src/zones.js";

describe("isValidTimezone", () => {
  it("returns true for valid IANA timezones", () => {
    expect(isValidTimezone("America/New_York")).toBe(true);
    expect(isValidTimezone("Europe/London")).toBe(true);
    expect(isValidTimezone("Asia/Tokyo")).toBe(true);
    expect(isValidTimezone("UTC")).toBe(true);
  });

  it("returns false for invalid timezone strings", () => {
    expect(isValidTimezone("Invalid/Timezone")).toBe(false);
    expect(isValidTimezone("")).toBe(false);
    expect(isValidTimezone("NotATimezone")).toBe(false);
  });
});

describe("getTimezoneOffset", () => {
  it("returns 0 for UTC", () => {
    const date = new Date("2024-06-15T12:00:00Z");
    expect(getTimezoneOffset("UTC", date)).toBe(0);
  });

  it("returns a negative offset for America/New_York in summer (EDT)", () => {
    const date = new Date("2024-06-15T12:00:00Z");
    expect(getTimezoneOffset("America/New_York", date)).toBe(-240);
  });

  it("returns a positive offset for Asia/Tokyo", () => {
    const date = new Date("2024-06-15T12:00:00Z");
    expect(getTimezoneOffset("Asia/Tokyo", date)).toBe(540);
  });

  it("throws for an invalid timezone", () => {
    expect(() => getTimezoneOffset("Invalid/Zone")).toThrow(
      "Invalid timezone",
    );
  });

  it("uses current date when no date is provided", () => {
    const offset = getTimezoneOffset("UTC");
    expect(offset).toBe(0);
  });
});

describe("listCommonTimezones", () => {
  it("returns an array of timezone strings", () => {
    const timezones = listCommonTimezones();
    expect(Array.isArray(timezones)).toBe(true);
    expect(timezones.length).toBeGreaterThan(20);
  });

  it("includes well-known timezones", () => {
    const timezones = listCommonTimezones();
    expect(timezones).toContain("America/New_York");
    expect(timezones).toContain("Europe/London");
    expect(timezones).toContain("Asia/Tokyo");
    expect(timezones).toContain("UTC");
  });

  it("returns a new array on each call (not a reference)", () => {
    const a = listCommonTimezones();
    const b = listCommonTimezones();
    expect(a).not.toBe(b);
    expect(a).toEqual(b);
  });
});
