import React, { useMemo, useState } from "react";
import { describe, it, expect, vi } from "vitest";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";

import TelemetryViewerPanel from "../../src/editor/telemetry/TelemetryViewerPanel.jsx";

vi.mock("../../src/utils/auth", () => ({
  getAccessToken: () => "TEST",
}));

describe("TelemetryViewerPanel", () => {
  it("runs sim and renders chart", async () => {
    global.fetch = vi
      .fn()
      // create job
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ job_id: 1, status: "succeeded", artifact_id: 7 }),
      })
      // get artifact
      .mockResolvedValueOnce({
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

    render(<TelemetryViewerPanel activeSnapshot={{ id: 10 }} />);

    fireEvent.click(screen.getByRole("button", { name: /run sim/i }));

    await waitFor(() => {
      expect(screen.getByLabelText("speed-chart")).toBeTruthy();
    });

    expect(global.fetch).toHaveBeenCalledTimes(2);
  });
});
