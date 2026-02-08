export interface RateLimitEntry {
  timestamp: string;
  endpoint: string;
  remaining: number;
  limit: number;
  used: number;
  resetAt: string;
}

export interface EndpointStats {
  endpoint: string;
  totalRequests: number;
  avgUsage: number;
  peakUsage: number;
  currentRemaining: number;
}

export type TimeRange = "1h" | "6h" | "24h" | "7d";
