import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ConstraintBlockedBanner from "../../src/editor/constraints/ConstraintBlockedBanner";

vi.mock("../../src/editor/constraints/constraintViolationStore", () => ({
  useConstraintViolations: () => ({
    violations: [{ constraint_id: "c1", kind: "bounds", message: "x" }],
  }),
}));

describe("ConstraintBlockedBanner", () => {
  it("renders blocked state", () => {
    render(<ConstraintBlockedBanner />);
    expect(screen.getByText("Apply blocked")).toBeTruthy();
  });
});
