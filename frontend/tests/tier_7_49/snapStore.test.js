import { describe, it, expect } from "vitest";
import {
  snapGetSnapshot,
  setSnap,
  resetSnap,
} from "../../src/editor/transform/snapStore";

describe("snapStore", () => {
  it("stores canonical snap values", () => {
    setSnap({
      enabled: true,
      step: 0.25,
      step_degrees: 15,
      step_factor: 0.2,
      axis_lock: "z",
      orientation: "world",
    });

    const s = snapGetSnapshot().snap;
    expect(s.enabled).toBe(true);
    expect(s.step).toBe(0.25);
    expect(s.step_degrees).toBe(15);
    expect(s.step_factor).toBe(0.2);
    expect(s.axis_lock).toBe("z");
    expect(s.orientation).toBe("world");
  });

  it("clamps invalid values", () => {
    setSnap({
      step: -1,
      step_degrees: 0,
      step_factor: NaN,
      axis_lock: "bad",
      orientation: "bad",
    });

    const s = snapGetSnapshot().snap;
    expect(s.step).toBe(0.1);
    expect(s.step_degrees).toBe(5);
    expect(s.step_factor).toBe(0.1);
    expect(s.axis_lock).toBe("none");
    expect(s.orientation).toBe("local");
  });

  it("resets to defaults", () => {
    resetSnap();
    const s = snapGetSnapshot().snap;
    expect(s.enabled).toBe(false);
    expect(s.axis_lock).toBe("none");
    expect(s.orientation).toBe("local");
  });
});
