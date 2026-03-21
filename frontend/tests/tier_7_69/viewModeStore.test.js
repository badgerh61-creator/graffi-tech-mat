import { describe, it, expect } from "vitest";
import { setViewMode, viewModeGetSnapshot } from "../../src/editor/view/viewModeStore";

describe("viewModeStore", () => {
  it("sets mode to wireframe", () => {
    setViewMode("wireframe");
    expect(viewModeGetSnapshot().mode).toBe("wireframe");
  });

  it("falls back to studio for invalid mode", () => {
    setViewMode("invalid-mode");
    expect(viewModeGetSnapshot().mode).toBe("studio");
  });
});
