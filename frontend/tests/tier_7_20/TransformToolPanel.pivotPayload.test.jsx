// frontend/tests/tier_7_20/TransformToolPanel.pivotPayload.test.jsx
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, fireEvent, screen, act } from "@testing-library/react";
import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";

vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 99 } })),
}));

describe("tier_7_20 TransformToolPanel pivot payload", () => {
  beforeEach(async () => {
    const { clearSelection } = await import(
      "../../src/editor/selection/selectionStore"
    );
    clearSelection();
  });

  it("sends pivot when pivot_mode=custom", async () => {
    const { executeTool } = await import(
      "../../src/services/studio/toolExecutionAdapter"
    );

    // ✅ Seed v2 selection so preflight passes and isMulti becomes true
    const { setPrimarySelection, toggleSecondarySelection } = await import(
      "../../src/editor/selection/selectionStore"
    );

    setPrimarySelection({ kind: "panel", id: "b" });
    toggleSecondarySelection({ kind: "panel", id: "a" });

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    // ✅ PivotControls should now be visible
    const modeSelect = screen.getByRole("combobox", { name: /mode/i });

    await act(async () => {
      fireEvent.change(modeSelect, { target: { value: "custom" } });
    });

    // After switching to custom, 3 pivot inputs appear (X,Y,Z)
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
  });
});
