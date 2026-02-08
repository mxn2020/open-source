import type { EndpointStats } from "../types";
import StatusBadge from "./StatusBadge";

interface EndpointTableProps {
  stats: EndpointStats[];
}

function EndpointTable({ stats }: EndpointTableProps) {
  return (
    <div className="endpoint-table-wrapper">
      <table className="endpoint-table">
        <thead>
          <tr>
            <th>Endpoint</th>
            <th>Total Requests</th>
            <th>Avg Usage</th>
            <th>Peak Usage</th>
            <th>Remaining</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((stat) => (
            <tr key={stat.endpoint}>
              <td className="endpoint-name">{stat.endpoint}</td>
              <td>{stat.totalRequests.toLocaleString()}</td>
              <td>{stat.avgUsage}%</td>
              <td>{stat.peakUsage}%</td>
              <td>{stat.currentRemaining.toLocaleString()}</td>
              <td>
                <StatusBadge usage={stat.peakUsage} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EndpointTable;
