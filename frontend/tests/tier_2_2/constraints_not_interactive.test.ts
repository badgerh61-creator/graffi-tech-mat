import { screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { renderEditor } from "../utils/renderEditor";

test("constraints are not interactive", () => {
  renderEditor({
    constraints: [{ id: "c1", type: "fixed-axis" }],
  });

  expect(
    screen.getByText(/fixed-axis/i)
  ).toHaveAttribute("data-readonly", "true");
});

