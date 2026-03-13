import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import MaterialSlotInspectorPanel from "../../src/editor/materials/MaterialSlotInspectorPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::Body/MainMesh" }),
}));

vi.mock("../../src/editor/materials/materialSlotStore", () => ({
  useMaterialSlots: () => ({
    slotsByTarget: {
      "obj-1::Body/MainMesh": [{ name: "BodyPaint", index: 0 }],
    },
  }),
}));

vi.mock("../../src/services/studio/materialPresetsApi", () => ({
  fetchMaterialPresets: async () => [{ id: "matte_black" }, { id: "chrome" }],
}));

describe("MaterialSlotInspectorPanel", () => {
  it("renders slot inspector", async () => {
    render(
      <MaterialSlotInspectorPanel
        snapshot={{ decor_state: { material_overrides: {} } }}
        canEdit={true}
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Material Slots")).toBeTruthy();
    expect(screen.getByText(/Effective slot override/)).toBeTruthy();

    await screen.findByDisplayValue("matte_black");
  });
});
