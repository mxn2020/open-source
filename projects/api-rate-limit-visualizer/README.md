# API Rate Limit Visualizer

A web dashboard that visualizes API rate limit usage and patterns. Built with React, TypeScript, and Recharts, it displays real-time (mocked) rate limit data with interactive charts, helping developers understand their API consumption patterns.

## Why This Exists

When working with rate-limited APIs (GitHub, Stripe, Twitter, etc.), it's crucial to understand consumption patterns. This dashboard provides a visual representation of rate limit usage, helping you:

- Identify peak usage times
- Spot endpoints approaching their limits
- Monitor overall API health
- Plan capacity and optimize request distribution

## Features

- **Real-time visualization** — Line charts showing usage trends over time
- **Multiple time ranges** — View data for 1 hour, 6 hours, 24 hours, or 7 days
- **Endpoint breakdown** — Per-endpoint statistics and status indicators
- **Summary cards** — At-a-glance metrics for total requests, average/peak usage
- **Status badges** — Color-coded health indicators (green/yellow/red)
- **Fully local** — Uses mocked data, no external API calls needed

## Screenshots

<!-- TODO: Add screenshots of the running dashboard -->

_Screenshots coming soon — run `pnpm dev` to see the dashboard in action._

## Quick Start

```bash
# Install dependencies
pnpm install

# Start the development server
pnpm dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Architecture Overview

```
src/
├── main.tsx                 # React entry point
├── App.tsx                  # Main app shell
├── types.ts                 # TypeScript type definitions
├── mock-data.ts             # Mock data generation
└── components/
    ├── Dashboard.tsx        # Main layout with state management
    ├── SummaryCard.tsx      # Metric display card
    ├── UsageChart.tsx       # Recharts line chart
    ├── EndpointTable.tsx    # Stats table
    ├── TimeRangeSelector.tsx # Time range buttons
    └── StatusBadge.tsx      # Color-coded status indicator
```

### Key Design Decisions

- **Recharts** for charting — lightweight, React-native, good TypeScript support
- **Mocked data** — deterministic seeded random generation for consistent demos
- **Vite** — fast development server and optimized builds
- **No external API calls** — self-contained, works offline

## Scripts

| Command        | Description                  |
| -------------- | ---------------------------- |
| `pnpm dev`     | Start development server     |
| `pnpm build`   | TypeScript check + Vite build|
| `pnpm preview` | Preview production build     |
| `pnpm test`    | Run tests with Vitest        |
| `pnpm lint`    | Lint source files with ESLint|
| `pnpm format`  | Check formatting with Prettier|

## Limitations

- Data is mocked — does not connect to real APIs
- No persistent storage — data regenerates on each page load
- Charts are fixed-width (not responsive container)
- No authentication or multi-user support

## Roadmap

- [ ] Connect to real API rate limit headers
- [ ] Add responsive chart containers
- [ ] Export data as CSV/JSON
- [ ] Alert notifications for approaching limits
- [ ] Historical data persistence
- [ ] Dark mode support

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

[MIT](LICENSE) — see LICENSE file for details.
