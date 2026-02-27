import { describe, it, expect, vi } from "vitest";
import { createSimulationJob } from "../../src/services/simulationApi.js";

describe("simulationApi", () => {
  it("posts correct body shape", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ job_id: 1, status: "succeeded", artifact_id: 2 }),
    });

    const res = await createSimulationJob({ snapshotId: 10, scenario: { duration_s: 1 }, token: "t" });
    expect(res.job_id).toBe(1);

    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/jobs");
    const body = JSON.parse(opts.body);
    expect(body.snapshot_id).toBe(10);
    expect(body.scenario.duration_s).toBe(1);
  });
});
