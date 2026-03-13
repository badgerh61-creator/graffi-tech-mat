import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";

import ToolContextBar from "../../src/editor/toolbar/ToolContextBar";

// Mock selection
vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({ selectedId: "obj-1::MeshA" }),
}));

// Mock gizmo mode
vi.mock("../../src/editor/gizmo/gizmoModeStore", () => ({
  useGizmoMode: () => ({ mode: "translate" }),
  setGizmoMode: () => {},
}));

describe("ToolContextBar — snap controls", () => {
  it("renders snap UI sections", () => {
    render(<ToolContextBar canEdit={true} reasons={[]} />);

    expect(screen.getByText("Snap")).toBeInTheDocument();
    expect(screen.getByText("Axis")).toBeInTheDocument();
    expect(screen.getByText("Space")).toBeInTheDocument();
  });
});
