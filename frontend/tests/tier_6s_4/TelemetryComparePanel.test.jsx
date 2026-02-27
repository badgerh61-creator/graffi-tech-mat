// frontend/tests/tier_6s_4/TelemetryComparePanel.test.jsx
import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import TelemetryComparePanel from "../../src/editor/telemetry/TelemetryComparePanel";

vi.mock("../../src/utils/auth", () => ({
  getAccessToken: () => "TEST",
}));

describe("TelemetryComparePanel", () => {
  it("loads summaries and compare delta", async () => {
    global.fetch = vi
      .fn()
      // summary A
      .mockResolvedValueOnce({ ok: true, json: async () => ({ summary: { speed_avg_mps: 1.0 } }) })
      // summary B
      .mockResolvedValueOnce({ ok: true, json: async () => ({ summary: { speed_avg_mps: 2.0 } }) })
      // compare
      .mockResolvedValueOnce({ ok: true, json: async () => ({ delta: { speed_avg_mps: 1.0 } }) });

    render(<TelemetryComparePanel />);

    fireEvent.change(screen.getByLabelText("A artifact_id"), { target: { value: "1" } });
    fireEvent.change(screen.getByLabelText("B artifact_id"), { target: { value: "2" } });

    fireEvent.click(screen.getByText("Compare"));

    // ✅ wait until compare UI is rendered
    expect(await screen.findByText("Δ (B - A)")).toBeTruthy();
  });
});
