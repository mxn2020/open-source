import type { RateLimitEntry, EndpointStats, TimeRange } from "./types";

const ENDPOINTS = ["/api/users", "/api/repos", "/api/search", "/api/issues", "/api/pulls"];

const ENDPOINT_LIMITS: Record<string, number> = {
  "/api/users": 5000,
  "/api/repos": 5000,
  "/api/search": 1000,
  "/api/issues": 5000,
  "/api/pulls": 5000,
};

function getTimeRangeMs(timeRange: TimeRange): number {
  switch (timeRange) {
    case "1h":
      return 60 * 60 * 1000;
    case "6h":
      return 6 * 60 * 60 * 1000;
    case "24h":
      return 24 * 60 * 60 * 1000;
    case "7d":
      return 7 * 24 * 60 * 60 * 1000;
  }
}

function getIntervalMs(timeRange: TimeRange): number {
  switch (timeRange) {
    case "1h":
      return 60 * 1000;
    case "6h":
      return 5 * 60 * 1000;
    case "24h":
      return 15 * 60 * 1000;
    case "7d":
      return 60 * 60 * 1000;
  }
}

function seededRandom(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

export function generateMockData(timeRange: TimeRange): RateLimitEntry[] {
  const now = new Date();
  const rangeMs = getTimeRangeMs(timeRange);
  const intervalMs = getIntervalMs(timeRange);
  const startTime = now.getTime() - rangeMs;
  const entries: RateLimitEntry[] = [];

  for (const endpoint of ENDPOINTS) {
    const limit = ENDPOINT_LIMITS[endpoint];
    let seed = endpoint.length * 17 + timeRange.length * 31;
    const baseLoad = 0.3 + seededRandom(seed++) * 0.4;

    for (let t = startTime; t <= now.getTime(); t += intervalMs) {
      const hourOfDay = new Date(t).getHours();
      const timeFactor = hourOfDay >= 9 && hourOfDay <= 17 ? 1.5 : 0.6;
      const noise = (seededRandom(seed++) - 0.5) * 0.2;
      const usagePercent = Math.min(0.98, Math.max(0.05, baseLoad * timeFactor + noise));
      const used = Math.round(limit * usagePercent);
      const remaining = limit - used;

      const resetTime = new Date(t + 60 * 60 * 1000);

      entries.push({
        timestamp: new Date(t).toISOString(),
        endpoint,
        remaining,
        limit,
        used,
        resetAt: resetTime.toISOString(),
      });
    }
  }

  return entries.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
}

export function getEndpointStats(data: RateLimitEntry[]): EndpointStats[] {
  const grouped = new Map<string, RateLimitEntry[]>();

  for (const entry of data) {
    const existing = grouped.get(entry.endpoint) ?? [];
    existing.push(entry);
    grouped.set(entry.endpoint, existing);
  }

  return Array.from(grouped.entries()).map(([endpoint, entries]) => {
    const usages = entries.map((e) => (e.used / e.limit) * 100);
    const totalRequests = entries.reduce((sum, e) => sum + e.used, 0);
    const avgUsage = usages.reduce((sum, u) => sum + u, 0) / usages.length;
    const peakUsage = Math.max(...usages);
    const lastEntry = entries[entries.length - 1];

    return {
      endpoint,
      totalRequests,
      avgUsage: Math.round(avgUsage * 10) / 10,
      peakUsage: Math.round(peakUsage * 10) / 10,
      currentRemaining: lastEntry.remaining,
    };
  });
}
