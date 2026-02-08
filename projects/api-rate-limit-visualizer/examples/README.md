# Examples

## Running the Dashboard Locally

1. Navigate to the project directory:

   ```bash
   cd projects/api-rate-limit-visualizer
   ```

2. Install dependencies:

   ```bash
   pnpm install
   ```

3. Start the development server:

   ```bash
   pnpm dev
   ```

4. Open [http://localhost:5173](http://localhost:5173) in your browser.

## What You'll See

The dashboard displays:

- **Summary cards** at the top with total requests, average usage, peak usage, and active endpoint count
- **Line chart** showing rate limit usage percentage over time for each API endpoint
- **Endpoint table** with detailed per-endpoint statistics and color-coded status badges

## Changing Time Ranges

Use the time range buttons (1 Hour, 6 Hours, 24 Hours, 7 Days) to adjust the data window. The chart and statistics update immediately.

## Screenshots

<!-- TODO: Add screenshots -->

_Run `pnpm dev` to see the dashboard in action._
