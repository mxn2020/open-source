import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import SummaryCard from "../../components/SummaryCard";

describe("SummaryCard", () => {
  it("renders title, value, and subtitle", () => {
    render(<SummaryCard title="Total Requests" value="12,345" subtitle="In the last 24h" />);

    expect(screen.getByText("Total Requests")).toBeInTheDocument();
    expect(screen.getByText("12,345")).toBeInTheDocument();
    expect(screen.getByText("In the last 24h")).toBeInTheDocument();
  });

  it("renders percentage values", () => {
    render(<SummaryCard title="Avg Usage" value="65.3%" subtitle="Across all endpoints" />);

    expect(screen.getByText("Avg Usage")).toBeInTheDocument();
    expect(screen.getByText("65.3%")).toBeInTheDocument();
  });
});
