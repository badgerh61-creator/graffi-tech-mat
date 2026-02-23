import { describe, it, expect } from "vitest";
import { snapValue, snapVec3 } from "../../src/editor/gizmo/snap";

describe("Tier 7.7 — snap helpers", () => {
  it("snaps scalar deterministically", () => {
    expect(snapValue(0.12, 0.25)).toBe(0.0);
    expect(snapValue(0.13, 0.25)).toBe(0.25);
    expect(snapValue(-0.13, 0.25)).toBe(-0.25);
  });

  it("snaps vec3 deterministically", () => {
    expect(
      snapVec3({ x: 0.13, y: 0, z: 0 }, 0.25)
    ).toEqual({ x: 0.25, y: 0, z: 0 });
  });
});
