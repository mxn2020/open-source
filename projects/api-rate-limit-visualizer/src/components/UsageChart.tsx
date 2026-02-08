import { useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import type { RateLimitEntry } from "../types";

const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#00C49F"];

interface UsageChartProps {
  data: RateLimitEntry[];
}

function UsageChart({ data }: UsageChartProps) {
  const chartData = useMemo(() => {
    const timestamps = [...new Set(data.map((d) => d.timestamp))];
    const endpoints = [...new Set(data.map((d) => d.endpoint))];

    return timestamps.map((ts) => {
      const point: Record<string, string | number> = {
        time: new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      for (const ep of endpoints) {
        const entry = data.find((d) => d.timestamp === ts && d.endpoint === ep);
        if (entry) {
          point[ep] = Math.round((entry.used / entry.limit) * 100);
        }
      }
      return point;
    });
  }, [data]);

  const endpoints = [...new Set(data.map((d) => d.endpoint))];

  return (
    <div className="usage-chart" data-testid="usage-chart">
      <LineChart width={1100} height={400} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} label={{ value: "Usage %", angle: -90 }} />
        <Tooltip />
        <Legend />
        {endpoints.map((ep, i) => (
          <Line
            key={ep}
            type="monotone"
            dataKey={ep}
            stroke={COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={2}
          />
        ))}
      </LineChart>
    </div>
  );
}

export default UsageChart;
