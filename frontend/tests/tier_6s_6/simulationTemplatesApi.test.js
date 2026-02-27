import { describe, it, expect, vi } from "vitest";
import { createScenarioFromTemplate } from "../../src/services/simulationTemplatesApi";

describe("simulationTemplatesApi", () => {
  it("posts correct create-from-template body shape", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ scenario_id: 1, scenario_hash: "abc", template_key: "accel_0_60_v1" }),
    });

    const out = await createScenarioFromTemplate({
      projectId: 9,
      name: "Baseline",
      templateKey: "accel_0_60_v1",
      engineVersion: "pseudo-v1",
      overrides: { mass_kg: 1300 },
      token: "T",
    });

    expect(out.scenario_id).toBe(1);

    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toContain("/simulation/scenarios/from-template");
    const body = JSON.parse(opts.body);
    expect(body.project_id).toBe(9);
    expect(body.template_key).toBe("accel_0_60_v1");
    expect(body.overrides.mass_kg).toBe(1300);
  });
});
