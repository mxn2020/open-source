import { describe, it, expect } from "vitest";
import { isValidTimezone, isValidDate, assertTimezone } from "../src/index.js";

describe("isValidTimezone", () => {
  it("returns true for UTC", () => {
    expect(isValidTimezone("UTC")).toBe(true);
  });

  it("returns true for America/New_York", () => {
    expect(isValidTimezone("America/New_York")).toBe(true);
  });

  it("returns true for Asia/Kolkata", () => {
    expect(isValidTimezone("Asia/Kolkata")).toBe(true);
  });

  it("returns false for an invalid timezone", () => {
    expect(isValidTimezone("Not/A/Timezone")).toBe(false);
  });

  it("returns false for empty string", () => {
    expect(isValidTimezone("")).toBe(false);
  });

  it("returns false for random string", () => {
    expect(isValidTimezone("foobar")).toBe(false);
  });
});

describe("isValidDate", () => {
  it("returns true for a Date object", () => {
    expect(isValidDate(new Date())).toBe(true);
  });

  it("returns false for an invalid Date", () => {
    expect(isValidDate(new Date("not-a-date"))).toBe(false);
  });

  it("returns true for a valid ISO string", () => {
    expect(isValidDate("2024-06-15T12:00:00Z")).toBe(true);
  });

  it("returns false for a non-date string", () => {
    expect(isValidDate("hello")).toBe(false);
  });

  it("returns true for a timestamp number", () => {
    expect(isValidDate(1718451600000)).toBe(true);
  });

  it("returns false for null", () => {
    expect(isValidDate(null)).toBe(false);
  });

  it("returns false for undefined", () => {
    expect(isValidDate(undefined)).toBe(false);
  });

  it("returns false for an object", () => {
    expect(isValidDate({})).toBe(false);
  });

  it("returns true for 0 (epoch)", () => {
    expect(isValidDate(0)).toBe(true);
  });
});

describe("assertTimezone", () => {
  it("does not throw for a valid timezone", () => {
    expect(() => assertTimezone("UTC")).not.toThrow();
    expect(() => assertTimezone("America/New_York")).not.toThrow();
  });

  it("throws RangeError for an invalid timezone", () => {
    expect(() => assertTimezone("Invalid/Zone")).toThrow(RangeError);
    expect(() => assertTimezone("Invalid/Zone")).toThrow('Invalid timezone: "Invalid/Zone"');
  });
});
