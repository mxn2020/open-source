import { describe, it, expect } from "vitest";
import { generateMockData, getEndpointStats } from "../mock-data";

describe("generateMockData", () => {
  it("returns an array of rate limit entries", () => {
    const data = generateMockData("1h");
    expect(data.length).toBeGreaterThan(0);
  });

  it("includes all five endpoints", () => {
    const data = generateMockData("24h");
    const endpoints = [...new Set(data.map((d) => d.endpoint))];
    expect(endpoints).toContain("/api/users");
    expect(endpoints).toContain("/api/repos");
    expect(endpoints).toContain("/api/search");
    expect(endpoints).toContain("/api/issues");
    expect(endpoints).toContain("/api/pulls");
    expect(endpoints).toHaveLength(5);
  });

  it("has valid entry structure", () => {
    const data = generateMockData("6h");
    const entry = data[0];
    expect(entry).toHaveProperty("timestamp");
    expect(entry).toHaveProperty("endpoint");
    expect(entry).toHaveProperty("remaining");
    expect(entry).toHaveProperty("limit");
    expect(entry).toHaveProperty("used");
    expect(entry).toHaveProperty("resetAt");
  });

  it("has used + remaining equal to limit", () => {
    const data = generateMockData("1h");
    for (const entry of data) {
      expect(entry.used + entry.remaining).toBe(entry.limit);
    }
  });

  it("generates more data points for longer time ranges", () => {
    const short = generateMockData("1h");
    const long = generateMockData("7d");
    expect(long.length).toBeGreaterThan(short.length);
  });

  it("entries are sorted by timestamp", () => {
    const data = generateMockData("24h");
    for (let i = 1; i < data.length; i++) {
      expect(new Date(data[i].timestamp).getTime()).toBeGreaterThanOrEqual(
        new Date(data[i - 1].timestamp).getTime(),
      );
    }
  });
});

describe("getEndpointStats", () => {
  it("returns stats for each endpoint", () => {
    const data = generateMockData("24h");
    const stats = getEndpointStats(data);
    expect(stats).toHaveLength(5);
  });

  it("has correct stat structure", () => {
    const data = generateMockData("1h");
    const stats = getEndpointStats(data);
    const stat = stats[0];
    expect(stat).toHaveProperty("endpoint");
    expect(stat).toHaveProperty("totalRequests");
    expect(stat).toHaveProperty("avgUsage");
    expect(stat).toHaveProperty("peakUsage");
    expect(stat).toHaveProperty("currentRemaining");
  });

  it("avgUsage is between 0 and 100", () => {
    const data = generateMockData("24h");
    const stats = getEndpointStats(data);
    for (const stat of stats) {
      expect(stat.avgUsage).toBeGreaterThanOrEqual(0);
      expect(stat.avgUsage).toBeLessThanOrEqual(100);
    }
  });

  it("peakUsage is >= avgUsage", () => {
    const data = generateMockData("24h");
    const stats = getEndpointStats(data);
    for (const stat of stats) {
      expect(stat.peakUsage).toBeGreaterThanOrEqual(stat.avgUsage);
    }
  });
});
