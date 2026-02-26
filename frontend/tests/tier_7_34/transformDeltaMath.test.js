import { describe, it, expect } from "vitest";
import { dominantAxisFromEulerDelta } from "../../src/editor/scene/transformDeltaMath";

describe("dominantAxisFromEulerDelta", () => {
  it("chooses the largest magnitude axis", () => {
    const r = dominantAxisFromEulerDelta({ dx: 2, dy: 10, dz: 3 });
    expect(r.axis).toBe("y");
    expect(r.degrees).toBe(10);
  });
});
