import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Dashboard from "../../components/Dashboard";

vi.mock("recharts", () => ({
  LineChart: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Line: () => <div />,
  XAxis: () => <div />,
  YAxis: () => <div />,
  CartesianGrid: () => <div />,
  Tooltip: () => <div />,
  Legend: () => <div />,
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe("Dashboard", () => {
  it("renders summary cards", () => {
    render(<Dashboard />);

    expect(screen.getAllByText("Total Requests").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Avg Usage").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Peak Usage").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Active Endpoints")).toBeInTheDocument();
  });

  it("renders time range selector", () => {
    render(<Dashboard />);

    expect(screen.getByText("1 Hour")).toBeInTheDocument();
    expect(screen.getByText("6 Hours")).toBeInTheDocument();
    expect(screen.getByText("24 Hours")).toBeInTheDocument();
    expect(screen.getByText("7 Days")).toBeInTheDocument();
  });

  it("renders section headings", () => {
    render(<Dashboard />);

    expect(screen.getByText("Rate Limit Usage Over Time")).toBeInTheDocument();
    expect(screen.getByText("Endpoint Details")).toBeInTheDocument();
  });

  it("renders endpoint table with data", () => {
    render(<Dashboard />);

    expect(screen.getByText("/api/users")).toBeInTheDocument();
    expect(screen.getByText("/api/repos")).toBeInTheDocument();
    expect(screen.getByText("/api/search")).toBeInTheDocument();
  });
});
