import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import ObjectActionsPanel from "../../src/editor/outliner/ObjectActionsPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::MeshA" }),
}));

describe("ObjectActionsPanel", () => {
  it("emits duplicate payload", () => {
    const onCommitTool = vi.fn();

    render(
      <ObjectActionsPanel
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    fireEvent.click(screen.getByText("Duplicate Object"));

    expect(onCommitTool).toHaveBeenCalledTimes(1);
    const payload = onCommitTool.mock.calls[0][0];

    expect(payload.tool).toBe("SCENE_DUPLICATE_OBJECT");
    expect(payload.payload.object_id).toBe("obj-1");
  });

  it("emits mirror payload", () => {
    const onCommitTool = vi.fn();

    render(
      <ObjectActionsPanel
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    fireEvent.click(screen.getByText("Mirror X"));

    expect(onCommitTool).toHaveBeenCalledTimes(1);
    const payload = onCommitTool.mock.calls[0][0];

    expect(payload.tool).toBe("SCENE_MIRROR_OBJECT");
    expect(payload.payload.axis).toBe("x");
  });
});
