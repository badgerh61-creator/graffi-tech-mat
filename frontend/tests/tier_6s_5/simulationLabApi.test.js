import { describe, it, expect, vi } from "vitest";
import { compareMatrix } from "../../src/services/simulationLabApi";

describe("simulationLabApi", () => {
  it("posts compare/matrix body shape", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ artifact_ids: [1, 2], matrix: {} }),
    });

    const out = await compareMatrix({ artifactIds: [1, 2], token: "T" });
    expect(out.artifact_ids.length).toBe(2);

    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/compare/matrix");
    const body = JSON.parse(opts.body);
    expect(body.artifact_ids).toEqual([1, 2]);
  });
});
