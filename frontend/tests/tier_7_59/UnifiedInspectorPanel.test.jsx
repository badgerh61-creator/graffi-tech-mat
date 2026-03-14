import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import UnifiedInspectorPanel from "../../src/editor/inspector/UnifiedInspectorPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::MeshA" }),
}));

vi.mock("../../src/editor/decals/activeDecalStore", () => ({
  useActiveDecal: () => ({ decalId: null }),
}));

vi.mock("../../src/editor/decals/decalPlacementStore", () => ({
  useDecalPlacement: () => ({ placement: { enabled: false } }),
}));

vi.mock("../../src/editor/constraints/constraintViolationStore", () => ({
  useConstraintViolations: () => ({ violations: [] }),
}));

vi.mock("../../src/editor/materials/MaterialSlotInspectorPanel", () => ({
  default: () => <div>MaterialSlotInspectorPanel</div>,
}));

vi.mock("../../src/editor/materials/PaintLibraryPanel", () => ({
  default: () => <div>PaintLibraryPanel</div>,
}));

vi.mock("../../src/editor/decals/DecalPlacementPanel", () => ({
  default: () => <div>DecalPlacementPanel</div>,
}));

vi.mock("../../src/editor/variants/VariantSetsPanel", () => ({
  default: () => <div>VariantSetsPanel</div>,
}));

vi.mock("../../src/editor/constraints/ConstraintViolationsPanel", () => ({
  default: () => <div>ConstraintViolationsPanel</div>,
}));

vi.mock("../../src/editor/outliner/ObjectActionsPanel", () => ({
  default: () => <div>ObjectActionsPanel</div>,
}));

describe("UnifiedInspectorPanel", () => {
  it("renders unified inspector", () => {
    render(
      <UnifiedInspectorPanel
        snapshot={{ id: 1, status: "draft" }}
        toolsEnabled={true}
        lockState="owned"
        onCommitTool={vi.fn()}
      />
    );

    expect(screen.getByText("Inspector")).toBeTruthy();
    expect(screen.getByText("MaterialSlotInspectorPanel")).toBeTruthy();
    expect(screen.getByText("PaintLibraryPanel")).toBeTruthy();
    expect(screen.getByText("VariantSetsPanel")).toBeTruthy();
  });
});
