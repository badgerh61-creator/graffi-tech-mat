import { describe, it, expect } from "vitest";
import { buildTranslatePayload } from "../../src/editor/gizmo/payloadBuilders";

describe("Tier 7.7 — payload builders", () => {
  it("builds translate payload with snap", () => {
    const p = buildTranslatePayload({
      targetId: "panel-1",
      axis: "x",
      rawDelta: { x: 0.13, y: 0, z: 0 },
      snap: { enabled: true, step: 0.25 },
    });

    expect(p.tool).toBe("TRANSLATE");
    expect(p.station).toBe("geometry");
    expect(p.payload.target_id).toBe("panel-1");
    expect(p.payload.delta.x).toBe(0.25);
  });
});
