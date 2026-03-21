import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import NumericTransformPanel from "../../src/editor/transform/NumericTransformPanel";

// ✅ Mock selection
vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::MeshA" }),
}));

describe("NumericTransformPanel", () => {
  it("renders panel", () => {
    render(
      <NumericTransformPanel
        snapshot={{ body_state: { objects: [] } }}
        canEdit={true}
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Numeric Transform")).toBeTruthy();
  });

  it("emits SCENE_SET_OBJECT_TRANSFORM with correct payload", () => {
    const onCommitTool = vi.fn();

    render(
      <NumericTransformPanel
        snapshot={{
          body_state: {
            objects: [
              {
                id: "obj-1",
                transform: {
                  pos: { x: 0, y: 0, z: 0 },
                  rot: { x: 0, y: 0, z: 0 },
                  scale: { x: 1, y: 1, z: 1 },
                },
              },
            ],
          },
        }}
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    // change X position
    const inputs = screen.getAllByRole("spinbutton");
    fireEvent.change(inputs[0], { target: { value: "5" } });

    fireEvent.click(screen.getByText("Apply Absolute"));

    expect(onCommitTool).toHaveBeenCalledTimes(1);

    const call = onCommitTool.mock.calls[0][0];

    expect(call.tool).toBe("SCENE_SET_OBJECT_TRANSFORM");
    expect(call.payload.object_id).toBe("obj-1");

    expect(call.payload.transform.pos.x).toBe(5);
    expect(call.payload.transform.pos.y).toBe(0);
    expect(call.payload.transform.pos.z).toBe(0);
  });

  it("emits SCENE_BULK_OFFSET_TRANSFORM for delta mode", () => {
    const onCommitTool = vi.fn();

    render(
      <NumericTransformPanel
        snapshot={{ body_state: { objects: [] } }}
        canEdit={true}
        onCommitTool={onCommitTool}
      />
    );

    // switch to delta mode
    fireEvent.click(screen.getByText("Delta"));

    const inputs = screen.getAllByRole("spinbutton");
    fireEvent.change(inputs[0], { target: { value: "2" } });

    fireEvent.click(screen.getByText("Apply Offset"));

    expect(onCommitTool).toHaveBeenCalledTimes(1);

    const call = onCommitTool.mock.calls[0][0];

    expect(call.tool).toBe("SCENE_BULK_OFFSET_TRANSFORM");

    expect(call.payload.delta.pos.x).toBe(2);
  });
});
