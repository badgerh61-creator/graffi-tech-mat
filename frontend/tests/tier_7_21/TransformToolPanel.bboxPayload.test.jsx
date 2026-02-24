import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";

vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 99 } })),
}));

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({
    selectedId: "b",
    primary: { kind: "panel", id: "b" },
    secondary: [{ kind: "panel", id: "a" }],
    hovered: null,
    lastUpdatedAt: 0,
  }),
}));

import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";

describe("tier_7_21 TransformToolPanel bbox payload", () => {
  it("includes selection_bbox when multi-select", async () => {
    const { executeTool } = await import(
      "../../src/services/studio/toolExecutionAdapter"
    );

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    fireEvent.click(screen.getByTestId("transform-execute"));

    await waitFor(() => expect(executeTool).toHaveBeenCalledTimes(1));

    const call = executeTool.mock.calls[0][0];
    expect(call.payload.selected_target_ids).toEqual(["a", "b"]);
    expect(call.payload.selection_bbox).toBeTruthy();
    expect(call.payload.selection_bbox.min).toHaveProperty("x");
    expect(call.payload.selection_bbox.max).toHaveProperty("z");
  });
});
