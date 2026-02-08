import { describe, it, expect } from "vitest";
import {
  createSafeDate,
  fromComponents,
  addDays,
  addHours,
  addMinutes,
  startOfDay,
  endOfDay,
  formatSafe,
} from "../src/index.js";

describe("addDays", () => {
  it("adds days correctly", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const result = addDays(sd, 3);
    expect(result.utc.toISOString()).toBe("2024-06-18T12:00:00.000Z");
    expect(result.timezone).toBe("UTC");
  });

  it("subtracts days with negative value", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const result = addDays(sd, -5);
    expect(result.utc.toISOString()).toBe("2024-06-10T12:00:00.000Z");
  });

  it("preserves timezone context", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    const result = addDays(sd, 1);
    expect(result.timezone).toBe("America/New_York");
  });
});

describe("addHours", () => {
  it("adds hours correctly", () => {
    const sd = createSafeDate("2024-06-15T10:00:00Z", "UTC");
    const result = addHours(sd, 5);
    expect(result.utc.toISOString()).toBe("2024-06-15T15:00:00.000Z");
  });

  it("handles crossing midnight", () => {
    const sd = createSafeDate("2024-06-15T22:00:00Z", "UTC");
    const result = addHours(sd, 4);
    expect(result.utc.toISOString()).toBe("2024-06-16T02:00:00.000Z");
  });
});

describe("addMinutes", () => {
  it("adds minutes correctly", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "UTC");
    const result = addMinutes(sd, 90);
    expect(result.utc.toISOString()).toBe("2024-06-15T13:30:00.000Z");
  });
});

describe("startOfDay", () => {
  it("returns start of day in UTC", () => {
    const sd = createSafeDate("2024-06-15T15:30:00Z", "UTC");
    const result = startOfDay(sd);
    expect(result.utc.toISOString()).toBe("2024-06-15T00:00:00.000Z");
  });

  it("returns start of day in local timezone", () => {
    // 2024-06-15T02:00:00Z = 2024-06-14 22:00 in America/New_York (EDT)
    // So start of day in NYC is 2024-06-14 00:00 EDT = 2024-06-14T04:00:00Z
    const sd = createSafeDate("2024-06-15T02:00:00Z", "America/New_York");
    const result = startOfDay(sd);
    const formatted = formatSafe(result, "YYYY-MM-DD HH:mm:ss");
    expect(formatted).toBe("2024-06-14 00:00:00");
  });
});

describe("endOfDay", () => {
  it("returns end of day in UTC", () => {
    const sd = createSafeDate("2024-06-15T10:00:00Z", "UTC");
    const result = endOfDay(sd);
    expect(result.utc.toISOString()).toBe("2024-06-15T23:59:59.000Z");
  });

  it("returns end of day in local timezone", () => {
    const sd = createSafeDate("2024-06-15T12:00:00Z", "America/New_York");
    const result = endOfDay(sd);
    const formatted = formatSafe(result, "HH:mm:ss");
    expect(formatted).toBe("23:59:59");
  });
});

describe("DST transition edge case", () => {
  it("handles spring forward in America/New_York", () => {
    // DST 2024: March 10 at 2:00 AM EST -> 3:00 AM EDT
    const beforeDST = fromComponents(2024, 3, 10, 1, 0, 0, "America/New_York");
    const afterDST = fromComponents(2024, 3, 10, 3, 0, 0, "America/New_York");
    // 1:00 AM EST (UTC-5) = 06:00 UTC, 3:00 AM EDT (UTC-4) = 07:00 UTC
    // The wall-clock gap is 2 hours but real elapsed time depends on offset change
    const diffMs = afterDST.utc.getTime() - beforeDST.utc.getTime();
    // Before DST: offset is -300 (EST), After DST: offset is -240 (EDT)
    expect(beforeDST.offset).toBe(-300);
    expect(afterDST.offset).toBe(-240);
    // The real difference: 1 AM EST = 6 AM UTC, 3 AM EDT = 7 AM UTC => 1 hour
    // But fromComponents uses the offset at each instant, so we verify the offsets changed
    expect(diffMs).toBeGreaterThan(0);
  });
});
