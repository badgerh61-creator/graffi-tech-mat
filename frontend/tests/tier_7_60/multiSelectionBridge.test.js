import { describe, it, expect, vi } from "vitest";
import { syncPrimaryToSingleSelection } from "../../src/editor/selection/multiSelectionBridge";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  setSelectedId: vi.fn(),
  clearSelection: vi.fn(),
}));

import { setSelectedId } from "../../src/editor/selection/selectionStore";

describe("multiSelectionBridge", () => {
  it("syncs primary to single selection", () => {
    syncPrimaryToSingleSelection("obj-1");
    expect(setSelectedId).toHaveBeenCalledWith("obj-1");
  });
});
