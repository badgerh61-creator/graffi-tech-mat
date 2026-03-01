// tests/tier_7_42/MaterialInspectorPanel.test.jsx
import React, { act } from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import MaterialInspectorPanel from "../../src/editor/materials/MaterialInspectorPanel";

// ✅ Mock selection store
vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "car-1::Body" }),
}));

// ✅ Mock presets API
vi.mock("../../src/services/studio/materialPresetsApi", () => ({
  fetchMaterialPresets: vi.fn(async () => [
    { id: "matte_black" },
    { id: "gloss_red" },
  ]),
}));

describe("MaterialInspectorPanel", () => {
  it("renders target and presets", async () => {
    await act(async () => {
      render(
        <MaterialInspectorPanel
          snapshot={{ decor_state: { material_overrides: {} } }}
          canEdit={true}
          onCommitTool={() => {}}
        />
      );
    });

    // Target label visible
    expect(screen.getByText(/Target:/)).toBeTruthy();

    // Presets rendered
    expect(screen.getByText("matte_black")).toBeTruthy();
    expect(screen.getByText("gloss_red")).toBeTruthy();
  });
});
