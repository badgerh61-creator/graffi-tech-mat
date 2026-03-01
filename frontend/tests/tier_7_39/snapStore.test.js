import { describe, it, expect } from "vitest";
import { snapGetSnapshot, setSnap } from "../../src/editor/transform/snapStore";

describe("snapStore", () => {
  it("updates snap settings", () => {
    setSnap({ enabled: true, step: 0.25 });
    const s = snapGetSnapshot().snap;
    expect(s.enabled).toBe(true);
    expect(s.step).toBe(0.25);
  });
});
