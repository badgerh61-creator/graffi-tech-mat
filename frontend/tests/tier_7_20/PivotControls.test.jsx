// frontend/tests/tier_7_20/PivotControls.test.jsx
import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, fireEvent, screen, act } from "@testing-library/react";
import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";

vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 99 } })),
}));

describe("tier_7_20 pivot payload", () => {
  it("includes pivot when multi-select + custom mode", async () => {
    const { executeTool } = await import(
      "../../src/services/studio/toolExecutionAdapter"
    );

    const { clearSelection, setPrimarySelection, toggleSecondarySelection } =
      await import("../../src/editor/selection/selectionStore");

    clearSelection();
    setPrimarySelection({ kind: "panel", id: "b" });
    toggleSecondarySelection({ kind: "panel", id: "a" });

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    // pivot mode select should exist because isMulti=true
    const modeSelect = screen.getByDisplayValue("BBox Center");

    await act(async () => {
      fireEvent.change(modeSelect, { target: { value: "custom" } });
    });

    // ✅ Robust: target pivot inputs by label (SnapControls added new spinbuttons)
    const pivotX = screen.getByLabelText("X");
    const pivotY = screen.getByLabelText("Y");
    const pivotZ = screen.getByLabelText("Z");

    await act(async () => {
      fireEvent.change(pivotX, { target: { value: "1" } });
      fireEvent.change(pivotY, { target: { value: "2" } });
      fireEvent.change(pivotZ, { target: { value: "3" } });
    });

    await act(async () => {
      fireEvent.click(screen.getByTestId("transform-execute"));
    });

    const call = executeTool.mock.calls[0][0];
    expect(call.payload.selected_target_ids).toEqual(["a", "b"]);
    expect(call.payload.pivot_mode).toBe("custom");
    expect(call.payload.pivot).toEqual({ x: 1, y: 2, z: 3 });

    // (optional, but consistent with 7.24)
    expect(call.payload.snap).toEqual({ enabled: true, step: 0.25 });
  });
});
