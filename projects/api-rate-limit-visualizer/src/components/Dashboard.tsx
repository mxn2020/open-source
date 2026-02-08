import { useState, useMemo } from "react";
import type { TimeRange } from "../types";
import { generateMockData, getEndpointStats } from "../mock-data";
import TimeRangeSelector from "./TimeRangeSelector";
import SummaryCard from "./SummaryCard";
import UsageChart from "./UsageChart";
import EndpointTable from "./EndpointTable";

function Dashboard() {
  const [timeRange, setTimeRange] = useState<TimeRange>("24h");

  const data = useMemo(() => generateMockData(timeRange), [timeRange]);
  const stats = useMemo(() => getEndpointStats(data), [data]);

  const totalRequests = stats.reduce((sum, s) => sum + s.totalRequests, 0);
  const avgUsage =
    stats.length > 0
      ? Math.round((stats.reduce((sum, s) => sum + s.avgUsage, 0) / stats.length) * 10) / 10
      : 0;
  const peakUsage = stats.length > 0 ? Math.max(...stats.map((s) => s.peakUsage)) : 0;
  const activeEndpoints = stats.length;

  return (
    <div className="dashboard">
      <div className="dashboard-controls">
        <TimeRangeSelector selected={timeRange} onChange={setTimeRange} />
      </div>

      <div className="summary-cards">
        <SummaryCard
          title="Total Requests"
          value={totalRequests.toLocaleString()}
          subtitle={`In the last ${timeRange}`}
        />
        <SummaryCard title="Avg Usage" value={`${avgUsage}%`} subtitle="Across all endpoints" />
        <SummaryCard title="Peak Usage" value={`${peakUsage}%`} subtitle="Highest observed" />
        <SummaryCard
          title="Active Endpoints"
          value={String(activeEndpoints)}
          subtitle="Being monitored"
        />
      </div>

      <section className="chart-section">
        <h2>Rate Limit Usage Over Time</h2>
        <UsageChart data={data} />
      </section>

      <section className="table-section">
        <h2>Endpoint Details</h2>
        <EndpointTable stats={stats} />
      </section>
    </div>
  );
}

export default Dashboard;
