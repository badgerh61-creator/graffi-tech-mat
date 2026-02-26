import { describe, it, expect } from "vitest";
import { gizmoModeGetSnapshot, setGizmoMode } from "../../src/editor/gizmo/gizmoModeStore";

describe("gizmoModeStore", () => {
  it("defaults to translate", () => {
    expect(gizmoModeGetSnapshot().mode).toBe("translate");
  });

  it("clamps invalid mode to translate", () => {
    setGizmoMode("nonsense");
    expect(gizmoModeGetSnapshot().mode).toBe("translate");
  });

  it("accepts rotate/scale", () => {
    setGizmoMode("rotate");
    expect(gizmoModeGetSnapshot().mode).toBe("rotate");
    setGizmoMode("scale");
    expect(gizmoModeGetSnapshot().mode).toBe("scale");
  });
});
