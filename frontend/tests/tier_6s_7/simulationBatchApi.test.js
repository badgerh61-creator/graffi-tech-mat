import { describe, it, expect, vi } from "vitest";
import { createBatch } from "../../src/services/simulationBatchApi";

describe("simulationBatchApi", () => {
  it("posts correct batch body shape", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ batch_id: 1, status: "succeeded", run_ids: [1], artifact_ids: [2] }),
    });

    const out = await createBatch({
      snapshotId: 10,
      engineVersion: "pseudo-v1",
      templateKeys: ["accel_0_60_v1"],
      token: "T",
    });

    expect(out.batch_id).toBe(1);

    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/batches");
    const body = JSON.parse(opts.body);
    expect(body.snapshot_id).toBe(10);
    expect(body.template_keys).toEqual(["accel_0_60_v1"]);
  });
});
