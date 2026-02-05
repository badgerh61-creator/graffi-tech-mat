import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { renderConstraintPanel } from "./renderConstraintPanel";

test("no constraint UI when none exist", () => {
  renderConstraintPanel({ constraints: [] });

  expect(screen.queryByText(/constraint/i)).toBeNull();
});

