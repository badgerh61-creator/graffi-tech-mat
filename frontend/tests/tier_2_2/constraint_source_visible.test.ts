import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { renderConstraintPanel } from "./renderConstraintPanel";

test("constraint source is visible", () => {
  renderConstraintPanel({
    constraints: [
      {
        id: "c1",
        type: "reference-plane",
        source: "panel-generator",
      },
    ],
  });

  expect(screen.getByText(/panel-generator/i)).toBeInTheDocument();
});

