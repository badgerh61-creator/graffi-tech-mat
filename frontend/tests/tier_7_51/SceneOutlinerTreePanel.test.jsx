import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SceneOutlinerTreePanel from "../../src/editor/outliner/SceneOutlinerTreePanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  setSelectedId: vi.fn(),
}));

describe("SceneOutlinerTreePanel", () => {
  it("renders hierarchy panel and emits create group", () => {
    const onCommitTool = vi.fn();

    render(
      <SceneOutlinerTreePanel
        snapshot={{ body_state: { objects: [] } }}
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    fireEvent.change(screen.getByPlaceholderText("Group name"), {
      target: { value: "Vehicle Group" },
    });

    fireEvent.click(screen.getByText("Create Group"));

    expect(onCommitTool).toHaveBeenCalledTimes(1);
    expect(onCommitTool.mock.calls[0][0].tool).toBe("SCENE_CREATE_GROUP");
  });
});
