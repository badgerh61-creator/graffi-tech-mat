import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { getRunRepro } from "../../src/services/simulationReproApi";

describe("simulationReproApi", () => {
  const prevFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = prevFetch;
    vi.restoreAllMocks();
  });

  it("fetches /simulation/runs/{id}/repro", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        run_id: 1,
        run_fingerprint: "abc",
        verified_deterministic: true,
      }),
    });

    const out = await getRunRepro({ runId: 1, token: "T" });
    expect(out.run_id).toBe(1);

    expect(global.fetch).toHaveBeenCalledTimes(1);
    const [url, opts] = global.fetch.mock.calls[0];

    expect(String(url)).toContain("/simulation/runs/1/repro");
    expect(opts.method || "GET").toBe("GET");
    expect(opts.headers.Authorization).toBe("Bearer T");
  });

  it("throws when response not ok", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      text: async () => "not found",
    });

    await expect(getRunRepro({ runId: 123, token: "T" })).rejects.toThrow();
  });
});
