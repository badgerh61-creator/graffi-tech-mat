import { renderDecorStudio } from "./renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor studio has no interactive controls", () => {
  renderDecorStudio({
    decor: [{ id: "seat-1", name: "Leather Seats" }],
  });

  expect(screen.queryByRole("slider")).toBeNull();
  expect(screen.queryByText(/apply/i)).toBeNull();
});

