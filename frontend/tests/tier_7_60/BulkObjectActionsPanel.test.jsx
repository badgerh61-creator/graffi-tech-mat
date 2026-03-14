import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import BulkObjectActionsPanel from "../../src/editor/outliner/BulkObjectActionsPanel";

vi.mock("../../src/editor/selection/multiSelectionStore", () => ({
  useMultiSelection: () => ({
    selectedIds: ["obj-1", "obj-2"],
    primaryId: "obj-1",
  }),
}));

describe("BulkObjectActionsPanel", () => {
  it("emits bulk enabled tool", () => {
    const onCommitTool = vi.fn();

    render(
      <BulkObjectActionsPanel
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    fireEvent.click(screen.getByText("Hide Selected"));
    expect(onCommitTool).toHaveBeenCalledTimes(1);
    expect(onCommitTool.mock.calls[0][0].tool).toBe("SCENE_BULK_SET_ENABLED");
  });
});
