import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SceneOutlinerPanel from "../../src/editor/outliner/SceneOutlinerPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  setSelectedId: vi.fn(),
}));

describe("SceneOutlinerPanel", () => {
  it("renders objects and emits enabled toggle tool", () => {
    const onCommitTool = vi.fn();

    render(
      <SceneOutlinerPanel
        snapshot={{
          body_state: {
            objects: [
              {
                id: "obj-1",
                name: "Car",
                kind: "model_ref",
                enabled: true,
                layers: ["default"],
              },
            ],
          },
        }}
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    expect(screen.getByText("Scene Outliner")).toBeTruthy();
    expect(screen.getByText("Car")).toBeTruthy();

    fireEvent.click(screen.getByLabelText("visible"));

    expect(onCommitTool).toHaveBeenCalled();
    expect(onCommitTool.mock.calls[0][0].tool).toBe("SCENE_SET_OBJECT_ENABLED");
  });
});
