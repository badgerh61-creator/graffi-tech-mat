import { describe, it, expect, beforeEach } from "vitest";
import { setSelectedId, clearSelection, selectionGetSnapshot } from "../../src/editor/selection/selectionStore";

describe("tier_7_9 selectionStore", () => {
  beforeEach(() => {
    clearSelection();
  });

  it("sets and clears selectedId", () => {
    expect(selectionGetSnapshot().selectedId).toBe(null);

    setSelectedId("panel-1");
    expect(selectionGetSnapshot().selectedId).toBe("panel-1");

    clearSelection();
    expect(selectionGetSnapshot().selectedId).toBe(null);
  });
});
