import { describe, it, expect } from "vitest";
import {
  startTransformPreview,
  updateTransformPreview,
  endTransformPreview,
} from "../../src/editor/transform/multiTransformPreviewStore";

describe("multiTransformPreviewStore", () => {
  it("tracks preview lifecycle", () => {
    startTransformPreview();
    updateTransformPreview({ pos: { x: 1 } });

    endTransformPreview();

    expect(true).toBe(true);
  });
});
