import { describe, it, expect } from "vitest";
import {
  setPivotPreview,
  clearPivotPreview,
  pivotPreviewGetSnapshot,
} from "../../src/editor/transform/pivotPreviewStore";

describe("pivotPreviewStore", () => {
  it("stores preview", () => {
    setPivotPreview({ object_id: "obj-1", pivot: { x: 1, y: 2, z: 3 } });
    expect(pivotPreviewGetSnapshot().preview.object_id).toBe("obj-1");
  });

  it("clears preview", () => {
    clearPivotPreview();
    expect(pivotPreviewGetSnapshot().preview).toBe(null);
  });
});
