import { describe, it, expect, vi } from "vitest";
import { navigateToSnapshot } from "../../src/editor/history/navigateSnapshot";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  clearSelection: vi.fn(),
}));

vi.mock("../../src/editor/gizmo/gizmoPreviewStore", () => ({
  clearGizmoPreview: vi.fn(),
}));

import { clearSelection } from "../../src/editor/selection/selectionStore";
import { clearGizmoPreview } from "../../src/editor/gizmo/gizmoPreviewStore";

describe("navigateToSnapshot", () => {
  it("clears volatile UI state and updates active snapshot id", () => {
    const setActiveSnapshotId = vi.fn();

    navigateToSnapshot({ snapshotId: 42, setActiveSnapshotId });

    expect(clearGizmoPreview).toHaveBeenCalledTimes(1);
    expect(clearSelection).toHaveBeenCalledTimes(1);
    expect(setActiveSnapshotId).toHaveBeenCalledWith(42);
  });

  it("ignores non-numeric ids", () => {
    const setActiveSnapshotId = vi.fn();
    navigateToSnapshot({ snapshotId: "not-a-number", setActiveSnapshotId });
    expect(setActiveSnapshotId).toHaveBeenCalledTimes(0);
  });
});
