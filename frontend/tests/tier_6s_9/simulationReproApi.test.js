import { describe, it, expect, vi } from "vitest";
import { getRunRepro } from "../../src/services/simulationReproApi";

describe("simulationReproApi", () => {
  it("fetches /runs/{id}/repro", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ run_id: 1, run_fingerprint: "abc", verified_deterministic: true }),
    });

    const out = await getRunRepro({ runId: 1, token: "T" });
    expect(out.run_id).toBe(1);

    const [url] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/runs/1/repro");
  });
});
