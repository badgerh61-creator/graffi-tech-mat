import { describe, it, expect } from "vitest";
import { viewModeGetSnapshot, setViewMode } from "../../src/editor/view/viewModeStore";

describe("viewModeStore", () => {
  it("defaults to studio and clamps invalid", () => {
    expect(viewModeGetSnapshot().mode).toBe("studio");
    setViewMode("nonsense");
    expect(viewModeGetSnapshot().mode).toBe("studio");
  });

  it("accepts valid modes", () => {
    setViewMode("wireframe");
    expect(viewModeGetSnapshot().mode).toBe("wireframe");
  });
});
