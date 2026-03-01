import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import PaintParamsPanel from "../../src/editor/materials/PaintParamsPanel";

vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1" }),
}));

describe("PaintParamsPanel", () => {
  it("shows message when no override exists", () => {
    render(
      <PaintParamsPanel
        snapshot={{ decor_state: { material_overrides: {} } }}
        canEdit={true}
      />
    );
    expect(screen.getByText(/Apply a preset first/)).toBeTruthy();
  });
});
