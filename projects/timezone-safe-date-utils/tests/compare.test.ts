import { describe, it, expect } from "vitest";
import {
  createSafeDate,
  isBefore,
  isAfter,
  isEqual,
  diffInMilliseconds,
  diffInMinutes,
  diffInHours,
  diffInDays,
} from "../src/index.js";

const earlier = createSafeDate("2024-06-15T10:00:00Z", "UTC");
const later = createSafeDate("2024-06-15T12:00:00Z", "UTC");
const sameAsLater = createSafeDate("2024-06-15T12:00:00Z", "Asia/Tokyo");

describe("isBefore", () => {
  it("returns true when a is before b", () => {
    expect(isBefore(earlier, later)).toBe(true);
  });

  it("returns false when a is after b", () => {
    expect(isBefore(later, earlier)).toBe(false);
  });

  it("returns false when equal", () => {
    expect(isBefore(later, sameAsLater)).toBe(false);
  });
});

describe("isAfter", () => {
  it("returns true when a is after b", () => {
    expect(isAfter(later, earlier)).toBe(true);
  });

  it("returns false when a is before b", () => {
    expect(isAfter(earlier, later)).toBe(false);
  });
});

describe("isEqual", () => {
  it("returns true for the same instant in different timezones", () => {
    expect(isEqual(later, sameAsLater)).toBe(true);
  });

  it("returns false for different instants", () => {
    expect(isEqual(earlier, later)).toBe(false);
  });
});

describe("diffInMilliseconds", () => {
  it("returns positive diff when a is after b", () => {
    expect(diffInMilliseconds(later, earlier)).toBe(7200000);
  });

  it("returns negative diff when a is before b", () => {
    expect(diffInMilliseconds(earlier, later)).toBe(-7200000);
  });

  it("returns 0 for equal instants", () => {
    expect(diffInMilliseconds(later, sameAsLater)).toBe(0);
  });
});

describe("diffInMinutes", () => {
  it("returns correct minutes difference", () => {
    expect(diffInMinutes(later, earlier)).toBe(120);
  });
});

describe("diffInHours", () => {
  it("returns correct hours difference", () => {
    expect(diffInHours(later, earlier)).toBe(2);
  });
});

describe("diffInDays", () => {
  it("returns correct days difference", () => {
    const day1 = createSafeDate("2024-06-15T00:00:00Z", "UTC");
    const day3 = createSafeDate("2024-06-18T00:00:00Z", "UTC");
    expect(diffInDays(day3, day1)).toBe(3);
  });

  it("returns fractional days", () => {
    expect(diffInDays(later, earlier)).toBeCloseTo(2 / 24);
  });
});
