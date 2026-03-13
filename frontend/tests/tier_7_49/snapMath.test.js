import { describe, it, expect } from "vitest";
import {
  snapTranslateDelta,
  snapRotateDegrees,
  snapScaleFactor,
  applyAxisLockToAxis,
} from "../../src/editor/transform/snapMath";

describe("snapMath", () => {
  it("snaps translation to grid", () => {
    const r = snapTranslateDelta(
      { x: 0.26, y: 0.11, z: -0.24 },
      { enabled: true, step: 0.1, axis_lock: "none" }
    );
    expect(r.x).toBe(0.3);
    expect(r.y).toBe(0.1);
    expect(r.z).toBe(-0.2);
  });

  it("applies axis lock to translation", () => {
    const r = snapTranslateDelta(
      { x: 1, y: 2, z: 3 },
      { enabled: false, axis_lock: "y" }
    );
    expect(r.x).toBe(0);
    expect(r.y).toBe(2);
    expect(r.z).toBe(0);
  });

  it("snaps rotation degrees", () => {
    expect(snapRotateDegrees(13, { enabled: true, step_degrees: 5 })).toBe(15);
  });

  it("snaps scale factor", () => {
    expect(snapScaleFactor(1.24, { enabled: true, step_factor: 0.1 })).toBe(1.2);
  });

  it("overrides axis with lock", () => {
    expect(applyAxisLockToAxis("z", { axis_lock: "x" })).toBe("x");
  });
});
