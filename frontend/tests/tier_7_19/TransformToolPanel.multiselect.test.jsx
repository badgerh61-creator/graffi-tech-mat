import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import { act } from "react";
import React from "react";

vi.mock("../../src/services/studio/toolExecutionAdapter", () => {
  return {
    executeTool: vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 99 } })),
  };
});

vi.mock("../../src/editor/selection/selectionStore", async () => {
  const actual = await vi.importActual("../../src/editor/selection/selectionStore");
  return {
    ...actual,
    useSelection: () => ({
      selectedId: "b",
      primary: { kind: "panel", id: "b" },
      secondary: [{ kind: "panel", id: "a" }],
      hovered: null,
      lastUpdatedAt: 0,
    }),
  };
});

import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";
import { executeTool } from "../../src/services/studio/toolExecutionAdapter";

describe("Tier 7.19 TransformToolPanel multiselect payload", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("includes selected_target_ids + pivot_mode when multi-select", async () => {
    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByTestId("transform-execute");

    await act(async () => {
      fireEvent.click(btn);
      // flush microtasks created by async execute()
      await Promise.resolve();
      await Promise.resolve();
    });

    expect(executeTool).toHaveBeenCalledTimes(1);

    const call = executeTool.mock.calls[0][0];
    expect(call.snapshotId).toBe(10);
    expect(call.tool).toBe("TRANSLATE");
    expect(call.payload.target_id).toBe("b");
    expect(call.payload.selected_target_ids).toEqual(["a", "b"]);
    expect(call.payload.pivot_mode).toBe("bbox_center");
  });
});
