# Design Decisions

## Technology Choices

### Recharts

We chose [Recharts](https://recharts.org/) for data visualization because:

- **React-native**: Built on React components, integrating naturally with the component tree
- **Lightweight**: Smaller bundle size than alternatives like D3 or Chart.js wrappers
- **Good TypeScript support**: Well-typed APIs for type-safe chart configuration
- **Declarative API**: Charts are composed from JSX components (`<LineChart>`, `<Line>`, etc.)

### Vite

Vite provides fast development iteration with hot module replacement and optimized production builds with tree-shaking.

### Mock Data Approach

The dashboard uses deterministic mock data generation rather than connecting to real APIs:

- **Seeded random**: Uses a seeded PRNG (`Math.sin` based) for reproducible data across renders
- **Realistic patterns**: Simulates higher usage during business hours (9 AM–5 PM)
- **Multiple endpoints**: Generates distinct usage patterns for 5 API endpoints
- **Time range support**: Data density adapts to the selected time range (1-minute intervals for 1h, hourly for 7d)

This approach allows the dashboard to work offline, requires no API keys, and produces consistent demos.

## Component Architecture

- **Dashboard**: Central state management (time range selection), orchestrates child components
- **SummaryCard**: Stateless display component for a single metric
- **UsageChart**: Transforms raw data into Recharts-compatible format
- **EndpointTable**: Tabular view with integrated StatusBadge
- **TimeRangeSelector**: Button group with active state management
- **StatusBadge**: Pure function mapping usage percentage to color/label

## Data Flow

```
TimeRange (state) → generateMockData() → RateLimitEntry[]
                                        → getEndpointStats() → EndpointStats[]
                                        → UsageChart (transformed for Recharts)
                                        → EndpointTable
                                        → SummaryCards (aggregated)
```
