import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import EndpointTable from "../../components/EndpointTable";
import type { EndpointStats } from "../../types";

const mockStats: EndpointStats[] = [
  {
    endpoint: "/api/users",
    totalRequests: 15000,
    avgUsage: 45.2,
    peakUsage: 78.5,
    currentRemaining: 2500,
  },
  {
    endpoint: "/api/search",
    totalRequests: 800,
    avgUsage: 82.1,
    peakUsage: 95.3,
    currentRemaining: 47,
  },
];

describe("EndpointTable", () => {
  it("renders table headers", () => {
    render(<EndpointTable stats={mockStats} />);

    expect(screen.getByText("Endpoint")).toBeInTheDocument();
    expect(screen.getByText("Total Requests")).toBeInTheDocument();
    expect(screen.getByText("Avg Usage")).toBeInTheDocument();
    expect(screen.getByText("Peak Usage")).toBeInTheDocument();
    expect(screen.getByText("Remaining")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
  });

  it("renders endpoint data", () => {
    render(<EndpointTable stats={mockStats} />);

    expect(screen.getByText("/api/users")).toBeInTheDocument();
    expect(screen.getByText("/api/search")).toBeInTheDocument();
    expect(screen.getByText("45.2%")).toBeInTheDocument();
    expect(screen.getByText("95.3%")).toBeInTheDocument();
  });

  it("renders status badges", () => {
    render(<EndpointTable stats={mockStats} />);

    expect(screen.getByText("Warning")).toBeInTheDocument();
    expect(screen.getByText("Critical")).toBeInTheDocument();
  });

  it("renders empty table when no stats", () => {
    render(<EndpointTable stats={[]} />);

    expect(screen.getByText("Endpoint")).toBeInTheDocument();
    expect(screen.queryByText("/api/users")).not.toBeInTheDocument();
  });
});
