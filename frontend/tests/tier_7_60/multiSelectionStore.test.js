import { describe, it, expect } from "vitest";
import {
  clearMultiSelection,
  addToMultiSelection,
  toggleMultiSelection,
  setPrimarySelection,
  multiSelectionGetSnapshot,
} from "../../src/editor/selection/multiSelectionStore";

describe("multiSelectionStore", () => {
  it("adds unique object ids", () => {
    clearMultiSelection();
    addToMultiSelection("obj-1::MeshA", true);
    addToMultiSelection("obj-1", false);
    addToMultiSelection("obj-2", false);

    const s = multiSelectionGetSnapshot();
    expect(s.selectedIds).toEqual(["obj-1", "obj-2"]);
    expect(s.primaryId).toBe("obj-1");
  });

  it("toggles selection", () => {
    clearMultiSelection();
    toggleMultiSelection("obj-1", true);
    expect(multiSelectionGetSnapshot().selectedIds).toEqual(["obj-1"]);
    toggleMultiSelection("obj-1", true);
    expect(multiSelectionGetSnapshot().selectedIds).toEqual([]);
  });

  it("sets primary and includes it", () => {
    clearMultiSelection();
    setPrimarySelection("obj-9");
    const s = multiSelectionGetSnapshot();
    expect(s.primaryId).toBe("obj-9");
    expect(s.selectedIds).toContain("obj-9");
  });
});
