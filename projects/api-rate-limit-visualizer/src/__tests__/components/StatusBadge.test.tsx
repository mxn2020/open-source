import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import StatusBadge from "../../components/StatusBadge";

describe("StatusBadge", () => {
  it("renders green/Healthy for low usage", () => {
    render(<StatusBadge usage={30} />);
    const badge = screen.getByText("Healthy");
    expect(badge).toBeInTheDocument();
    expect(badge.className).toContain("status-badge--green");
  });

  it("renders yellow/Warning for moderate usage", () => {
    render(<StatusBadge usage={75} />);
    const badge = screen.getByText("Warning");
    expect(badge).toBeInTheDocument();
    expect(badge.className).toContain("status-badge--yellow");
  });

  it("renders red/Critical for high usage", () => {
    render(<StatusBadge usage={95} />);
    const badge = screen.getByText("Critical");
    expect(badge).toBeInTheDocument();
    expect(badge.className).toContain("status-badge--red");
  });

  it("renders Warning at exactly 70%", () => {
    render(<StatusBadge usage={70} />);
    expect(screen.getByText("Warning")).toBeInTheDocument();
  });

  it("renders Critical at exactly 90%", () => {
    render(<StatusBadge usage={90} />);
    expect(screen.getByText("Critical")).toBeInTheDocument();
  });

  it("renders Healthy at 69%", () => {
    render(<StatusBadge usage={69} />);
    expect(screen.getByText("Healthy")).toBeInTheDocument();
  });
});
