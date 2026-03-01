import { describe, it, expect } from "vitest";
import { decalPreviewGetSnapshot, setDecalPreviewPatch, clearDecalPreviewPatch } from "../../src/editor/decals/decalPreviewStore";

describe("decalPreviewStore", () => {
  it("stores preview patch by id", () => {
    setDecalPreviewPatch("dec-1", { position: { x: 1, y: 0, z: 0 } });
    expect(decalPreviewGetSnapshot().patchById["dec-1"].position.x).toBe(1);
    clearDecalPreviewPatch("dec-1");
    expect(decalPreviewGetSnapshot().patchById["dec-1"]).toBeUndefined();
  });
});
