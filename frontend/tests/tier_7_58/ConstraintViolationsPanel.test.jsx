import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ConstraintViolationsPanel from "../../src/editor/constraints/ConstraintViolationsPanel";

vi.mock("../../src/editor/constraints/constraintViolationStore", () => ({
  useConstraintViolations: () => ({
    violations: [
      {
        constraint_id: "c1",
        kind: "locked_axis",
        message: "Rotate blocked on axis y",
        target_id: "obj-1::MeshA",
        data: { axis: "y" },
      },
    ],
  }),
}));

vi.mock("../../src/editor/selection/selectionStore", () => ({
  setSelectedId: vi.fn(),
}));

describe("ConstraintViolationsPanel", () => {
  it("renders violations", () => {
    render(<ConstraintViolationsPanel />);
    expect(screen.getByText("Constraint Violations")).toBeTruthy();
    expect(screen.getByText("locked_axis")).toBeTruthy();
    expect(screen.getByText("Select Target")).toBeTruthy();
  });
});
