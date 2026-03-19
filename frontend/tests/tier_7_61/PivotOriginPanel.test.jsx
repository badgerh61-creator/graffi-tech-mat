import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import PivotOriginPanel from "../../src/editor/transform/PivotOriginPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::MeshA" }),
}));

vi.mock("../../src/editor/transform/pivotPreviewStore", () => ({
  setPivotPreview: vi.fn(),
  clearPivotPreview: vi.fn(),
}));

describe("PivotOriginPanel", () => {
  it("emits apply pivot tool", () => {
    const onCommitTool = vi.fn();

    render(
      <PivotOriginPanel
        snapshot={{ body_state: { objects: [{ id: "obj-1", pivot: null }] } }}
        canEdit={true}
        onCommitTool={onCommitTool}
        onRequestPivotPreset={vi.fn()}
      />
    );

    fireEvent.click(screen.getByText("Apply Pivot"));
    expect(onCommitTool).toHaveBeenCalledTimes(1);
    expect(onCommitTool.mock.calls[0][0].tool).toBe("SCENE_SET_OBJECT_PIVOT");
  });
});
