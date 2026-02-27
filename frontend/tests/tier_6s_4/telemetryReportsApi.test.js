import { describe, it, expect, vi } from "vitest";
import { compareTelemetry } from "../../src/services/telemetryReportsApi";

describe("telemetryReportsApi", () => {
  it("posts compare body shape", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ a_artifact_id: 1, b_artifact_id: 2, delta: { speed_avg_mps: 0.1 } }),
    });

    const out = await compareTelemetry({ aArtifactId: 1, bArtifactId: 2, token: "T" });
    expect(out.a_artifact_id).toBe(1);

    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/compare");
    const body = JSON.parse(opts.body);
    expect(body.a_artifact_id).toBe(1);
    expect(body.b_artifact_id).toBe(2);
  });
});
