// frontend/tests/tier_6s_3/TelemetryAdvancedPanel.test.jsx
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import TelemetryAdvancedPanel from "../../src/editor/telemetry/TelemetryAdvancedPanel";
import { clearArtifacts } from "../../src/editor/telemetry/telemetryStore";

vi.mock("../../src/utils/auth", () => ({ getAccessToken: () => "TEST" }));

describe("TelemetryAdvancedPanel", () => {
  beforeEach(() => {
    clearArtifacts();
    vi.restoreAllMocks();
  });

  it("loads an artifact and renders curve chart", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        artifact_id: 7,
        snapshot_id: 10,
        engine_version: "pseudo-v1",
        timestep_s: 0.1,
        duration_s: 10,
        curves: { time_s: [0, 1], speed_mps: [0, 2] },
      }),
    });

    render(<TelemetryAdvancedPanel />);

    fireEvent.change(screen.getByPlaceholderText("artifact id"), {
      target: { value: "7" },
    });
    fireEvent.click(screen.getByText("Load Artifact"));

    // ✅ multiple "speed_mps" appear (toggle label + chart header)
    const hits = await screen.findAllByText("speed_mps");
    expect(hits.length).toBeGreaterThanOrEqual(2);

    // ✅ chart should be present
    expect(screen.getByLabelText("chart-speed_mps")).toBeTruthy();
  });
});
