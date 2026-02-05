import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { renderConstraintPanel } from "./renderConstraintPanel";

test("constraints are rendered when present", () => {
  renderConstraintPanel({
    constraints: [{ id: "c1", type: "symmetry" }],
  });

  expect(screen.getByText(/symmetry/i)).toBeInTheDocument();
});

