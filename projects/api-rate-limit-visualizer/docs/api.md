# Component API Documentation

## Types

### `RateLimitEntry`

A single rate limit data point.

| Property    | Type     | Description                          |
| ----------- | -------- | ------------------------------------ |
| `timestamp` | `string` | ISO 8601 timestamp of the data point |
| `endpoint`  | `string` | API endpoint path                    |
| `remaining` | `number` | Remaining requests in the window     |
| `limit`     | `number` | Total request limit                  |
| `used`      | `number` | Requests used in the window          |
| `resetAt`   | `string` | ISO 8601 timestamp for limit reset   |

### `EndpointStats`

Aggregated statistics for a single endpoint.

| Property            | Type     | Description                          |
| ------------------- | -------- | ------------------------------------ |
| `endpoint`          | `string` | API endpoint path                    |
| `totalRequests`     | `number` | Sum of all requests in the range     |
| `avgUsage`          | `number` | Average usage percentage (0–100)     |
| `peakUsage`         | `number` | Maximum usage percentage (0–100)     |
| `currentRemaining`  | `number` | Most recent remaining count          |

### `TimeRange`

`'1h' | '6h' | '24h' | '7d'`

## Data Functions

### `generateMockData(timeRange: TimeRange): RateLimitEntry[]`

Generates mock rate limit data for all endpoints within the specified time range. Data points are sorted by timestamp. Uses seeded random generation for deterministic output.

### `getEndpointStats(data: RateLimitEntry[]): EndpointStats[]`

Computes aggregated statistics from an array of rate limit entries, grouped by endpoint.

## Components

### `<Dashboard />`

Main dashboard component. Manages time range state and renders all sub-components.

### `<SummaryCard title value subtitle />`

Displays a single metric card.

| Prop       | Type     | Description                |
| ---------- | -------- | -------------------------- |
| `title`    | `string` | Card title (e.g., "Avg Usage") |
| `value`    | `string` | Display value (e.g., "65.3%")  |
| `subtitle` | `string` | Context text               |

### `<UsageChart data />`

Line chart showing rate limit usage over time.

| Prop   | Type               | Description              |
| ------ | ------------------ | ------------------------ |
| `data` | `RateLimitEntry[]` | Array of rate limit data |

### `<EndpointTable stats />`

Table displaying per-endpoint statistics.

| Prop    | Type              | Description              |
| ------- | ----------------- | ------------------------ |
| `stats` | `EndpointStats[]` | Array of endpoint stats  |

### `<TimeRangeSelector selected onChange />`

Button group for selecting a time range.

| Prop       | Type                         | Description               |
| ---------- | ---------------------------- | ------------------------- |
| `selected` | `TimeRange`                  | Currently selected range  |
| `onChange` | `(range: TimeRange) => void` | Selection change callback |

### `<StatusBadge usage />`

Color-coded status indicator.

| Prop    | Type     | Description            |
| ------- | -------- | ---------------------- |
| `usage` | `number` | Usage percentage (0–100) |

| Usage Range | Label      | Color  |
| ----------- | ---------- | ------ |
| 0–69%       | Healthy    | Green  |
| 70–89%      | Warning    | Yellow |
| 90–100%     | Critical   | Red    |
